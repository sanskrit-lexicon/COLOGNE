_Created: 15-05-2026 · Last updated: 05-09-2026_

# Sanskrit Lexicon — Contribution Standard

This is the **org-wide** contribution standard for all repositories under [sanskrit-lexicon](https://github.com/sanskrit-lexicon). Individual repos may extend this in their own `CONTRIBUTING.md`, but must not contradict it.

## Repository categories

| Category | Examples | Issue taxonomy |
|---|---|---|
| Dictionary | PWG, MWS, AP90, PWK, GRA, FRI, MD, … | Dictionary taxonomy (9 type labels, 3 severity, 4 milestones) |
| Tooling | csl-pywork, csl-app, csl-orig | Tooling taxonomy (9 type labels, 4 severity, 5 milestones) |
| Meta | csl-corrections, csl-observatory, COLOGNE | Either, by scope |

## Issue taxonomy — dictionary repos

**Type** (exactly one, `#0075ca`): `link-target`, `link-splitting`, `markup`, `text-correction`, `content-enhancement`, `encoding`, `scan-quality`, `bug`, `question`

**Severity** (exactly one): `minor` `#e4e669`, `medium` `#fbca04`, `hard` `#d93f0b`

**Milestone** (one): Dictionary to Book, Digitization Quality, Structured Data, Major Enhancements

## Issue taxonomy — tooling repos

**Type** (exactly one): `bug`, `feature`, `enhancement`, `performance`, `tech-debt`, `security`, `documentation`, `infrastructure`, `question`

**Severity**: `trivial`, `minor`, `major`, `critical`

**Milestone**: API Stability, User Experience, Data Quality, Developer Experience, Community

## Pull requests

1. Fork → feature branch → PR.
2. Reference the issue number in the PR title or body.
3. Keep PRs focused: one logical change per PR.
4. PR will not be merged without at least one approval from a maintainer.

## Source-file edits

Dictionary source files (`*.xml`, `*.txt` under `csl-orig`) are **never edited directly**. Corrections are expressed as change files applied by scripts (`updateByLine.py` pattern — see the relevant `CLAUDE.md`).

## Code of Conduct

All contributors follow the Contributor Covenant 2.1 — see `CODE_OF_CONDUCT.md` in each repo.

## Acknowledgements & credit

- ≤ 2 commits / minor PRs → listed in `data/people.yaml` (where applicable) or repo contributors
- ≥ 3 commits or a non-trivial component → named in release notes / paper acknowledgements
- Substantial intellectual contribution to a paper → co-authorship (judgment call by project lead in consultation with maintainers)

## Questions

- Repo-specific: open an issue in that repo
- Cross-repo / project-wide: open an issue in [COLOGNE](https://github.com/sanskrit-lexicon/COLOGNE/issues)
- Direct contact: gasyoun@gmail.com (project lead)

_Dr. Mārcis Gasūns_
