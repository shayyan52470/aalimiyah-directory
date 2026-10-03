# Code conventions

## General

- Prefer the smallest understandable solution.
- Use UTF-8, LF line endings, two-space indentation, and a final newline. Python uses four spaces.
- Keep commits and pull requests focused on one coherent change.
- Explain intent and policy decisions; do not comment obvious syntax.
- Never commit generated `_site/`, cache directories, credentials, or private research exports.

## HTML

- Use semantic elements and preserve heading order.
- Every form control needs a visible label.
- Keep keyboard operation and visible focus states working.
- Use relative URLs for internal pages so GitHub project Pages works below `/aalimiyah-directory/`.
- Add external links through DOM APIs or static trusted markup; use `noopener noreferrer` with new tabs.

## CSS

- Reuse the custom properties in `:root` for colour, typography, radius, and shadow.
- Keep selectors shallow and component-oriented.
- Add responsive rules to the existing breakpoints unless a new content constraint genuinely requires another.
- Respect `prefers-reduced-motion`.

## Browser JavaScript

- Use native ES modules and DOM APIs; there is no bundling step.
- Treat CSV values as untrusted text. Assign them with `textContent`, never `innerHTML`.
- Keep parsing helpers in `assets/csv.js` and page behaviour in `assets/app.js`.
- Keep the interface usable when optional fields are empty.
- Do not fetch the live Google Sheet from the browser.

## Python

- Use the standard library unless a dependency solves a demonstrated need.
- Share schema constants and normalisers through `scripts/data_schema.py`.
- Write output atomically when replacing the canonical CSV.
- Add a regression test for every importer or privacy-rule fix.
- Error messages should name the record and field a contributor must fix.

## GitHub Actions

- Grant the minimum permissions per workflow.
- Pin actions to an intentional major version and review upgrades.
- Keep untrusted pull-request code away from repository secrets and write permissions.
- Data synchronization must produce a pull request, never commit directly to `main`.

