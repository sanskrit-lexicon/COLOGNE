# COLOGNE

_Created: 14-01-2014 · Last updated: 11-07-2026_

The Cologne Digital Sanskrit Dictionaries (CDSL) project has been accumulating
build tooling, one-off scripts, generated reports, and issue-tracked
proposals since 2014 — long enough that nobody can say offhand which files
are load-bearing infrastructure, which are dead prototypes, and which are
stale reports nobody regenerates anymore. **COLOGNE is the project's
build-meta repository**: it holds the cross-cutting tooling, architecture
review, and a non-destructive **cleanup taxonomy** that classifies every file
in the repo — active tooling vs. generated report vs. archival issue-work vs.
prototype vs. legacy — so a maintainer can approve, override, defer, or ignore
each classification before anything gets moved or deleted.

Nothing is auto-deleted by this workflow. The taxonomy proposer only reads
the tree and writes a CSV with `human_decision` left blank; a human (or an
agent under his instruction) fills that column before any cleanup PR happens.

## Operator manual

[docs/TOOLING_MANUAL.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/docs/TOOLING_MANUAL.md)
is the detailed operator manual for every tooling directory in this repo — cheat-sheet,
data-flow, per-directory walkthroughs with exact commands, the add-a-new-dictionary
flow, load-bearing vs legacy verdicts, and a symptom → cause → cure table. Its
improvement backlog lives in
[docs/TOOLING_MANUAL.meta.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/docs/TOOLING_MANUAL.meta.md).

## Cleanup planning

- [ARCHITECTURE_REVIEW.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/ARCHITECTURE_REVIEW.md) — architecture review and roadmap
- [docs/cleanup/taxonomy_schema.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/docs/cleanup/taxonomy_schema.md) — the classification schema
- [docs/cleanup/taxonomy_summary.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/docs/cleanup/taxonomy_summary.md) — summary of proposals
- [docs/cleanup/taxonomy_proposals.csv](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/docs/cleanup/taxonomy_proposals.csv) — per-file approval CSV
- [docs/cleanup/cleanup_issue_backlog.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/docs/cleanup/cleanup_issue_backlog.md) — proposed cleanup issue backlog

## Usage example — executed, real output

Regenerating the taxonomy proposal is a single command, run for real against
this repo's current tree while writing this README
([tools/propose_cleanup_taxonomy.py](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/tools/propose_cleanup_taxonomy.py)):

```bash
python tools/propose_cleanup_taxonomy.py
```

Actual output:

```
Wrote 480 proposals to C:\Users\user\Documents\GitHub\COLOGNE\docs\cleanup
- C:\Users\user\Documents\GitHub\COLOGNE\docs\cleanup\taxonomy_schema.md
- C:\Users\user\Documents\GitHub\COLOGNE\docs\cleanup\taxonomy_summary.md
- C:\Users\user\Documents\GitHub\COLOGNE\docs\cleanup\taxonomy_proposals.csv
- C:\Users\user\Documents\GitHub\COLOGNE\docs\cleanup\cleanup_issue_backlog.md
```

The generated CSV holds one classified row per scanned file (464 data rows in
the current tree) and leaves `human_decision` and `human_notes` blank so a
maintainer can approve, override, defer, or ignore each proposed
classification — this verification run's output was discarded (`git checkout`)
afterward, so writing this README would not silently alter the repo's tracked
cleanup state as a side effect.

## Issues overview

As of 11-07-2026 (live counts via the GitHub API):

| State | Issues |
|---|---|
| Open | 199 |
| Closed | 259 |
| Total | 458 |

The full, always-current list is on the
[issue tracker](https://github.com/sanskrit-lexicon/COLOGNE/issues). Per-label
and per-milestone breakdowns are intentionally not hardcoded here — they drift
faster than a README can be maintained; filter the live tracker instead.

## GitHub issue conventions

This build-meta repo follows the
[Cologne tooling-repo taxonomy](https://github.com/sanskrit-lexicon/csl-observatory/blob/main/runbook/cologne-tooling-runbook.md)
for new issues (type + severity + milestone labels). Some older issues still
carry legacy dictionary-style labels (`link-target`, `markup`, `scan-quality`,
`text-correction`, …) from before this repo was recategorized; those are
migrated opportunistically rather than in a bulk relabel. The org-level
[Tooling Roadmap](https://github.com/orgs/sanskrit-lexicon/projects/9) project
tracks tool work across all repositories.

See [CLAUDE.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/CLAUDE.md)
for the full label and milestone definitions.

## Correcting dictionary source text

COLOGNE holds build tooling, not the dictionary source files themselves.
Corrections to the actual dictionary text (in `csl-orig`) are never made by
hand-editing source — they go through the change-file workflow documented
canonically in
[csl-corrections/docs/correction-workflow.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md).

---

_Dr. Mārcis Gasūns_
