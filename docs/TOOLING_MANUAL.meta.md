# TOOLING_MANUAL.md — metadoc

_Created: 11-07-2026 · Last updated: 11-07-2026_

Companion record for
[docs/TOOLING_MANUAL.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/docs/TOOLING_MANUAL.md).

## Purpose

Operator manual for the COLOGNE build-meta repo: enable a new operator/contributor to
run every live workflow (cleanup taxonomy, correction engine, character/tag censuses,
transcoding tables, Markdown export, local installs, new-dictionary onboarding) from
the manual alone, without reading source code.

## Audience

New CDSL maintainers and contributors; agent sessions doing build/tooling work in this
repo; the future operator who inherits the Windows XAMPP / Mac local installs.

## Provenance

Authored 11-07-2026 by Fable 5 (`claude-fable-5`) executing handoff
[H506](https://github.com/gasyoun/Uprava/blob/main/handoffs/H506-Fable_COLOGNE_cross_cutting_tooling_manual_10.07.26.md)
(manual-coverage census of 10-07-2026, which flagged COLOGNE as deserving a detailed
manual but lacking one). Modelled on the gold-standard operator manual
[RussianRamayana Litpam-Indexator MANUAL.md](https://github.com/gasyoun/RussianRamayana/blob/main/Litpam-Indexator/docs/indesign-pipeline/MANUAL.md).
Source evidence: repo docs
([README.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/README.md),
[ARCHITECTURE_REVIEW.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/ARCHITECTURE_REVIEW.md),
[readme_new_dict_addition.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/readme_new_dict_addition.md))
plus four parallel directory-exploration passes over all 14 tooling directories
(same model tier).

## Ranked improvement backlog

| # | Item | Status |
|---|---|---|
| 1 | Verify each documented command by executing it in a full CDSL umbrella checkout (this manual is source-derived; commands were not all run live) | open |
| 2 | Add a worked end-to-end example with real output for one census run (`sh redo_one.sh mw`) once a csl-orig sibling is available | open |
| 3 | When the taxonomy `human_decision` pass lands and files move, update the walkthrough paths and the load-bearing table in the same PR | open |
| 4 | If `stardict/` is ported to Python 3 or retired (Human Approval Queue #3), rewrite or drop its section | open |
| 5 | Cross-link from the org manuals index / FEATURES_INDEX if a docs census consumes this | open |

## Known limitations

- Written from source-and-docs evidence; the sibling `cologne/csl-orig` umbrella
  layout was not present in the authoring checkout, so `redo_*` commands are
  transcribed from the scripts, not re-executed.
- The `issues/` section is deliberately structural (270 archival files are not
  enumerated).
- Load-bearing verdicts mirror the cleanup taxonomy as of 464-row generation
  (0 rows human-decided); they may shift once decisions land.

## Related documents

- [README.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/README.md) — repo intro + taxonomy entry point
- [ARCHITECTURE_REVIEW.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/ARCHITECTURE_REVIEW.md) — findings + roadmap
- [docs/cleanup/taxonomy_summary.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/docs/cleanup/taxonomy_summary.md) — cleanup state
- [csl-corrections/docs/correction-workflow.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md) — canonical correction workflow

## Revision history

| Date | Change | By |
|---|---|---|
| 11-07-2026 | Initial version (H506): cheat-sheet, data-flow, 14 directory walkthroughs, new-dict flow, load-bearing verdicts, symptom table, glossary, maintainer appendix | Fable 5 (`claude-fable-5`) |

_Dr. Mārcis Gasūns_
