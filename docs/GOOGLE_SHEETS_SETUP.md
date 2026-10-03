# Google Sheets setup

## Recommended workbook structure

Keep at least two tabs:

- **Public Data** contains only the canonical fields from `DATA_GUIDE.md` and is safe to publish.
- **Private Research** contains personal comparisons, investigation notes, contacts, and unfinished source analysis. Never publish this tab.

The existing workbook currently combines these concerns. Migrate the public fields before enabling automatic synchronization.

## Prepare the public tab

1. Add a tab named `Public Data`.
2. Copy the exact field headers from `scripts/data_schema.py` or `data/courses.csv`.
3. Copy reviewed values into the appropriate fields.
4. Use dropdown validation for `status`, `delivery_mode`, `gender`, and `study_load`.
5. Use semicolons in multi-value cells.
6. Protect the header row and freeze it.
7. Keep `last_verified` manual.

## Publish only that tab

In Google Sheets:

1. Choose **File → Share → Publish to web**.
2. Select `Public Data`, not the entire document.
3. Select **Comma-separated values (.csv)**.
4. Publish and copy the generated URL.

Anyone with the published URL can read that tab. Treat it as public information even if the editable workbook remains restricted.

## Add the URL to GitHub

With GitHub CLI authenticated:

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

