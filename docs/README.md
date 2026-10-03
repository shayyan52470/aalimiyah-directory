# Programmer documentation

This directory explains how the project works and how to maintain it safely.

## Start here

- [Getting started](GETTING_STARTED.md) — run the site locally and make a first change
- [Architecture](ARCHITECTURE.md) — understand the files, browser flow, and design constraints
- [Data pipeline](DATA_PIPELINE.md) — understand the Sheet, CSV, validation, and review process
- [Google Sheets setup](GOOGLE_SHEETS_SETUP.md) — prepare the public-data tab and enable synchronization
- [GitHub administration](GITHUB_ADMIN.md) — configure Pages, labels, permissions, and branch protection
- [Code conventions](CODE_CONVENTIONS.md) — keep HTML, CSS, JavaScript, Python, and workflows consistent

## Other important documents

- [`DATA_GUIDE.md`](../DATA_GUIDE.md) defines every public CSV field.
- [`CONTRIBUTING.md`](../CONTRIBUTING.md) explains the contribution and review process.
- [`SECURITY.md`](../SECURITY.md) explains how to report vulnerabilities and handle secrets.

## Quick health check

From the repository root:

```sh
python3 scripts/check_project.py
```

That command runs the data-pipeline tests, validates the committed CSV, and assembles the exact static site GitHub Pages will deploy.
