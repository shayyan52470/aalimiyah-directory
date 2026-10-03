"""Shared schema and normalisation helpers for the Aalimiyah Directory."""

from __future__ import annotations

import re
import unicodedata
from urllib.parse import urlparse


FIELDS = [
    "id",
    "institution",
    "programme_name",
    "programme_type",
    "status",
    "delivery_mode",
    "institution_location",
    "country",
    "timezone",
    "languages",
    "arabic_entry_level",
    "gender",
    "study_load",
    "duration_years",
    "schedule",
    "curriculum",
    "jurisprudence_school",
    "theology_school",
    "qualification",
    "accreditation",
    "entry_requirements",
    "tuition_amount",
    "tuition_currency",
    "tuition_period",
    "tuition_notes",
    "financial_aid",
    "subjects",
    "texts",
    "tags",
    "official_url",
    "syllabus_url",
    "source_urls",
    "last_verified",
    "notes",
]

MULTI_VALUE_FIELDS = {
    "languages",
    "jurisprudence_school",
    "theology_school",
    "subjects",
    "texts",
    "tags",
    "source_urls",
}

ENUMS = {
    "status": {"draft", "published", "archived"},
    "delivery_mode": {"online", "in-person", "hybrid", "unknown", ""},
    "gender": {"open", "men", "women", "separate", "unknown", ""},
    "study_load": {"full-time", "part-time", "flexible", "unknown", ""},
}


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def slugify(value: str) -> str:
    normal = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", normal.lower()).strip("-")


def split_values(value: str, separators: str = r"[;,]") -> list[str]:
    seen: set[str] = set()
    values: list[str] = []
    for raw in re.split(separators, clean(value)):
        item = clean(raw).strip(" .")
        key = item.casefold()
        if item and key not in seen:
            values.append(item)
            seen.add(key)
    return values


def join_values(values: list[str]) -> str:
    return "; ".join(values)


def extract_urls(value: str) -> list[str]:
    return re.findall(r"https?://[^\s,]+", value or "")


def is_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)

