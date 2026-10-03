# Google Sheets setup

## Current workbook structure

Keep at least two tabs:

- **Public Data** contains only the canonical fields from `DATA_GUIDE.md` and is safe to publish.
- **Private Research** contains personal comparisons, investigation notes, contacts, and unfinished source analysis. Never publish this tab.

The existing workbook now follows this separation. `Public Data` is the canonical synchronization source and the original `Sheet1` remains unpublished research material.

## Rebuilding or extending the public tab

1. Keep the tab named `Public Data`; changing its identity requires republishing it and updating GitHub.
2. Preserve the exact field headers from `scripts/data_schema.py` or `data/courses.csv`.
3. Add reviewed values to the appropriate fields.
4. Use dropdown validation for `status`, `delivery_mode`, `gender`, and `study_load`.
5. Use semicolons in multi-value cells.
6. Protect the header row and freeze it.
7. Keep `last_verified` manual.

## Publication scope

The `Public Data` tab is already published as CSV. If publication is stopped or rebuilt, use Google Sheets:

1. Choose **File → Share → Publish to web**.
2. Select `Public Data`, not the entire document.
3. Select **Comma-separated values (.csv)**.
4. Publish and copy the generated URL.

Anyone with the published URL can read that tab. Treat it as public information even if the editable workbook remains restricted.

## Updating the URL in GitHub

The current URL is already stored as a GitHub Actions secret. To replace it with GitHub CLI authenticated:

```sh
gh secret set GOOGLE_SHEET_CSV_URL
```

Paste the published CSV URL at the prompt. Do not place the URL in a committed file if you prefer it to remain undiscoverable.

Alternatively, use **Repository Settings → Secrets and variables → Actions → New repository secret** and name it `GOOGLE_SHEET_CSV_URL`.

## Test the integration

1. Open the repository’s **Actions** tab.
2. Select **Propose Google Sheet updates**.
3. Choose **Run workflow**.
4. Confirm that it opens a pull request rather than changing `main`.
5. Review the CSV diff, validation result, and cited sources before merging.

## Revoking access

Stop publishing the Google tab and delete the `GOOGLE_SHEET_CSV_URL` secret. Existing committed data remains public in Git history; remove sensitive data through a separate incident response rather than an ordinary deletion commit.
