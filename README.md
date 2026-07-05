# COLOGNE

_Created: 14-01-2014 · Last updated: 05-07-2026_

The Cologne Digital Sanskrit Dictionaries (CDSL) project has been accumulating
build tooling, one-off scripts, generated reports, and issue-tracked
proposals since 2014 — long enough that nobody can say offhand which files
are load-bearing infrastructure, which are dead prototypes, and which are
stale reports nobody regenerates anymore. **COLOGNE is the project's
build-meta repository**: it holds the cross-cutting tooling, architecture
review, and (as of this pass) a non-destructive **cleanup taxonomy** that
classifies every file in the repo — active tooling vs. generated report vs.
archival issue-work vs. prototype vs. legacy — so a maintainer can approve,
override, defer, or ignore each classification before anything gets moved or
deleted.

Nothing is auto-deleted by this workflow. The taxonomy proposer only reads
the tree and writes a CSV with `human_decision` left blank; a human (or an
agent under his instruction) fills that column before any cleanup PR happens.

## Cleanup planning

- [ARCHITECTURE_REVIEW.md](ARCHITECTURE_REVIEW.md) — architecture review and roadmap
- [docs/cleanup/taxonomy_schema.md](docs/cleanup/taxonomy_schema.md) — the classification schema
- [docs/cleanup/taxonomy_summary.md](docs/cleanup/taxonomy_summary.md) — summary of proposals
- [docs/cleanup/taxonomy_proposals.csv](docs/cleanup/taxonomy_proposals.csv) — per-file approval CSV
- [docs/cleanup/cleanup_issue_backlog.md](docs/cleanup/cleanup_issue_backlog.md) — proposed cleanup issue backlog

## Usage example — executed, real output

Regenerating the taxonomy proposal is a single command, run for real against
this repo's current tree while writing this README:

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

480 files classified in one pass. The generated CSV leaves `human_decision`
and `human_notes` blank so a maintainer can approve, override, defer, or
ignore each proposed classification — this verification run's output was
discarded (`git checkout`) afterward, so writing this README would not
silently alter the repo's tracked cleanup state as a side effect.

## Issues overview

**Total**: 100 | **Open**: 71 | **Closed**: 29

| Milestone | Open | Closed | Total |
|---|---|---|---|
| Unassigned | 71 | 29 | 100 |

By type: enhancement 67 · question 14 · bug 8 · performance 1.
By severity: minor 59 · trivial 21.

## GitHub issue conventions

Follows the [Cologne tooling-repo taxonomy](https://github.com/sanskrit-lexicon/csl-observatory/blob/main/runbook/cologne-tooling-runbook.md):

- **9 type labels**: bug, feature, enhancement, performance, tech-debt, security, documentation, infrastructure, question
- **4 severity levels**: trivial, minor, major, critical
- **5 milestones**: API Stability, User Experience, Data Quality, Developer Experience, Community
- **Org Project**: [Tooling Roadmap](https://github.com/orgs/sanskrit-lexicon/projects/9)

See [CLAUDE.md](CLAUDE.md) for full definitions.

---

_Dr. Mārcis Gasūns_
