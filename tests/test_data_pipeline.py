from __future__ import annotations

import csv
import io
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from data_schema import FIELDS  # noqa: E402
from sync_sheet import convert  # noqa: E402


def csv_text(headers: list[str], row: list[str]) -> str:
    output = io.StringIO()
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(headers)
    writer.writerow(row)
    return output.getvalue()


class CanonicalImportTests(unittest.TestCase):
    def test_preserves_commas_and_splits_semicolon_values(self) -> None:
        row = {field: "" for field in FIELDS}
        row.update(
            {
                "institution": "Example Institute",
                "programme_name": "Aalimiyah",
                "status": "draft",
                "subjects": "Law, ethics and society; Hadith",
                "languages": "English; Arabic",
            }
        )
        imported = convert(csv_text(FIELDS, [row[field] for field in FIELDS]))[0]
        self.assertEqual(imported["subjects"], "Law, ethics and society; Hadith")
        self.assertEqual(imported["languages"], "English; Arabic")
        self.assertEqual(imported["id"], "example-institute-aalimiyah")


class LegacyImportTests(unittest.TestCase):
    headers = [
        "Institution Name",
        "Course Name",
        "Location",
        "Language",
        "Full time",
        "Madhab",
        "Aqaa'id",
        "Key references",
        "Comments",
        "Big question for myself: What living standards do I want ",
    ]

    def test_does_not_publish_personal_notes_or_likely_values(self) -> None:
        imported = convert(
            csv_text(
                self.headers,
                [
                    "Example Institute",
                    "Aalimiyah",
                    "Online, UK",
                    "Likely English",
                    "FALSE",
                    "Likely Hanafi",
                    "Likely Maturidi",
                    "https://third-party.example/course",
                    "Private research comment",
                    "Personal preference",
                ],
            )
        )[0]
        self.assertEqual(imported["status"], "draft")
        self.assertEqual(imported["languages"], "")
        self.assertEqual(imported["jurisprudence_school"], "")
        self.assertEqual(imported["theology_school"], "")
        self.assertEqual(imported["notes"], "")
        self.assertNotIn("Personal preference", imported.values())

    def test_recognises_a_provider_owned_domain(self) -> None:
        imported = convert(
            csv_text(
                self.headers,
                [
                    "Example Institute",
                    "Aalimiyah",
                    "Online",
                    "English",
                    "FALSE",
                    "Hanafi",
                    "Maturidi",
                    "https://exampleinstitute.org/aalimiyah",
                    "",
                    "",
                ],
            )
        )[0]
        self.assertEqual(imported["status"], "published")
        self.assertEqual(imported["official_url"], "https://exampleinstitute.org/aalimiyah")


if __name__ == "__main__":
    unittest.main()

