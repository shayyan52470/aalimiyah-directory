# Contributing

Thank you for helping build a careful, useful directory.

## Suggesting a programme

The easiest route is the structured **Submit a programme** issue form. Search existing records and issues first, provide the institution’s official programme URL, and include sources for any curriculum, fee, recognition, or admissions claim.

## Editing the CSV

1. Fork the repository and create a branch.
2. Read `DATA_GUIDE.md`.
3. Edit `data/courses.csv` without changing the header order.
4. Run `python3 scripts/check_project.py`.
5. Open a pull request and explain the change and its sources.

Please keep unrelated programme changes in separate pull requests where practical. Reviewers may adjust terminology or ask for stronger sourcing before merging.

## Code contributions

Read the [programmer documentation](docs/README.md), especially the architecture and code-convention guides. Keep the no-dependency static architecture unless a pull request identifies a concrete requirement it cannot reasonably satisfy.

Before opening a pull request:

```sh
python3 scripts/check_project.py
python3 scripts/build_site.py
python3 -m http.server 8000 --directory _site
```

Check user-facing changes locally, include tests for data-pipeline changes, and update documentation when behaviour or setup changes.

## Evidence and tone

- Prefer primary sources from the institution.
- Attribute uncertain or inferred information explicitly; otherwise leave the field blank.
- Do not submit private contact details, private messages, allegations, endorsements, rankings, or unsourced reputational claims.
- Describe jurisprudential and theological orientation neutrally and only when the source supports it.
- A linked source does not give this project permission to copy its full prose, images, or logo. Summarise factual information in your own words.

## Licensing

Code contributions are distributed under the MIT License. Data and original written descriptions are distributed under CC BY 4.0. By submitting a contribution, you agree that it may be distributed under the applicable licence.
