# Architecture

## Design goals

The project favours auditability, low operating cost, and easy contribution over application complexity. It is a static website with a version-controlled data snapshot.

There is deliberately:

- no application server;
- no runtime database;
- no user authentication owned by the project;
- no package manager or third-party runtime dependency;
- no direct write access from the public website to the dataset.

GitHub handles contributor identity, issue submissions, pull-request review, automation, and hosting.

## Repository map

```text
.
├── index.html                 Programme directory
├── data.html                  Interactive CSV explorer
├── methodology.html           Public editorial methodology
├── submit.html                Contribution entry point
├── assets/
│   ├── app.js                 Page controllers and rendering
│   ├── csv.js                 Browser CSV parser
│   ├── styles.css             Shared visual system
│   ├── favicon.svg
│   └── og.png
├── data/
│   └── courses.csv            Reviewed public data snapshot
├── scripts/
│   ├── data_schema.py         Canonical fields and normalisers
│   ├── sync_sheet.py          Sheet export and safe legacy mapping
│   ├── validate_data.py       Merge/deployment gate
│   └── build_site.py          Static artifact assembly
├── tests/                     Data conversion and privacy tests
├── config/                    Non-secret source identifiers
├── docs/                      Programmer and maintainer guides
└── .github/                   Forms, review templates, and Actions
```

## Browser flow

Both interactive pages load `data/courses.csv` with `fetch`, parse it in the browser, and render from plain objects. The directory filters to `status=published`. The data explorer intentionally shows drafts and archived rows because the CSV itself is public.

All dynamic text is assigned through DOM `textContent`; source data is never inserted as HTML. External links open in a new tab with `noopener noreferrer`.

## Build flow

`scripts/build_site.py` copies only public website files into `_site/`. GitHub Pages deploys that directory. Maintenance scripts, tests, private GitHub configuration, and documentation are therefore not part of the deployed artifact.

## Change boundaries

- Add or rename CSV fields in `scripts/data_schema.py` first, then update the importer, validator, browser labels, documentation, tests, and Sheet headers together.
- Keep presentation in `assets/styles.css`, data parsing in `assets/csv.js`, and page behaviour in `assets/app.js`.
- Do not add a framework merely for convenience. Reconsider the stack only when a concrete requirement—such as thousands of records, authenticated moderation, or server-side search—cannot be handled cleanly by the static model.
- Do not make the live site fetch Google Sheets directly. The reviewed CSV is the production boundary.

