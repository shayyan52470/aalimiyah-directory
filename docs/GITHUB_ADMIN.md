# GitHub administration

This is the one-time owner checklist for `shayyan52470/aalimiyah-directory`.

## Access needed for assisted setup

Git over SSH can push commits, but repository configuration needs GitHub CLI or equivalent API access. On your own computer:

1. Install GitHub CLI from <https://cli.github.com/>.
2. Run `gh auth login`.
3. Select `GitHub.com`, authenticate through the browser, and use SSH for Git if prompted.
4. Confirm with `gh auth status`.

Do not send passwords, personal access tokens, recovery codes, or SSH private keys through chat. Browser-based `gh auth login` stores credentials on your machine. Once `gh auth status` succeeds in the shared environment, an assistant can run repository setup commands without seeing your password.

## Initial publication checklist

1. Review the generated files and run `make check`.
2. Commit and push `main`.
3. Under **Settings → Pages**, choose **GitHub Actions** as the source.
4. Under **Settings → Actions → General**, allow GitHub Actions to create and approve pull requests.
5. Add the `GOOGLE_SHEET_CSV_URL` secret after preparing the public Sheet tab.
6. Create the labels `course-submission` and `needs-review`.
7. Run **Deploy GitHub Pages** and **Propose Google Sheet updates** manually once.

## Branch protection

Create a ruleset targeting `main` with:

- pull requests required before merging;
- one approval required;
- stale approvals dismissed when new commits are pushed;
- required status check: the validation job from **Validate contributions**;
- conversation resolution required;
- force pushes and branch deletion blocked;
- administrator bypass kept narrow.

The Sheet-sync workflow needs permission to push only its automation branch and open a pull request. It does not need to bypass `main` protection.

## CODEOWNERS and labels

`.github/CODEOWNERS` requests owner review for all changes and explicitly covers data, scripts, and workflows. Ensure the `course-submission` and `needs-review` labels exist; GitHub does not create missing labels from an issue-form definition.

## Routine owner work

- Review new programme issues and close duplicates.
- Check sources before marking a record published.
- Review the daily Sheet-sync pull request when it changes.
- Refresh stale `last_verified` dates only after opening the sources.
- Keep Actions updated through reviewed dependency pull requests.
- Archive discontinued programmes instead of erasing their history.

