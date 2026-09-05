_Created: 15-05-2026 · Last updated: 05-09-2026_

# Cleanup Taxonomy Schema

This taxonomy is a proposal layer. It is intended for human approval before any file moves, deletes, or refactors.

## Lifecycle Labels

- `active-core`: Maintained code/data used by repeatable dictionary workflows.
- `active-ops`: Maintained operational scripts or local setup helpers.
- `generated-report`: Output that can probably be regenerated from scripts or data.
- `reference-doc`: Human-facing documentation or scholarly/project reference material.
- `legacy-python2`: Code that requires Python 2 or fails Python 3 syntax parsing.
- `prototype`: Experimental API/frontend/export work that needs promotion or retirement.
- `archival-issue`: Historical issue workspace; preserve for provenance by default.
- `external-inventory`: Lists or notes about external services/artifacts.
- `repo-governance`: Repository-level governance, contribution, or assistant metadata.

## Workflow Labels

- `transliteration`: SLP1, IAST, Devanagari, or other transliteration mappings.
- `xml-tag-audit`: XML-like tag counting and related generated tag reports.
- `unicode-audit`: Extended Unicode/non-ASCII scans and reports.
- `corrections`: Line-change or dictionary correction workflows.
- `dictionary-export`: Markdown, StarDict, Babylon, or transform/export tooling.
- `api-design`: API docs or service prototypes.
- `frontend-prototype`: Browser-side prototype code or transformed HTML fixtures.
- `local-install`: Local XAMPP/Mac setup, downloads, or environment notes.
- `aws-inventory`: S3/AWS blob, scan, PDF, or listing references.
- `issue-repair`: Issue-specific repair, analysis, or fixture material.
- `scholarly-reference`: Bibliography, sandhi, presentation, or external reference files.
- `repo-governance`: Repository metadata and contributor-facing process docs.
- `review-roadmap`: Cleanup, architecture, or planning artifacts.

## Proposed Actions

- `keep-maintained`: Keep in place and maintain.
- `test-and-package`: Add tests, package/import path, and keep active.
- `mark-generated`: Mark as generated and document regeneration command.
- `archive-no-refactor`: Preserve as historical material; do not refactor by default.
- `port-or-retire`: Either port to Python 3/current tooling or explicitly retire.
- `promote-or-sunset`: Decide whether to productize prototype or archive it.
- `consolidate-shared`: Extract shared logic into a maintained module.
- `harden-ops`: Improve safety, verification, paths, and failure handling.
- `document-owner`: Assign maintainer/status and expected use.

## Approval Columns

The generated CSV leaves `human_decision` and `human_notes` blank. Suggested values for `human_decision`:

- `approve`: accept the proposed taxonomy/action.
- `override`: keep the path but change lifecycle, workflow, or action.
- `defer`: revisit after related cleanup issues land.
- `ignore`: exclude from cleanup tracking.

_Dr. Mārcis Gasūns_
