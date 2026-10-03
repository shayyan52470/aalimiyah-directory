# Aalimiyah Directory

An open-source directory of online and in-person Aalimiyah programmes, courses, and study options.

The site is deliberately static. A reviewed CSV snapshot powers the directory and its interactive data explorer; GitHub Pages publishes only changes merged into `main`. It has no runtime database, application server, package installation, or project-owned login system.

## Documentation

Programmers should begin with the [`docs/` documentation hub](docs/README.md):

- [Getting started](docs/GETTING_STARTED.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Data pipeline](docs/DATA_PIPELINE.md)
- [Google Sheets setup](docs/GOOGLE_SHEETS_SETUP.md)
- [GitHub administration](docs/GITHUB_ADMIN.md)
- [Code conventions](docs/CODE_CONVENTIONS.md)

The exact public fields and editorial definitions live in [DATA_GUIDE.md](DATA_GUIDE.md).

## How it works

1. Researchers maintain programme records in a structured Google Sheet or directly in `data/courses.csv`.
2. A scheduled workflow exports the Sheet into the canonical CSV and opens a pull request.
3. Automated checks validate identifiers, required fields, URLs, enums, dates, and multi-value formatting.
4. A maintainer reviews the sources and merges the pull request.
5. GitHub Pages deploys the approved snapshot.

The Sheet is an editing interface; `data/courses.csv` is the public, versioned snapshot used by the website. The sync process imports only approved public fields, preventing research notes or personal comparison columns from being exposed.

## Local development

Python 3 is the only local requirement.

```sh
python3 scripts/check_project.py
python3 scripts/build_site.py
python3 -m http.server 8000 --directory _site
```

Open `http://127.0.0.1:8000`. Do not open the HTML files directly because browsers restrict local CSV requests.

If GNU Make is installed, the shortcuts are:

```sh
make check
make serve
```

## Google Sheet sync

The workbook has a dedicated `Public Data` tab containing the canonical headers in `DATA_GUIDE.md`. Only that tab is published as CSV; the original research tab remains unpublished. Its URL is stored in the `GOOGLE_SHEET_CSV_URL` GitHub Actions secret.

The **Propose Google Sheet updates** workflow runs daily. When the Sheet changes, it validates the export and opens or refreshes a pull request. It never deploys unreviewed Sheet changes directly.

See [docs/GOOGLE_SHEETS_SETUP.md](docs/GOOGLE_SHEETS_SETUP.md) before changing the publication or rebuilding the integration.

For a one-off local export:

```sh
GOOGLE_SHEET_CSV_URL='published-csv-url' python3 scripts/sync_sheet.py
python3 scripts/validate_data.py
```

The importer supports both the canonical headers and the original research-sheet headers. Scheduled production sync uses the canonical `Public Data` tab.

## GitHub setup

- In **Settings → Pages**, select **GitHub Actions** as the source.
- Protect `main` and require pull requests, at least one approval, and the validation check.
- If Sheet sync cannot open a pull request, enable the repository setting that allows GitHub Actions to create and approve pull requests.
- Create the labels `course-submission` and `needs-review` so submitted issues are categorized automatically.

The full owner checklist—including safe GitHub CLI authentication and branch-protection settings—is in [docs/GITHUB_ADMIN.md](docs/GITHUB_ADMIN.md).

## Contributing

Use the website submission page, open the structured GitHub issue form, or propose a direct CSV edit. Read [CONTRIBUTING.md](CONTRIBUTING.md) and [DATA_GUIDE.md](DATA_GUIDE.md) first.

## Licence

Website code is licensed under the [MIT License](LICENSE). Data in `data/` and original written descriptions are licensed under [CC BY 4.0](LICENSE-DATA). By submitting a contribution, you agree that it may be distributed under the applicable licence.
