# Getting started

## Requirements

- Git
- Python 3.10 or newer
- GNU Make is recommended, but every command can also be run directly
- GitHub CLI is optional for ordinary development and recommended for maintainers

There are no JavaScript packages, Python packages, database servers, or API keys to install. The browser code uses native ES modules and the maintenance scripts use only Python’s standard library.

## Clone and verify

```sh
git clone git@github.com:shayyan52470/aalimiyah-directory.git
cd aalimiyah-directory
python3 scripts/check_project.py
```

Warnings about missing `last_verified` dates do not stop a build. Errors do.

## Preview locally

```sh
python3 scripts/build_site.py
python3 -m http.server 8000 --directory _site
```

Open <http://127.0.0.1:8000>. Stop the server with `Ctrl+C`.

Do not double-click the HTML files. Browsers block the CSV request when pages are opened through `file://`.

## Make a change

1. Create a descriptive branch: `git switch -c docs/improve-setup`.
2. Change one coherent area.
3. Run `python3 scripts/check_project.py`.
4. Build and preview user-facing changes with the commands above.
5. Commit the change and open a pull request.

For data edits, read `DATA_GUIDE.md` before changing `data/courses.csv`.

## Common commands

| Command | Purpose |
|---|---|
| `python3 scripts/check_project.py` | Run the complete dependency-free project check |
| `make check` | Run tests, validation, and a production build |
| `make test` | Test conversion and privacy rules |
| `make validate` | Validate the committed CSV |
| `make build` | Assemble `_site/` for GitHub Pages |
| `make serve` | Build and serve the site locally |
| `make sync` | Import the configured published Sheet CSV |
| `make clean` | Delete generated local files |

Generated `_site/` and Python cache directories are ignored by Git and must not be committed.
