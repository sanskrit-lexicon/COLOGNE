# Changelog

All notable changes to the COLOGNE build-meta repository are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). This repo has no
version tags to date; entries accumulate under Unreleased until the maintainers
choose to cut a first release.

## [Unreleased]

## [0.1.0] - 2026-08-30
### Fixed

- **CodeQL workflow triggers** (H1522 / H1245 find): [`.github/workflows/codeql.yml`](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/.github/workflows/codeql.yml) push/PR branches were `master` while the default branch is `main`, so PR-time CodeQL never fired (only the weekly cron). Triggers now target `main`.

### Changed

- `docs/TOOLING_MANUAL.md` estate refresh (H1245, 18-07-2026): fact-check recounts
  against the live tree (`issues/` 265 files not 270; `xmltag/catall.sh` 36 codes
  not 34, the 8 missing codes named; `stardict/redo.sh` 36 not 37; eascii output
  format), an executed `updateByLine.py` worked example (apply + stop-on-mismatch),
  an engine-verification pattern for checkouts without the `cologne/` umbrella
  layout, and a `DeprecationWarning` symptom row. Companion
  `docs/TOOLING_MANUAL.meta.md` gains a `LAST_VERIFIED` verification block
  (6 commands spot-run), a reconciled backlog, and a consolidation verdict.
