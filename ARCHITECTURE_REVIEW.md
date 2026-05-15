# COLOGNE Code and Architecture Review

Reviewed: 2026-05-15

## Executive Summary

This repository is best understood as a historical and operational toolkit for the Cologne Digital Sanskrit Dictionaries, not as a single deployable application. Its strongest assets are domain-specific scripts for dictionary digitization analysis, transliteration, correction application, Markdown export, StarDict/Babylon export, and issue-specific data repair work.

The main architectural risk is that reusable logic has not been separated from issue workspaces. Many scripts are copied across issue directories, dependency and runtime expectations are implicit, and there is no automated test or CI layer to catch regressions. The result is a repo with valuable specialist knowledge but uneven maintainability.

The recommended future direction is incremental: preserve the issue folders as historical records, extract shared reusable utilities into a small package, add dependency manifests and smoke tests, then modernize the most-used scripts one workflow at a time.

## Review Scope

Inspected areas:

- Repository structure, documentation, and git state.
- Core scripts in `iast/`, `xmltag/`, `eascii/`, `enhancements/code/`, `makemd/`, and `stardict/`.
- Representative issue workspaces under `issues/`, including the Flask prototype in `issues/issue445/`.
- Shell workflows for batch dictionary processing and local setup.
- Python syntax compatibility, external dependencies, duplicated files, and test/CI presence.

Lightweight checks run:

- Counted file types and executable surfaces.
- Parsed all 127 Python files with Python 3.14 AST parsing.
- Searched for dependency, test, security, runtime, and CLI patterns.
- Checked availability of external Python dependencies in the current environment.
- Compared duplicated script copies and tested the transliterator path behavior without modifying source files.

## Findings

### P1. Several committed Python scripts do not parse under Python 3

Evidence:

- `enhancements/code/updateByLine_python2.py`
- `enhancements/issue10/levenshtein.py`
- `enhancements/issue10/suggest.py`
- `stardict/make_babylon.py`

The syntax check reported four `SyntaxError` failures, mostly Python 2 `print` statements and `xrange` usage. This is already documented for `stardict/make_babylon.py`, but the repo does not separate Python 2-only scripts from Python 3 scripts in tooling or metadata.

Impact:

- A developer running "all scripts" or future CI under Python 3 will fail immediately.
- The StarDict/Babylon workflow is effectively legacy-only unless a Python 2 environment is maintained.
- The autocomplete/suggestion utilities in `enhancements/issue10/` are not usable with the current default Python.

Recommendation:

- Add a compatibility inventory: `python3`, `python2-legacy`, and `archival`.
- Port or retire the Python 2 scripts, starting with `stardict/make_babylon.py` if StarDict output is still needed.
- Add a Python 3 syntax smoke test that excludes explicitly legacy files.

### P1. The transliterator has a broken default data path and duplicated divergent copies

Evidence:

- `iast/transcoder.py` initializes `transcoder_dir` to the repo parent plus `data/transcoder` at lines 45-47, but the XML files live in `iast/`.
- `iast/slp1_iast.py` compensates by calling `transcoder.transcoder_set_dir('')` at line 9, which only works when the current directory is `iast/`.
- `stardict/transcoder.py` initializes its path to `stardict/data/transcoder` at lines 41-42, but that directory and the XML files are not present.
- `stardict/make_babylon.py` imports `stardict/transcoder.py` but never sets a valid transcoder directory.

Local behavior observed:

- Importing `iast/transcoder.py` from the repo root leaves `rAma` unchanged for `slp1 -> roman`.
- After explicitly setting the directory to `iast/`, `rAma` becomes the expected IAST long-a form (`r\u0101ma`).
- Importing `stardict/transcoder.py` leaves `rAma` unchanged for `slp1 -> deva`.

Impact:

- Transliteration silently falls back to returning the original string when the XML file is not found.
- The StarDict generator can produce incorrectly transliterated output without failing loudly.
- Divergent copies make fixes easy to apply in one place but not the other.

Recommendation:

- Make missing transliteration XML a hard error unless the caller explicitly opts into passthrough.
- Consolidate `iast/transcoder.py` and `stardict/transcoder.py` into one shared module.
- Resolve data files relative to the module by default, or package the XML mappings as package data.

### P1. The Flask API prototype is not safe or scalable as a service boundary

Evidence:

- `issues/issue445/serve_api.py` enables CORS for every route at line 12.
- It fetches all rows from SQLite on every search at lines 46-48, then filters in Python with user-provided regexes at lines 51-58.
- Invalid regex errors are not handled, because only `sqlite3.Error` is caught at lines 64-65.
- The server runs with `debug=True` at line 94.
- Database and table names are hardcoded at lines 16-17.

Impact:

- Large dictionaries will force full-table scans and high memory use per request.
- User-provided regexes can crash a request or consume excessive CPU.
- Debug mode and blanket CORS are unsuitable outside local experiments.
- The prototype is tightly bound to one table name and cannot naturally support multiple dictionaries.

Recommendation:

- Treat `issues/issue445/` as prototype code, not production architecture.
- If this API is revived, move it into a proper app package with configuration, bounded search, regex validation/timeouts, pagination, SQLite indexes or FTS, and production-safe CORS/debug settings.
- Add API tests for empty queries, invalid regexes, large results, and missing files.

### P1. Dependency and environment setup is implicit

Evidence:

- No `requirements.txt`, `pyproject.toml`, `setup.py`, `environment.yml`, or CI workflow files were found.
- External imports include `lxml`, `indic_transliteration`, `flask`, `flask_restx`, and `flask_cors`.
- In the current environment, `lxml` and `indic_transliteration` are available, while `flask`, `flask_restx`, and `flask_cors` are missing.

Impact:

- New contributors cannot reliably reproduce working environments.
- Scripts fail late, at import time, instead of being grouped by optional feature set.
- It is unclear which Python versions each workflow supports.

Recommendation:

- Add a minimal `pyproject.toml` or `requirements.txt` with optional dependency groups such as `api`, `markdown`, and `xmlvalidate`.
- Add `README` setup examples using a virtual environment.
- Add a `scripts/check_env.py` helper that reports which workflows are available.

### P2. Reusable issue-processing logic is copied across many issue directories

Evidence:

- Identical file hashes appear across `issues/issue422` through `issues/issue432`, including `frontback.py`, `infotag.py`, `info_end.py`, `middle.py`, and `digentry.py`.
- Other duplicated families include `k2_paren.py`, `hwextra_adj.py`, `k1k2_change.py`, `convert_hwextra_lbody.py`, and `updateByLine.py`.

Impact:

- Bugs fixed in one issue copy will remain in other copies.
- It is hard to know which copy is canonical.
- Review and test effort scales with duplication rather than behavior.

Recommendation:

- Preserve existing issue folders as archival snapshots.
- Create a shared `cologne_tools/` package for reusable parsing, entry splitting, metaline handling, line-change application, and tag analysis.
- For future issue work, use thin issue-specific scripts that import shared utilities.

### P2. There is no automated test suite or CI safety net

Evidence:

- No `tests/` or `.github/workflows/` directory was found.
- Search found assertions embedded in scripts, but no runnable test harness.
- Core behavior such as `updateByLine`, tag counting, extended Unicode counting, transliteration, and Markdown export has no automated regression coverage.

Impact:

- Domain-specific transformations can regress silently.
- Python version upgrades are risky.
- Refactoring duplicated code is harder than it needs to be.

Recommendation:

- Start with golden-file tests for the stable utilities:
  - `updateByLine.py`
  - `xmltag.py`
  - `eascii/ea.py`
  - `iast/transcoder.py`
- Add a CI job that runs syntax checks, unit tests, and a few small CLI smoke tests.

### P2. Shell workflows assume fragile local layout and unverified downloads

Evidence:

- `xmltag/redo_one.sh` and `eascii/redo_one.sh` hardcode `../../../cologne/csl-orig/v02/...` at line 4.
- `enhancements/code/dictionary_init.sh` downloads over plain HTTP at lines 41, 44, and 47.
- The download script does not use checksum verification or `curl -fSL`.

Impact:

- Scripts break outside the original local directory structure.
- Failed downloads may still proceed to unzip.
- HTTP download and lack of checksums create supply-chain and reproducibility risk.

Recommendation:

- Accept `CSL_ORIG` or `--csl-orig` as configuration rather than hardcoding sibling paths.
- Switch downloads to HTTPS where available.
- Use `curl -fSL`, verify checksums or sizes, and fail fast before unzip.

### P2. XML and HTML handling mixes structured parsing with regex/string transforms

Evidence:

- `xmltag/xmltag.py` uses regex `<(.*?)>` at line 35 for tag discovery.
- `makemd/make_md.py` uses `ElementTree` parsing but removes `<body>` tags via string replacement at lines 55-58.
- `issues/issue445/frontend.html` injects transformed content with `$("#response").html(container)` at line 191.
- `issues/issue443/searchHighlight.js` builds regexes from raw input at line 79 and writes generated markup with `innerHTML` at lines 85-88.

Impact:

- Regex-based XML/HTML handling can miscount malformed tags or mishandle edge cases.
- Browser-side HTML insertion is acceptable for trusted local prototypes, but it is not safe as a public web path without sanitization.
- Search regexes can throw errors or become expensive for pathological input.

Recommendation:

- Keep regex scanners where the goal is approximate corpus analysis, but label them as scanners rather than validators.
- Use structured parsing for canonical transformations.
- Escape or sanitize browser-rendered data, and distinguish literal search from regex search in UI/API design.

### P3. CLI ergonomics are thin

Evidence:

- Many scripts read positional `sys.argv` values directly without length checks or help, for example `makemd/make_md.py` at line 121 and `enhancements/code/updateByLine.py` at lines 159-161.
- Several scripts assume they are run from their containing directory.

Impact:

- User errors become stack traces.
- Scripts are hard to compose from automation or CI.

Recommendation:

- Add `argparse` to active scripts.
- Resolve paths relative to explicit arguments or module location.
- Standardize exit codes and error messages.

## Architecture Assessment

### What Works Well

- The repository captures years of domain knowledge in scripts and issue workspaces.
- The text processing model is direct and inspectable, which is useful for scholarly corpus maintenance.
- `updateByLine.py` has a good safety concept: change records include the expected old line, so mismatches stop the update.
- The `iast/` XML mapping approach gives a clear source of truth for transliteration.
- Documentation is better than the average scripts repo; `README.md`, `CLAUDE.md`, and folder readmes explain the historical workflows.

### Main Architectural Gaps

- No clear boundary between maintained tools, prototypes, generated reports, and archival issue code.
- No package/module layout for shared code.
- No dependency manifest or test harness.
- Environment assumptions are local and implicit.
- Some failures are silent, especially transliteration XML lookup.

### Suggested Target Shape

```text
COLOGNE/
  cologne_tools/
    transliteration/
    digitization/
    corrections/
    scanners/
    exports/
  scripts/
    xmltag
    eascii
    update-by-line
    make-md
  tests/
    fixtures/
  issues/
    issueNNN/        # archival and experiment work remains here
  docs/
    architecture.md
    workflows.md
```

This target shape does not require a disruptive rewrite. It gives future work a stable place to live while preserving the current historical record.

## Roadmap

### Phase 1: Stabilize and Inventory

- Add a compatibility matrix for every script: Python version, dependencies, inputs, outputs, and status.
- Add `requirements.txt` or `pyproject.toml` with optional dependency groups.
- Add a Python 3 syntax check that excludes files marked `python2-legacy`.
- Make missing transliteration XML fail loudly.
- Document the expected sibling repository layout and add environment-variable overrides.

### Phase 2: Add Tests Around Current Behavior

- Add small fixtures for metalines, entries, Unicode characters, XML-like tags, and change transactions.
- Test `updateByLine.py` for `new`, `ins`, `del`, old-line mismatch, odd transaction counts, and out-of-range lines.
- Test `xmltag.py` and `eascii/ea.py` on small dictionary samples.
- Test `iast/transcoder.py` with representative `slp1`, `roman`, and `deva` cases.
- Add CI for syntax and tests.

### Phase 3: Extract Shared Utilities

- Create `cologne_tools` with reusable entry parsing and file IO helpers.
- Move duplicate issue helpers into shared modules after tests exist.
- Keep issue folders as reproducible snapshots, but make new issue scripts thin wrappers.
- Replace copied `updateByLine.py` instances with imports or documented archival status.

### Phase 4: Modernize Active Workflows

- Port `stardict/make_babylon.py` to Python 3 or mark the StarDict workflow retired.
- Add `argparse` CLIs for active tools.
- Replace hardcoded relative paths with CLI flags and environment variables.
- Add structured logging for batch runs.
- Switch cloud downloads to HTTPS and verified artifacts.

### Phase 5: Productize Only If Needed

- If the Flask API becomes an active direction, move it out of `issues/` into an app package.
- Use configuration per dictionary, indexed search, pagination, and bounded regex/literal search modes.
- Add production settings for CORS, debug mode, error handling, and deployment.
- Add frontend sanitization and UI tests before exposing it beyond local use.

## Suggested Near-Term Backlog

1. Create a script inventory table in `docs/script_inventory.md`.
2. Add `pyproject.toml` or `requirements.txt` with optional extras.
3. Add a `tests/fixtures/mini_dict.txt` sample and tests for `updateByLine`, `xmltag`, and `eascii`.
4. Fix `iast/transcoder.py` default XML lookup and remove the duplicate `stardict/transcoder.py`.
5. Decide whether `stardict/make_babylon.py` is still active; port it or mark it legacy.
6. Add CI for Python 3 syntax and tests.
7. Introduce shared `cologne_tools` modules for duplicated issue utilities.

## Residual Risks

- This review did not run full dictionary batch workflows because the sibling data repositories are not present in this workspace.
- Some issue directories are historical experiments; not every prototype should be modernized.
- The most important next decision is ownership: which workflows are active, which are archival, and which can be retired.
