#!/usr/bin/env python3
"""Export the configured Google Sheet into the public, reviewed CSV snapshot."""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

from data_schema import FIELDS, clean, extract_urls, join_values, slugify, split_values


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "courses.csv"
CONFIG = ROOT / "config" / "data-source.json"


def source_text(source_file: str | None) -> str:
    if source_file:
        return Path(source_file).read_text(encoding="utf-8-sig")

    configured = os.environ.get("GOOGLE_SHEET_CSV_URL", "").strip()
    if not configured:
        config = json.loads(CONFIG.read_text(encoding="utf-8"))
        configured = (
            "https://docs.google.com/spreadsheets/d/"
            f"{config['sheet_id']}/export?format=csv&gid={config['gid']}"
        )

    try:
        request = urllib.request.Request(configured, headers={"User-Agent": "aalimiyah-directory-sync/1.0"})
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read().decode("utf-8-sig")
    except urllib.error.HTTPError as exc:
        if exc.code in {401, 403}:
            raise SystemExit(
                "The Sheet is not publicly exportable. Publish the data tab as CSV, "
                "then save that URL as the GOOGLE_SHEET_CSV_URL repository secret."
            ) from exc
        raise


def infer_delivery(location: str) -> str:
    lowered = location.casefold()
    if "online" in lowered and any(term in lowered for term in ("melbourne", "uk", "sydney", "campus")):
        return "online"
    return "online" if "online" in lowered else "in-person"


def infer_country(location: str) -> str:
    lowered = location.casefold()
    countries = {
        "pakistan": "Pakistan",
        "yemen": "Yemen",
        "south africa": "South Africa",
        "australia": "Australia",
        "sydney": "Australia",
        "melbourne": "Australia",
        "uk": "United Kingdom",
        "united kingdom": "United Kingdom",
    }
    for needle, country in countries.items():
        if needle in lowered:
            return country
    return ""


def legacy_official_url(institution: str, urls: list[str]) -> str:
    """Only promote a legacy reference when its host plausibly belongs to the provider."""
    known_hosts = {"Hadhramout University": {"hu.edu.ye"}}
    ignored_tokens = {"academy", "college", "darul", "institute", "islamic", "university"}
    tokens = {
        token for token in slugify(institution).split("-")
        if len(token) >= 4 and token not in ignored_tokens
    }
    for url in urls:
        host = urlparse(url).netloc.casefold().removeprefix("www.")
        # Match provider tokens against the registrable part, not a coincidental TLD.
        host_identity = "".join(host.split(".")[:-1])
        if host in known_hosts.get(institution, set()) or any(token in host_identity for token in tokens):
            return url
    return ""


def sourced_legacy_value(value: str) -> str:
    value = clean(value)
    return "" if "likely" in value.casefold() else value


def normalise_canonical(row: dict[str, str]) -> dict[str, str]:
    result = {field: clean(row.get(field, "")) for field in FIELDS}
    for field in ("languages", "jurisprudence_school", "theology_school", "tags", "subjects", "texts"):
        # Canonical sheets use semicolons so commas can remain inside names.
        result[field] = join_values(split_values(result[field], r";"))
    result["source_urls"] = join_values(split_values(result["source_urls"], r"[;\s]+"))
    result["id"] = result["id"] or slugify(f"{result['institution']} {result['programme_name']}")
    result["status"] = result["status"].lower() or "draft"
    return result


def normalise_legacy(row: dict[str, str]) -> dict[str, str]:
    institution = clean(row.get("Institution Name"))
    programme = clean(row.get("Course Name"))
    location = clean(row.get("Location"))
    references = clean(row.get("Key references"))
    urls = extract_urls(references)
    official = legacy_official_url(institution, urls)
    curriculum = clean(row.get("Darse Structure"))
    is_full_time = clean(row.get("Full time")).casefold() == "true"
    status = "published" if institution and programme and official else "draft"
    tags = []
    if curriculum:
        tags.append(slugify(curriculum))

    return {
        "id": slugify(f"{institution} {programme or 'programme'}"),
        "institution": institution,
        "programme_name": programme,
        "programme_type": "Aalimiyah" if programme else "",
        "status": status,
        "delivery_mode": infer_delivery(location) if location else "unknown",
        "institution_location": location,
        "country": infer_country(location),
        "timezone": "",
        "languages": join_values(split_values(sourced_legacy_value(row.get("Language")))),
        "arabic_entry_level": clean(row.get("Criteria")),
        "gender": "unknown",
        "study_load": "full-time" if is_full_time else "part-time",
        "duration_years": clean(row.get("Years")),
        "schedule": "",
        "curriculum": curriculum,
        "jurisprudence_school": join_values(split_values(sourced_legacy_value(row.get("Madhab")))),
        "theology_school": join_values(split_values(sourced_legacy_value(row.get("Aqaa'id")))),
        "qualification": "",
        "accreditation": "",
        "entry_requirements": "",
        "tuition_amount": "",
        "tuition_currency": "",
        "tuition_period": "",
        "tuition_notes": clean(row.get("Cost of Course")),
        "financial_aid": "",
        "subjects": join_values(split_values(clean(row.get("List of Subjects")))),
        "texts": join_values(split_values(clean(row.get("List of Books")))),
        "tags": join_values(tags),
        "official_url": official,
        "syllabus_url": next((url for url in urls if url.lower().endswith(".pdf")), ""),
        "source_urls": join_values(urls),
        "last_verified": "",
        "notes": "",
    }


def convert(text: str) -> list[dict[str, str]]:
    reader = csv.DictReader(io.StringIO(text))
    headers = set(reader.fieldnames or [])
    canonical = {"id", "institution", "programme_name", "status"}.issubset(headers)
    rows: list[dict[str, str]] = []
    for raw in reader:
        if not any(clean(value) for value in raw.values()):
            continue
        row = normalise_canonical(raw) if canonical else normalise_legacy(raw)
        if row["institution"]:
            rows.append(row)
    return rows


def write_rows(rows: list[dict[str, str]]) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", delete=False, dir=OUTPUT.parent) as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
        temporary = Path(handle.name)
    temporary.replace(OUTPUT)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", help="Use a local CSV export instead of downloading the Sheet")
    args = parser.parse_args()
    rows = convert(source_text(args.source_file))
    write_rows(rows)
    print(f"Synced {len(rows)} records to {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
