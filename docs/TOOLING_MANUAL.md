# COLOGNE cross-cutting tooling — operator manual

_Created: 11-07-2026 · Last updated: 11-07-2026_

This is the operator manual for the [COLOGNE](https://github.com/sanskrit-lexicon/COLOGNE)
build-meta repository of the Cologne Digital Sanskrit Lexicon (CDSL) project. The test
this document sets itself: **a newcomer can run every live workflow in this repo from
this manual alone, without reading the source code.**

Three documents describe this repo, with different jobs — not three parallel truths:

- **What the repo is + the cleanup-taxonomy entry point** —
  [README.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/README.md);
- **Code-quality findings + modernization roadmap** —
  [ARCHITECTURE_REVIEW.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/ARCHITECTURE_REVIEW.md);
- **How to actually operate each tool** — this manual.

Corrections to dictionary source text are out of scope here: they follow the canonical
change-file workflow in
[csl-corrections/docs/correction-workflow.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md)
(this manual only documents the local engine, `updateByLine.py`, that the workflow uses).

---

## Cheat-sheet: the whole repo on one screen

Each row links to its detailed section below. "Status" is the load-bearing verdict
(details in [Load-bearing vs legacy](#load-bearing-vs-legacy--the-explicit-verdicts)).

| Directory | What it does | Canonical command | Status |
|---|---|---|---|
| [tools/](https://github.com/sanskrit-lexicon/COLOGNE/tree/main/tools) | classify all repo files for cleanup (proposal-only) | `python tools/propose_cleanup_taxonomy.py` (repo root) | 🟢 active, headline tool |
| [enhancements/code/](https://github.com/sanskrit-lexicon/COLOGNE/tree/main/enhancements/code) | apply change-files to digitizations; XML-validate; encoding helpers | `python updateByLine.py OLDFILE CHGFILE NEWFILE` | 🟢 active core |
| [eascii/](https://github.com/sanskrit-lexicon/COLOGNE/tree/main/eascii) | census of non-ASCII characters per dictionary | `sh redo_one.sh xxx` (from `eascii/`) | 🟢 active audit |
| [xmltag/](https://github.com/sanskrit-lexicon/COLOGNE/tree/main/xmltag) | census of XML tags per dictionary; `<chg>` extraction | `sh redo_one.sh xxx` (from `xmltag/`) | 🟢 active audit |
| [iast/](https://github.com/sanskrit-lexicon/COLOGNE/tree/main/iast) | SLP1⇄IAST transcode tables — **source of truth for the live site** | `python slp1_iast.py slp1_roman.xml slp1_iast.txt` (from `iast/`) | 🟢 canonical asset |
| [makemd/](https://github.com/sanskrit-lexicon/COLOGNE/tree/main/makemd) | export a dictionary XML to per-headword Markdown (Hugo) | `python3 make_md.py dictcode` (from `makemd/`) | 🟡 runnable, needs sibling tree |
| [localinstall/](https://github.com/sanskrit-lexicon/COLOGNE/tree/main/localinstall) | run the whole CDSL site locally (Windows/Mac) | `sh download2.sh dictcode` (Mac) · XAMPP runbook (Windows) | 🟢 active runbooks |
| [stardict/](https://github.com/sanskrit-lexicon/COLOGNE/tree/main/stardict) | export dictionaries to StarDict/Babylon format | `python2 make_babylon.py ../../Cologne_localcopy md` | 🔴 legacy Python 2, broken traps |
| [api/](https://github.com/sanskrit-lexicon/COLOGNE/tree/main/api) | REST-API URL design spec (2020) | none — paper spec, not code | 🟡 design doc |
| [aws/](https://github.com/sanskrit-lexicon/COLOGNE/tree/main/aws) | S3 upload notes (2014) + bucket manifests | none — archival + inventories | 🟡 manifests useful |
| [enhancements/autocomplete/](https://github.com/sanskrit-lexicon/COLOGNE/tree/main/enhancements/autocomplete) | headword autocomplete data generator | `python listsanhw1.py` | 🟡 data ships, script legacy |
| [enhancements/issue10/](https://github.com/sanskrit-lexicon/COLOGNE/tree/main/enhancements/issue10) | spelling-suggestion prototype | `python2 suggest.py inputword` | 🔴 legacy Python 2 |
| [issues/](https://github.com/sanskrit-lexicon/COLOGNE/tree/main/issues) | per-issue archival workspaces (270 files) | none — archival; exception: issue445 | ⚪ archival |
| [xsswork/](https://github.com/sanskrit-lexicon/COLOGNE/tree/main/xsswork) | 2022 XSS-hardening notes | none — memo | ⚪ archival |
| [misc/](https://github.com/sanskrit-lexicon/COLOGNE/tree/main/misc) | scholarly reference artifacts | none — reference | ⚪ archival |

The add-a-new-dictionary flow (spanning five sibling repos) has
[its own section](#adding-a-new-dictionary-to-cdsl) below.

## Data flow

```
                         sibling repos / trees (NOT in COLOGNE)
        ┌────────────────────────────────────────────────────────────────┐
        │ csl-orig/v02/<xxx>/<xxx>.txt        (dictionary digitizations) │
        │ <dictcode>/pywork/<dictcode>.xml    (pywork-built XML)         │
        │ Cologne_localcopy/<id>/<id>xml/xml/ (local XML mirror)         │
        └───────┬───────────────────┬──────────────────┬─────────────────┘
                │                   │                  │
   eascii/ea.py │      xmltag/xmltag.py     makemd/make_md.py   stardict/make_babylon.py
   (char census)│      (tag census)         (MD export)         (Babylon export, py2)
                ▼                   ▼                  ▼                  ▼
        eadata/ea_xxx.txt    xmltag_xxx.txt     MD/<dict>/*.md     output/<id>.babylon
        easummary*.tsv       all_xmltags.txt    (Hugo site feed)   (StarDict toolchain)
                                                                   [silent-translit trap]
   ────────────────────────────────────────────────────────────────────────────────
   corrections lane:  enhancements/code/updateByLine.py  OLDFILE + CHGFILE → NEWFILE
                      eascii/eachanges-degree/: make_change.py → updateByLine.py
                      → copy_orig.sh  (writes BACK into csl-orig — the mutating step)
   ────────────────────────────────────────────────────────────────────────────────
   live-site lane:    iast/slp1_roman.xml + roman_slp1.xml   (source of truth)
                      → install_local.sh → csl-apidev + csl-websanlexicon transcoder
                      dirs → the sanskrit-lexicon.uni-koeln.de displays
   ────────────────────────────────────────────────────────────────────────────────
   governance lane:   tools/propose_cleanup_taxonomy.py → docs/cleanup/*  (4 files,
                      human_decision loop; nothing moves until a human decides)
```

## Environment & prerequisites

**Directory layout assumption (load-bearing).** Nearly every runnable script assumes
COLOGNE is checked out inside a `cologne/` umbrella directory that also holds the data
repo [csl-orig](https://github.com/sanskrit-lexicon/csl-orig) and (for `iast/`) the PHP
repos [csl-apidev](https://github.com/sanskrit-lexicon/csl-apidev) and
[csl-websanlexicon](https://github.com/sanskrit-lexicon/csl-websanlexicon). The
canonical local layout is the Windows XAMPP tree `C:\xampp\htdocs\cologne\` (this is
what `install_local.sh` and the `../../../cologne/csl-orig/...` relative paths in the
`redo_*.sh` drivers expect). In a bare GitHub checkout without those siblings, every
`redo_*` driver fails on input paths — that is layout, not a bug.

**Python version split** (per-script; there is no repo-wide interpreter):

| Tool | Interpreter | Evidence |
|---|---|---|
| `tools/propose_cleanup_taxonomy.py` | Python ≥ 3.9 | uses `Path.is_relative_to`; stdlib only |
| `eascii/*.py` | Python 3.7+ | `sys.stdout.reconfigure(encoding='utf-8')` |
| `xmltag/*.py` | Python 2 or 3 | version-agnostic stdlib |
| `iast/slp1_iast.py`, `iast/transcoder.py` | Python 2 or 3 | dual-version by design |
| `makemd/make_md.py` | Python 3 | needs pip package `indic_transliteration` |
| `enhancements/code/updateByLine.py` | Python 3 | (`updateByLine_python2.py` is the py2 twin) |
| `enhancements/code/xmlvalidate.py` | Python 2.7 + `lxml` | Windows stand-in for `xmllint` |
| `stardict/make_babylon.py`, `stardict/transcoder.py` | **Python 2 only** | `print` statements, `xrange` — SyntaxError under py3 |
| `enhancements/issue10/*.py` | **Python 2 only** | same |
| `aws/awsintro.txt` procedure | Python 2.6/2.7 + `awscli` | 2014 host setup, archival |

There is no `requirements.txt`/`pyproject.toml` yet (a known
[ARCHITECTURE_REVIEW.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/ARCHITECTURE_REVIEW.md)
P1). Third-party packages actually imported anywhere: `lxml`,
`indic_transliteration`, and (issue445 prototype only) `flask`, `flask_restx`,
`flask_cors`.

**External tools** by workflow: `curl` + `unzip` (localinstall downloads), Apache +
PHP + `mod_rewrite` (localinstall serving), XAMPP + `mako` + `sqlite3` + `zip`
(Windows source-build), Homebrew + `ant` + `php` + libphp code-signing (Mac), `pdftk`
(new-dictionary scan splitting), the StarDict toolchain `stardict-editor`/`dictzip`
(consuming `.babylon` files — not in this repo).

**Windows encoding gotcha.** The `sys.stdout.reconfigure(encoding='utf-8')` lines in
`eascii/` exist to survive git-bash on Windows, which otherwise crashes with
`UnicodeEncodeError: 'charmap' codec`. Do not remove them; add them to any new script
that prints Sanskrit.

---

## Directory walkthroughs

### tools/ — the cleanup taxonomy (governance, proposal-only)

**When to reach for it:** you want to know what any file in this repo *is* (active
tooling vs generated report vs archival issue-work vs prototype vs legacy), or you are
regenerating the cleanup proposal after the tree changed.

**Run (from the repo root):**

```bash
python tools/propose_cleanup_taxonomy.py
# options: --root . --out-dir docs/cleanup
```

[tools/propose_cleanup_taxonomy.py](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/tools/propose_cleanup_taxonomy.py)
scans the whole tree (skipping `.git`, `__pycache__`, and its own output dir),
SHA-256-hashes every file to find byte-identical duplicates, AST-parses every `.py`
under Python 3 to detect Python-2-only scripts mechanically, and classifies each file
on three axes — 9 lifecycle labels × 13 workflow labels × 9 proposed actions — plus
risk and confidence. It **never moves, deletes, or rewrites** anything.

It writes four files into
[docs/cleanup/](https://github.com/sanskrit-lexicon/COLOGNE/tree/main/docs/cleanup):

1. [taxonomy_schema.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/docs/cleanup/taxonomy_schema.md) — the label glossary;
2. [taxonomy_proposals.csv](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/docs/cleanup/taxonomy_proposals.csv) — one row per file (464 rows currently), `human_decision`/`human_notes` left **blank**;
3. [taxonomy_summary.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/docs/cleanup/taxonomy_summary.md) — totals + the 6-group Human Approval Queue;
4. [cleanup_issue_backlog.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/docs/cleanup/cleanup_issue_backlog.md) — 9 pre-drafted cleanup issues.

**The human loop:** a maintainer fills `human_decision` per row with `approve`,
`override`, `defer`, or `ignore` (+ free-text `human_notes`). As of 11-07-2026, 0 of
464 rows are decided; nothing may be moved or deleted before decisions land, and even
then the change goes through issues opened from the backlog doc — never directly from
the proposal.

**Trap:** running the tool rewrites the four *tracked* files under `docs/cleanup/`. If
you run it only to verify it works, discard the diff afterwards (`git checkout --
docs/cleanup`), as the README's own recorded verification run did — otherwise you
silently reset the (eventually human-annotated) committed state.

### enhancements/code/ — the correction engine and friends

Documented in
[enhancements/code/readme.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/enhancements/code/readme.md).
This is the shared core of the Cologne correction machinery.

- [updateByLine.py](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/enhancements/code/updateByLine.py) —
  **the primary correction applier.**

  ```bash
  python updateByLine.py OLDFILE CHGFILE NEWFILE
  ```

  Applies a change-file to a digitization. A change-file is a sequence of
  two-line transactions: an `old` verification line (`NNN old text…`) paired with a
  `new`/`ins`/`del` action line; lines starting `;` are comments; everything UTF-8.
  Safety property worth knowing: **if the `old` text does not byte-match the current
  line in OLDFILE, the run stops** — mismatches never get silently applied. The full
  8-stage workflow around this engine (snapshot → apply → promote → regenerate →
  validate → audit → commit → refresh) is canonical in
  [csl-corrections/docs/correction-workflow.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md);
  do not re-derive it from here.

- [updateByLine_python2.py](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/enhancements/code/updateByLine_python2.py) —
  the Python-2 legacy twin. Do not use for new work.
- [xmlvalidate.py](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/enhancements/code/xmlvalidate.py) —
  `python xmlvalidate.py file.xml file.dtd` — DTD validation on Windows where
  `xmllint` is unavailable (Python 2.7 + `lxml`).
- [dictionary_init.sh](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/enhancements/code/dictionary_init.sh) —
  `sh dictionary_init.sh mw` — downloads a per-dictionary working environment
  (orig / pywork / web) from the project's AWS blobs into a `cologne/` dir under the
  server path. ⚠️ Downloads over plain HTTP without checksums or `curl -fSL`
  fail-fast — a known hardening item; verify what you fetched before trusting it.
- [scanparse.py](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/enhancements/code/scanparse.py) —
  `python scanparse.py xxx_error.txt parse1.txt parse2.txt` — converts a
  CORRECTIONS-repo `xxx_error.txt` into `xxx_printchange.txt`-format scan-error lines.
- `cp1252_utf8.py` / `utf8_cp1252.py` / `unicode_dump.py` — one-shot encoding
  converters and a codepoint inspector.

### eascii/ — non-ASCII character census

**When to reach for it:** auditing which non-ASCII characters a dictionary's entries
actually use — the classic catch being MASCULINE ORDINAL INDICATOR `º` typed where
DEGREE SIGN `°` was meant.

**Run (from `eascii/`, with the `cologne/csl-orig` sibling in place):**

```bash
sh redo_one.sh mw          # one dictionary → eadata/ea_mw.txt
sh redo_all.sh             # all 36 dictionaries
sh catall.sh > all_ea.txt  # concatenate
python easummary.py ../../../cologne/csl-orig easummary        # cross-dict matrices
python easummary_meta.py ../../../cologne/csl-orig easummary_meta  # metaline-only
```

Output lines look like `° (°) 55614 := DEGREE SIGN`. Scripts only count
characters **inside entries** (from the `<L>` metaline to `<LEND>`), deliberately
excluding front matter. `easummary.py` splits Greek/Arabic/Cyrillic into separate
TSVs; `easummary_meta.py` examines only the `<L>` metalines and does **not** separate
Cyrillic — the two are intentionally different, not drifted copies.

**The nested correction campaign**
[eascii/eachanges-degree/](https://github.com/sanskrit-lexicon/COLOGNE/tree/main/eascii/eachanges-degree)
is a completed º→° fix across 13 dictionaries: `make_change.py` generated
change-files, `redo_changes.sh` applied them via `updateByLine.py` into `temporig/`,
and `copy_orig.sh` copied the results back over the live `csl-orig` digitizations —
that last script is the **data-mutating step** and takes no backup beyond git. Its
`log_changes.txt` is preserved as the audit trail (e.g. 21,109 instances in mw72).
Note the path depth: scripts here use `../../../../cologne/csl-orig/v02` (one more
`../` than `eascii/` itself).

### xmltag/ — XML-tag census

**When to reach for it:** markup-normalization auditing — which XML tags does each
dictionary actually use inside entries, and how often
(ref [issue #366](https://github.com/sanskrit-lexicon/COLOGNE/issues/366)).

**Run (from `xmltag/`):**

```bash
sh redo_one.sh mw               # → xmltag_mw.txt  (lines like "<HI1> 26982")
sh redo_all.sh                  # ~44 dictionary codes
sh catall.sh > all_xmltags.txt  # concatenate — but see the trap below
python chgtag.py ../../../cologne/csl-orig/v02/gra/gra.txt chgtag_gra.txt  # extract <chg>…</chg>
```

Counts opening/attributed/empty tags; closing tags, `<L>`/`<LEND>` metalines, and the
curly pseudo-tags `{#…#}` `{@…@}` `{%…%}` are deliberately out of scope. The scanner
is a line-based regex (`<(.*?)>`) — an approximate corpus scanner, not a validator.

**Trap:** `redo_all.sh` and `catall.sh` iterate **different** dictionary-code lists
(44 vs 34) — `catall.sh` concatenates fewer files than `redo_all.sh` generates. Check
both lists before trusting `all_xmltags.txt` as complete.

### iast/ — the transcoding source of truth

**What it is:** `slp1_roman.xml` and `roman_slp1.xml` here are, per
[iast/readme.txt](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/iast/readme.txt),
**the source of truth for the transliteration tables the live CDSL website uses**.
Editing them changes how the production displays transcode Sanskrit.

**Run (from `iast/` — the CWD matters, see trap):**

```bash
python slp1_iast.py slp1_roman.xml slp1_iast.txt
```

Regenerates the human-readable table `slp1_iast.txt` and runs three consistency
checks (IAST→SLP1 round-trip; SLP1 keysets match across the two XMLs; IAST keysets
match), printing `GOOD` or `WARNING` per check. Run this after **any** edit to either
XML.

**Install to the live PHP repos (Windows XAMPP layout only):**

```bash
sh install_local.sh
```

copies both XMLs into `csl-apidev/utilities/transcoder/` and
`csl-websanlexicon/v02/makotemplates/web/utilities/transcoder/` under
`/c/xampp/htdocs/cologne/`; you then commit and push those two repos yourself.

**Traps:**

- Three copies of each XML exist (here + two PHP repos) and are synced **by hand**;
  `slp1_iast.py`'s checks guard local consistency but nothing enforces parity with
  the installed copies. After editing, always run `install_local.sh` and push both
  consumers, or the site drifts from the source of truth.
- `slp1_iast.py` calls `transcoder.transcoder_set_dir('')`, which resolves the XML
  tables relative to the **current directory** — run it from anywhere but `iast/`
  and the transcoder loads nothing and *silently returns input unchanged* (the same
  silent-passthrough defect flagged as P1 in
  [ARCHITECTURE_REVIEW.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/ARCHITECTURE_REVIEW.md)).

### makemd/ — Markdown export for a Hugo site

**Run (from `makemd/`, Python 3, `pip install indic_transliteration`):**

```bash
python3 make_md.py snp
```

Reads the pywork-built XML from the **sibling tree** `../../snp/pywork/snp.xml` and
writes one Markdown file per headword to `MD/snp/`, named by the Devanagari form of
the headword (Hugo lowercases URLs, so SLP1/HK filenames would collide — Devanagari
avoids that). Each file carries YAML front-matter, the entry body, and links back to
the production `getword.php`/`servepdf.php` endpoints.

**Traps:** must be run from inside `makemd/` (hardcoded `../../` input path); bare
invocation without a dictcode is an unhandled `IndexError`; body extraction strips
`<body>` tags by string-replace, which breaks if the tag ever grows attributes.

### localinstall/ — running CDSL locally

Two maintained paths and one archive:

**Mac display-only (the light path —
[localinstall/mac/](https://github.com/sanskrit-lexicon/COLOGNE/tree/main/localinstall/mac)).**
Does **not** build from source and does not need csl-orig/csl-pywork/csl-websanlexicon
at all — it downloads prebuilt display bundles from the production server. One-time
setup per
[macCologneDictInstallation.txt](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/localinstall/mac/macCologneDictInstallation.txt):
Apache on, Homebrew, `brew install ant php`, wire libphp into
`/private/etc/apache2/httpd.conf` (with code-signing), enable `mod_rewrite` +
`AllowOverride All` for the `cologne/` docroot dir, install the
[.htaccess](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/localinstall/mac/.htaccess).
Then, from inside the served `cologne/` directory:

```bash
sh download2.sh mw        # one dictionary → cologne/mw/web/…
sh download2_all.sh       # all 38 codes
chmod -R 755 mw           # after each install
```

`download2.sh` fetches
`https://www.sanskrit-lexicon.uni-koeln.de/scans/{DICT}Scan/{year}/downloads/{dict}web1.zip`
and unzips it — so it hard-depends on the production server being up. Scan images
come separately: download the matching
[sanskrit-lexicon-scans](https://github.com/sanskrit-lexicon-scans) repo and move its
`pdfpages/` to `cologne/scans/{dict}/pdfpages`. Use `download2.sh`, not
`download1.sh` — the older script hardcodes `year=2020` and fails for `lrv` (2022).

**Windows source-build
([localinstall/xampp/](https://github.com/sanskrit-lexicon/COLOGNE/tree/main/localinstall/xampp)).**
The heavier path: install XAMPP, Python 3 (and copy `python.exe` → `python3.exe` so
`python3` resolves), `pip install mako`, GitBash, `sqlite3` on PATH, `zip` (GOW). Then
under `/c/xampp/htdocs`:

```bash
mkdir cologne sanskrit-lexicon-scans
cd cologne
git clone https://github.com/sanskrit-lexicon/csl-orig.git          # + csl-websanlexicon,
# csl-pywork, csl-apidev, csl-homepage, csl-doc — six sibling repos
cd csl-pywork/v02
sh generate_dict.sh md ../../md      # build one dictionary from source
sh redo_xampp_all.sh                 # or build everything
```

Homepage: `cd csl-homepage && sh update_version.sh && sh redo_xampp.sh`. Simple
search: drop the
[xampp/.htaccess](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/localinstall/xampp/.htaccess)
into `cologne/`. Note `generate_dict.sh`/`redo_xampp_all.sh` live in the sibling
[csl-pywork](https://github.com/sanskrit-lexicon/csl-pywork) repo, not here.

**Archive
([localinstall/mac1/](https://github.com/sanskrit-lexicon/COLOGNE/tree/main/localinstall/mac1)).**
Raw April-2023 install transcripts (brew/php/ant sessions, a stock `httpd.conf`
snapshot) kept as evidence; the runnable scripts there are copies of `mac/`.

**Traps:** CRLF line endings can break the download scripts if edited on Windows;
Safari cannot render the PDF scan pages (use Firefox); a `pcre.jit` PHP warning
appears in MW list displays until `;pcre.jit=1` is unset in `php.ini`; rerunning a
download into an existing `cologne/xxx` behaves oddly — remove the old dir first.

### stardict/ — Babylon/StarDict export (legacy, handle with care)

**Status: 🔴 Python-2-only legacy with two known silent traps.** Port or retire is the
standing recommendation
([ARCHITECTURE_REVIEW.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/ARCHITECTURE_REVIEW.md)
P1). If you must run it:

```bash
# Python 2 mandatory; lxml required; run from stardict/
mkdir -p output                                    # trap 1: output/ does not exist
# trap 2: supply the transcoder FSM tables (see below) or output is silently wrong
python2 make_babylon.py ../../Cologne_localcopy md # one dictionary
sh redo.sh                                         # all 37 codes
```

Reads `<pathToDicts>/<id>/<id>xml/xml/<id>.xml` from a local mirror named
`Cologne_localcopy` (a sibling directory, not in this repo) and writes
`output/<id>.babylon`, which the external StarDict toolchain
(`stardict-editor`/`dictzip`) then compiles. Per-dictionary cleanup quirks are
hardcoded inside the script.

**The silent-transliteration trap (P1):**
[stardict/transcoder.py](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/stardict/transcoder.py)
is a divergent copy of `iast/transcoder.py` that looks for its FSM XML tables in
`stardict/data/transcoder/` — **a directory that does not exist**. When the table
file is missing, the transcoder returns the input **unchanged instead of erroring**,
so `make_babylon.py` can produce entire `.babylon` files with raw SLP1 where
Devanagari was intended, and no error tells you. Before any real run, copy the needed
`slp1_deva.xml` (etc.) tables into `stardict/data/transcoder/` and spot-check the
output for Devanagari.

### api/ — REST API design spec (2020, not code)

Four Markdown files by Dhaval Patel specifying clean URLs (Apache `mod_rewrite`) over
the production PHP endpoints:
[getword.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/api/getword.md)
(entry detail),
[listhier.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/api/listhier.md)
(nearby headwords),
[servepdf.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/api/servepdf.md)
(scan page). Nothing here executes. Read them when designing API work against the
production site; know that every rewrite target hardcodes the `2020` display-tree
year, `listhier` is flagged broken for non-SLP1 input, and both getword and listhier
end in unresolved "Questions" sections — the spec was never finalized.

### aws/ — S3 upload notes and bucket manifests

[awsintro.txt](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/aws/awsintro.txt)
is Jim Funderburk's December-2014 log of pushing the scans to `s3://sanskrit-lexicon/`
(Python 2.6 virtualenv, `aws s3 cp … --acl public-read --recursive`) — archival; do
not imitate the setup. The durable value is the **manifests**: `aws_scans_list.txt`
(47,962 scan PDFs), `aws_scans_summary.txt` (per-dictionary PDF filename formats),
plus blob/web1 zip inventories with sizes — the index of what lives in the bucket
(objects like `https://s3.amazonaws.com/sanskrit-lexicon/scans/ACC/pg1_002.pdf`),
last refreshed 2023. One operational fact worth keeping: objects uploaded without
`--acl public-read` return `AccessDenied` to the public.

### enhancements/autocomplete/ + issue10/ — headword suggestion utilities

`autocomplete/` ships the headword lists `hw1.txt`/`hw11.txt` (~6 MB each) and the
generator `listsanhw1.py` (reads `../../../CORRECTIONS/sanhw1/sanhw1.txt`, another
sibling-repo dependency). `issue10/` is a Python-2 spelling-suggestion prototype
(`python2 suggest.py inputword`, Levenshtein-based) that fails to parse under
Python 3 — port-or-retire.

### issues/ — archival workspaces (plus one live prototype)

One directory per GitHub issue (`407`, `issue422`…`issue445`), indexed by
[issues/readme.txt](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/issues/readme.txt).
Policy: **archival — preserve for provenance, never refactor** (270 files classified
`archive-no-refactor`). Many scripts are byte-identical copies across issue dirs
(`issue422`–`issue432` are the same hwextra-Lbody conversion applied to ten
dictionaries) — a bug fixed in one copy is NOT fixed in the others; the canonical
version of anything reusable is `enhancements/code/`.

The one exception is
[issues/issue445/](https://github.com/sanskrit-lexicon/COLOGNE/tree/main/issues/issue445)
— a live Flask API + HTML search prototype (`python serve_api.py` →
`GET /search?key_query=…&data_query=…` on `http://127.0.0.1:5000/`; needs `flask`,
`flask_restx`, `flask_cors`, `lxml`, a `temp_pwg_10.sqlite` DB and `transform.xsl`).
It is a **local experiment only**: blanket CORS, `debug=True`, full-table scans, and
unvalidated user regexes make it unsafe to expose — see the P1 in
[ARCHITECTURE_REVIEW.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/ARCHITECTURE_REVIEW.md).
Its fate (promote or sunset) is an open taxonomy decision.

### xsswork/ and misc/ — notes and reference artifacts

[xsswork/readme.txt](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/xsswork/readme.txt)
preserves a 2022 reflected-XSS reproduction against the PWG scan viewer and a sketch
of an input-blacklist sanitizer. Treat it as a historical pointer only — the sketched
`str_replace` blacklist is bypass-prone and corrupts legitimate queries; real fixes
use contextual output escaping and live in the PHP repos.

[misc/](https://github.com/sanskrit-lexicon/COLOGNE/tree/main/misc) is pure reference:
the Harvard bibliography of the dictionaries, a Devanagari transliteration scheme PDF,
a 2019 conference deck, a 2017 broken-link crawl, a large Apte-format data dump
(`boroo.all`), and hand-written notes on gaps in Huet's morphology engine. Nothing
executes; nothing imports it.

---

## Adding a new dictionary to CDSL

The full flow lives in
[readme_new_dict_addition.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/readme_new_dict_addition.md)
(running example: `armh`/ARMH). It spans **five sibling repos plus one org** — this
summary is the map; follow the source doc step-by-step when executing.

1. **Make it work.** Create `csl-orig/v02/xxx/` with `xxx.txt` plus blank
   `xxx_hwextra.txt`, `xxx-meta2.txt`, `xxxheader.xml`. Create
   `csl-websanlexicon/v02/distinctfiles/xxx/web/webtc/` with a `pdffiles.txt`
   (`pc:pdffilename:headword`, headword optional). Register the dict in **both**
   `csl-pywork/v02/dictparams.py` and `csl-websanlexicon/v02/dictparams.py` (the
   latter with year/accent/WorldCat/title metadata). Append `generate_dict.sh` /
   `generate_web.sh` lines to the four `redo_{cologne,xampp}_all.sh` drivers. Add the
   scan-page URL to `$cologne_pdfpages_urls` in the websanlexicon `dictinfo.php` and
   in `csl-apidev/dictinfo.php` (also `$dictyear` there); add the display name to
   `csl-apidev/sample/dictnames.js` and the dictcode to
   `csl-apidev/simple-search/v1.1/parse_uri.php`. Register in
   `hwnorm1/sanhw1/sanhw1.py` (`dictyear` + the right `san_*_dicts` array) — then
   **rerun the hwnorm1 redo after `generate_dict.sh`, and copy the fresh
   `hwnorm1c.sqlite` into csl-apidev and push it**, or simple-search/servepdf will not
   see the new dictionary.
2. **Add markup.** Register the dictcode in the `%if dictlo in […]` guards of
   `csl-pywork/v02/makotemplates/pywork` so entries get `<s>` tags — without this,
   transliteration output silently stays SLP1 even when Devanagari is selected, and
   line breaks do not display.
3. **Scan images locally.** Split the source PDF with `pdftk` (frontmatter / content
   / endmatter, then `burst` to single pages), place pages in
   `cologne/scans/xxx/pdfpages`, generate `pdffiles.txt`.
4. **Scan images on GitHub.** Create repo `xxx` in the
   [sanskrit-lexicon-scans](https://github.com/sanskrit-lexicon-scans) org and push
   the single-page PDFs into `pdfpages/`.

Known gap recorded in the source doc: `csl-homepage` and `csl-doc` registration is
not covered ("Still not handled").

---

## Load-bearing vs legacy — the explicit verdicts

What feeds the live CDSL build/site, what is diagnostic, what is dead weight:

- **Feeds the live site directly:** `iast/slp1_roman.xml` + `roman_slp1.xml` (the
  production transcoding tables); the `readme_new_dict_addition.md` flow (touches five
  production repos); historically, `eascii/eachanges-degree/copy_orig.sh` (wrote
  corrections into csl-orig).
- **Active tooling, diagnostic outputs:** `tools/` (governance),
  `enhancements/code/updateByLine.py` + `xmlvalidate.py` (correction machinery),
  `eascii/` and `xmltag/` censuses (last touched 2024 and 2026 respectively),
  `localinstall/` runbooks, `makemd/`.
- **Legacy / archival — do not build on:** `stardict/` (py2 + silent-translit trap),
  `enhancements/issue10/` (py2), `enhancements/code/updateByLine_python2.py`,
  `aws/awsintro.txt` (2014 procedure; manifests still useful), `api/` (unfinalized
  2020 spec), `issues/` (except the issue445 prototype pending a decision),
  `xsswork/`, `misc/`, `localinstall/mac1/` (transcripts), `download1.sh`
  (superseded by `download2.sh`).

The row-level source of truth for these calls is
[docs/cleanup/taxonomy_proposals.csv](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/docs/cleanup/taxonomy_proposals.csv).

## Symptom → cause → cure

| Symptom | Cause | Cure |
|---|---|---|
| Transcoded text comes back unchanged (SLP1 in, SLP1 out), no error | `transcoder.py` couldn't find its FSM XML (wrong CWD, or `stardict/data/transcoder/` absent) and **silently passes input through** | Run from `iast/`; for stardict, create `data/transcoder/` and copy the tables in; spot-check output for Devanagari |
| `SyntaxError` on `print` or `xrange` | You ran a Python-2-only script (`stardict/make_babylon.py`, `issue10/*.py`, `updateByLine_python2.py`) under Python 3 | Use a py2 interpreter, or use the py3 twin (`updateByLine.py`); see the [interpreter table](#environment--prerequisites) |
| `UnicodeEncodeError: 'charmap' codec` printing Sanskrit on Windows | git-bash console encoding; the script lacks `sys.stdout.reconfigure(encoding='utf-8')` | Add the reconfigure line (present in all `eascii/` scripts as the model) |
| `redo_one.sh` / `redo_all.sh` can't find the input file | The `../../../cologne/csl-orig/...` sibling layout isn't in place | Recreate the umbrella layout (clone csl-orig under a shared `cologne/` parent) or edit the path; `eachanges-degree/` needs one *extra* `../` |
| `make_babylon.py` dies with `IOError` on first write | `stardict/output/` does not exist in the repo | `mkdir output` first |
| `make_md.py` raises `IndexError` immediately | No dictcode argument (bare `sys.argv[1]`) | `python3 make_md.py <dictcode>` |
| `make_md.py` `FileNotFoundError` on the XML | Not run from inside `makemd/`, or no sibling `<dictcode>/pywork/` tree | `cd makemd` first; needs a full CDSL checkout |
| `updateByLine.py` stops mid-run with a mismatch | A change-file `old` line doesn't match the current digitization — the source moved since the change-file was written | Regenerate the change-file against the current source; never force it |
| `download1.sh` 404s for `lrv` | `year=2020` hardcoded; LRV's display tree is 2022 | Use `download2.sh` (handles the exception) |
| Mac download script errors on `${x^^}` or behaves oddly | CRLF line endings from Windows editing, or old-bash incompatible upper-casing | Re-save LF-only; use `download2.sh` (uses `tr`, not `${x^^}`) |
| Local scan pages blank in Safari | Safari can't render the served PDF pages | Use Firefox |
| New dictionary shows SLP1 even with Devanagari selected | Dictcode not registered in the `%if dictlo in […]` markup guards (Step 2 of new-dict flow) | Add the code to the `adjust_slp1` guards in `csl-pywork/v02/makotemplates/pywork` |
| simple-search doesn't see a newly added dictionary | hwnorm1 redo not rerun, or fresh `hwnorm1c.sqlite` not copied into csl-apidev and pushed | Redo hwnorm1 **after** `generate_dict.sh`, copy the sqlite, push csl-apidev |
| S3 object returns `AccessDenied` | Uploaded without `--acl public-read` | Re-upload with the ACL flag |
| Cleanup-taxonomy run changed tracked files you didn't mean to change | The tool writes `docs/cleanup/*` in place | `git checkout -- docs/cleanup` after verification-only runs |

## Glossary

- **CDSL** — Cologne Digital Sanskrit Lexicon, the project behind
  [sanskrit-lexicon.uni-koeln.de](https://www.sanskrit-lexicon.uni-koeln.de/).
- **dictcode** — the 2–5-letter lowercase dictionary id (`mw`, `pwg`, `ap90`, `armh`…);
  uppercase form (`MW`) used in scan-repo and display contexts. ~38 codes.
- **digitization** — the master text file `csl-orig/v02/<xxx>/<xxx>.txt`, one line
  per printed line, with metalines.
- **metaline / `<L>` / `<LEND>`** — the record separators inside a digitization: an
  entry runs from its `<L>` line to its `<LEND>` line; the census tools only look
  inside entries.
- **change-file** — the two-line-transaction correction format (`old` verification
  line + `new`/`ins`/`del` action line) consumed by `updateByLine.py`.
- **pywork** — the per-dictionary build tree produced by
  [csl-pywork](https://github.com/sanskrit-lexicon/csl-pywork)'s `generate_dict.sh`,
  containing the dictionary XML the exporters read.
- **SLP1 / IAST / HK / Velthuis** — Sanskrit transliteration schemes; SLP1 is the
  internal encoding of the digitizations, IAST the scholarly roman form.
- **FSM tables** — the `<from>_<to>.xml` finite-state-machine mapping files
  (`slp1_roman.xml` etc.) that `transcoder.py` loads.
- **`.babylon`** — the intermediate text format the StarDict toolchain compiles into
  StarDict dictionaries.
- **web1 zip** — a prebuilt per-dictionary display bundle
  (`{dict}web1.zip`) served from the production server for local installs.
- **taxonomy / `human_decision`** — the cleanup classification of every repo file and
  the blank CSV column a maintainer fills (`approve`/`override`/`defer`/`ignore`)
  before any cleanup happens.

## Maintainer appendix

**Invariants to preserve:**

1. `updateByLine.py`'s stop-on-mismatch check is the correction system's safety
   property — never "fix" it to continue past a failed `old` match.
2. `iast/slp1_roman.xml`/`roman_slp1.xml` are the source of truth; the copies in
   csl-apidev and csl-websanlexicon are derived. Edit here, run the checks, install,
   push both consumers — in that order.
3. The cleanup taxonomy is proposal-only: nothing moves or deletes on the strength of
   the CSV alone; changes go through issues opened from the backlog after
   `human_decision` is filled.
4. `issues/` is archival: preserve, don't refactor. The canonical copy of any
   duplicated helper is `enhancements/code/`.
5. Census tools scan entries only (`<L>`…`<LEND>`); keep that scope when extending
   them, or their historical counts stop being comparable.

**Known defects, tracked and deliberate-not-yet-fixed** (all detailed in
[ARCHITECTURE_REVIEW.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/ARCHITECTURE_REVIEW.md);
fixing several is gated on the taxonomy `human_decision` pass):

- Silent transcoder passthrough on missing FSM XML — both `transcoder.py` copies (P1).
- `stardict/transcoder.py` is a divergent duplicate of `iast/transcoder.py` —
  consolidation is Human Approval Queue priority 1.
- Four scripts fail Python-3 parsing (`stardict/make_babylon.py`,
  `enhancements/issue10/levenshtein.py` + `suggest.py`,
  `enhancements/code/updateByLine_python2.py` twin kept deliberately).
- No dependency manifest; `flask*` needed only by the issue445 prototype.
- `dictionary_init.sh` downloads over plain HTTP without verification (P2).
- Thin CLIs: bare `sys.argv` indexing in `make_md.py`, `updateByLine.py` (P3).
- `xmltag/xmltag.py` carries dead code (unreachable `print`, unused `chkgreek`);
  `redo_all.sh` vs `catall.sh` list mismatch (documented in the walkthrough above).

**What CI checks on every PR**
([.github/workflows/ci.yml](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/.github/workflows/ci.yml)):
`ruff` lint (Python-2 dirs excluded via
[ruff.toml](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/ruff.toml)),
change-file format validation (`changes*.txt` must follow the `NNN` +
`old`/`new`/`ins`/`del` grammar), change-file UTF-8 validation, YAML lint. CodeQL
(Python) runs on PRs and weekly. Dependabot PRs auto-merge once checks pass.

**Companion metadoc:** improvement backlog, provenance, and revision history for this
manual live in
[docs/TOOLING_MANUAL.meta.md](https://github.com/sanskrit-lexicon/COLOGNE/blob/main/docs/TOOLING_MANUAL.meta.md).

_Dr. Mārcis Gasūns_
