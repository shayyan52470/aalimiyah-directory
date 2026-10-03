#!/usr/bin/env python3
"""Validate the public course CSV before it can be merged or deployed."""

from __future__ import annotations

import csv
import re
import sys
from datetime import date
from pathlib import Path

from data_schema import ENUMS, FIELDS, MULTI_VALUE_FIELDS, clean, is_url


ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "courses.csv"


def main() -> None:
    errors: list[str] = []
    warnings: list[str] = []
    ids: set[str] = set()

    with CSV_PATH.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != FIELDS:
            errors.append("CSV headers or their order do not match scripts/data_schema.py")
        for number, row in enumerate(reader, start=2):
            row_id = clean(row.get("id"))
            label = row_id or f"row {number}"
            if not row_id or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", row_id):
                errors.append(f"{label}: id must be a lowercase kebab-case value")
            elif row_id in ids:
                errors.append(f"{label}: duplicate id")
            ids.add(row_id)

            if not clean(row.get("institution")):
                errors.append(f"{label}: institution is required")
            for field, allowed in ENUMS.items():
                value = clean(row.get(field)).lower()
                if value not in allowed:
                    errors.append(f"{label}: invalid {field} value {value!r}")

            if clean(row.get("status")) == "published":
                for field in ("programme_name", "official_url", "source_urls"):
                    if not clean(row.get(field)):
                        errors.append(f"{label}: published records require {field}")
                if not clean(row.get("last_verified")):
                    warnings.append(f"{label}: published record has no last_verified date")

            for field in ("official_url", "syllabus_url"):
                value = clean(row.get(field))
                if value and not is_url(value):
                    errors.append(f"{label}: {field} is not a valid HTTP(S) URL")
            for value in [part.strip() for part in clean(row.get("source_urls")).split(";") if part.strip()]:
                if not is_url(value):
                    errors.append(f"{label}: source_urls contains an invalid URL")

            verified = clean(row.get("last_verified"))
            if verified:
                try:
                    date.fromisoformat(verified)
                except ValueError:
                    errors.append(f"{label}: last_verified must use YYYY-MM-DD")

            for field in MULTI_VALUE_FIELDS:
                value = clean(row.get(field))
                if value and "," in value:
                    errors.append(f"{label}: use semicolons, not commas, inside {field}")

            for field, value in row.items():
                if clean(value).startswith(("=", "+", "-", "@")):
                    errors.append(f"{label}: {field} begins with a spreadsheet formula character")

    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Validated {len(ids)} course records ({len(warnings)} warnings).")


if __name__ == "__main__":
    main()
