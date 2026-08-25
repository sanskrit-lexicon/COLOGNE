# human_decision fill — taxonomy_proposals.csv, 2026-08-25

_Created: 25-08-2026 · Last updated: 25-08-2026_

Executes handoff [H3484](https://github.com/gasyoun/Uprava/blob/main/handoffs/H3484-OxAlpha_COLOGNE_cologne-cleanup-464-execute_25.08.26.md): fills the ratified `human_decision` column of
[taxonomy_proposals.csv](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/docs/cleanup/taxonomy_proposals.csv)
for all 464 rows.

## Rule applied

The COLOGNE tooling-cleanup ruling of **19-07-2026** (M.G., weekly @DECIDE sheet; recorded in
[Uprava GTD_ARCHIVE.md](https://github.com/gasyoun/Uprava/blob/main/GTD_ARCHIVE.md)) was a plain assent with no
per-bucket amendment: *the proposed dispositions stand as written across all 6 priority buckets*. Therefore:

> `human_decision` := `proposed_action`, verbatim, for every row. No re-adjudication, no divergence.
> `human_notes` left empty (the ruling carried no notes).

Priority buckets from [taxonomy_summary.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/docs/cleanup/taxonomy_summary.md) § Human Approval Queue map to implementation slices in
[cleanup_issue_backlog.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/docs/cleanup/cleanup_issue_backlog.md) (annotated with their issues in the same commit).

## Fill result (parity 464 → 464)

| Disposition | Rows |
|---|---:|
| `archive-no-refactor` | 288 |
| `mark-generated` | 90 |
| `harden-ops` | 29 |
| `promote-or-sunset` | 19 |
| `test-and-package` | 16 |
| `keep-maintained` | 10 |
| `document-owner` | 6 |
| `port-or-retire` | 4 |
| `consolidate-shared` | 2 |
| **Total** | **464** |

Checks run on the filled file:

- Row count before/after: 464 → 464 (no rows added or dropped).
- Empty `human_decision` cells after fill: **0**.
- Every `human_decision` equals its row's `proposed_action` (asserted programmatically).
- Diff touches only the `human_decision` column; line endings (CRLF), quoting and all other columns unchanged.

## Residual table

None — 0 rows left empty; no genuinely ambiguous rows surfaced (the ratification covered all six buckets without amendment).

## Slice issues opened per cleanup_issue_backlog.md

| Slice | Issue | Status |
|---|---|---|
| 1 Approve cleanup taxonomy schema and inventory workflow | [#479](https://github.com/sanskrit-lexicon/COLOGNE/issues/479) | closed completed (approval itself was the 19-07-2026 ruling) |
| 2 Mark generated reports and document regeneration commands | [#480](https://github.com/sanskrit-lexicon/COLOGNE/issues/480) | open |
| 3 Preserve issue workspaces as archival by default | [#481](https://github.com/sanskrit-lexicon/COLOGNE/issues/481) | open |
| 4 Package and test active core scripts | [#482](https://github.com/sanskrit-lexicon/COLOGNE/issues/482) | open |
| 5 Consolidate transliteration into one maintained source | [#483](https://github.com/sanskrit-lexicon/COLOGNE/issues/483) | open |
| 6 Decide port-or-retire policy for Python 2 and legacy scripts | [#484](https://github.com/sanskrit-lexicon/COLOGNE/issues/484) | open |
| 7 Promote or sunset prototypes | [#485](https://github.com/sanskrit-lexicon/COLOGNE/issues/485) | open |
| 8 Harden operational setup and download workflows | [#486](https://github.com/sanskrit-lexicon/COLOGNE/issues/486) | open |
| 9 Assign owners for reference and governance material | [#487](https://github.com/sanskrit-lexicon/COLOGNE/issues/487) | open |

Tracker: [#478](https://github.com/sanskrit-lexicon/COLOGNE/issues/478).

_Executor: OxAlpha (`opencode/x-preview-f-free`), 25-08-2026._

_Dr. Mārcis Gasūns_
