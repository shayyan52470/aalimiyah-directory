# Data pipeline

## Source of truth

The Google Sheet is the convenient editorial workspace. `data/courses.csv` is the reviewed, versioned, deployable snapshot. The website reads only the committed CSV.

```text
Google Sheet public-data tab
        │ scheduled/manual export
        ▼
scripts/sync_sheet.py
        │ whitelist + normalisation
        ▼
data/courses.csv
        │ validation + human review
        ▼
pull request → main → GitHub Pages
```

## Why the sync opens a pull request

A spreadsheet edit can contain an accidental deletion, an unsupported claim, malformed data, or a private note. Synchronization therefore never writes directly to `main`. The workflow updates `automation/google-sheet-sync` and opens or refreshes a pull request.

## Import modes

`sync_sheet.py` detects two formats:

1. **Canonical format** uses the exact public headers in `DATA_GUIDE.md`. This is the long-term format.
2. **Legacy research format** maps the original Sheet’s known columns through a strict whitelist. Personal notes, reputation fields, living preferences, and unsourced values containing “likely” are discarded.

Unknown source columns are ignored. An automated import never updates `last_verified`; that date records a human source check.

## Multi-value fields

Use semicolons inside `languages`, schools, `subjects`, `texts`, `tags`, and `source_urls`:

```text
Arabic grammar; Hadith; Tafsir
```

Do not use commas as separators. Commas may be meaningful within a title or description.

## Validation

`scripts/validate_data.py` checks:

- exact headers and column order;
- stable kebab-case IDs and uniqueness;
- required fields for published records;
- controlled status, delivery, gender, and study-load values;
- HTTP(S) links and ISO dates;
- semicolon formatting for multi-value cells;
- spreadsheet formula-injection prefixes.

Warnings identify research debt but permit deployment. Errors block the pull request and deployment.

## Changing the schema

Schema changes must be atomic. Update all of the following in one pull request:

1. `FIELDS` and related rules in `scripts/data_schema.py`;
2. canonical and legacy conversion in `scripts/sync_sheet.py`;
3. validation in `scripts/validate_data.py`;
4. labels, filters, and rendering in `assets/app.js`;
5. `DATA_GUIDE.md` and the public methodology page;
6. the public-data Sheet headers;
7. automated tests and the committed CSV.

