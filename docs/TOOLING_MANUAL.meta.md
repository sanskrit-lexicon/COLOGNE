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
[H506](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H506-Fable_COLOGNE_cross_cutting_tooling_manual_10.07.26.md)
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

## Intended use / known misuse

**For:** onboarding a new operator/contributor onto every *live, runnable* workflow in
COLOGNE — which command to type, from which directory, against which sibling-repo
layout — without reading the source of `tools/`, `enhancements/code/`, `eascii/`,
`xmltag/`, `iast/`, `makemd/`, `localinstall/`, or `stardict/` first. It is also the
correct first stop for diagnosing a failure via the Symptom → cause → cure table, and
for the new-dictionary-onboarding map (which still defers to
[readme_new_dict_addition.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/readme_new_dict_addition.md)
for execution detail).

**Known/likely misuse:**

- **Treating it as a source-text correction guide.** It explicitly documents only the
  local engine (`updateByLine.py`); the canonical correction workflow is
  [csl-corrections/docs/correction-workflow.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md).
  Applying corrections from this manual alone skips the snapshot/promote/audit stages.
- **Running commands verbatim without the `cologne/` umbrella sibling layout.** Nearly
  every `redo_*`/`download*`/`install_local.sh` command assumes COLOGNE sits inside a
  `cologne/` directory next to `csl-orig` (and, for `iast/`, `csl-apidev` +
  `csl-websanlexicon`) — a bare GitHub checkout will fail on input paths, and that
  failure is layout, not a tool bug, per the manual's own Environment section.
  Misreading such a failure as "the script is broken" is the most likely error.
- **Reading transcoder silence as success.** Both `iast/transcoder.py` and its
  divergent copy `stardict/transcoder.py` return input **unchanged instead of
  erroring** when they cannot find their FSM XML tables (wrong CWD, or a missing
  `stardict/data/transcoder/`) — the manual flags this as a P1 silent-passthrough
  defect. A `GOOD`/`WARNING` console line from `slp1_iast.py`, not silence, is the
  real success signal; treating "no error" as "it worked" is the documented trap.
- **Editing `iast/slp1_roman.xml` or `roman_slp1.xml` without running `install_local.sh`
  and pushing the two PHP-repo consumers.** The three copies are hand-synced; editing
  only the COLOGNE copy leaves the live site on stale tables.
- **Treating the cleanup-taxonomy CSV as an execution order.** `tools/propose_cleanup_taxonomy.py`
  output is proposal-only (`human_decision` blank for all 464 rows as of 11-07-2026);
  moving or deleting a file on the strength of the CSV alone, before a human fills the
  decision column and an issue is opened from the backlog, contradicts the documented
  human loop.
- **Running `stardict/` or `enhancements/issue10/` as templates for new work.** Both are
  flagged 🔴 legacy Python-2-only in the cheat-sheet; the manual documents them for
  operability of existing exports, not as a pattern to extend.

## Maintenance & sunset plan

**Owner:** the COLOGNE repo itself — specifically whoever next touches the directories
this manual documents (14 tooling directories) or the cleanup-taxonomy pipeline in
`tools/`. There is no dedicated bot or CI job that keeps this manual current; it is
maintained the same way it was written — an agent session re-reading source + running
`tools/propose_cleanup_taxonomy.py` and updating the affected walkthrough section in
the same PR as the underlying change (see backlog item 3 above).

**Sunset triggers:**

- If the taxonomy `human_decision` pass lands and files referenced here move or are
  retired (backlog item 3), the walkthrough sections for those directories need a
  same-PR update, not a rewrite from scratch.
- If `stardict/` is ported to Python 3 or retired (Human Approval Queue item, backlog
  item 4), its walkthrough section and the cheat-sheet status row are the ones to
  rewrite or drop.
- **What "archived/ended" looks like:** this manual is retired only if COLOGNE's
  tooling surface is itself consolidated or the repo is merged/retired at the org
  level — there is no independent expiry date. Until then it stays `active` and is
  expected to be edited in place rather than superseded by a new document.

## Deprecation status

`active` — authored same-day (11-07-2026) as its subject document, with backlog item 1
("commands not yet run live in a full CDSL umbrella checkout") still open. No successor
document exists and no evidence surfaced during this backfill that the manual's
commands or directory map are stale.

## Related documents

- [README.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/README.md) — repo intro + taxonomy entry point
- [ARCHITECTURE_REVIEW.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/ARCHITECTURE_REVIEW.md) — findings + roadmap
- [docs/cleanup/taxonomy_summary.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/docs/cleanup/taxonomy_summary.md) — cleanup state
- [csl-corrections/docs/correction-workflow.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md) — canonical correction workflow

## Revision history

| Date | Change | By |
|---|---|---|
| 11-07-2026 | Initial version (H506): cheat-sheet, data-flow, 14 directory walkthroughs, new-dict flow, load-bearing verdicts, symptom table, glossary, maintainer appendix | Fable 5 (`claude-fable-5`) |
| 11-07-2026 | template v2 backfill (H663) | Sonnet 5 (`claude-sonnet-5`) |

_Dr. Mārcis Gasūns_
