# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository contains development tools for the [Cologne Digital Sanskrit Dictionaries](http://www.sanskrit-lexicon.uni-koeln.de/) — a collection of ~35 Sanskrit lexicons digitized and hosted by the University of Cologne. The repo does not contain the dictionary data itself; it contains analysis and utility scripts that operate on data from the related `csl-orig`, `csl-pywork`, and `csl-websanlexicon` repositories.

## Dictionary data format

Each dictionary `xxx` has a UTF-8 text file `xxx.txt` in `csl-orig/v02/xxx/`. Lines within an entry are bounded by a metaline starting with `<L>` and a closing `<LEND>` line. Content lines use XML-like tags and SLP1 transliteration for Sanskrit text. Most scripts skip content outside `<L>`/`<LEND>` pairs (front-matter, appendices, etc.).

Dictionary codes are lowercase (e.g., `mw`, `pw`, `cae`); the uppercase form (e.g., `MW`) is the "dictup" used in URLs and display names.

## Transliteration schemes

The `iast/transcoder.py` module implements an FSM-based transcoder. Scheme names used throughout:
- `slp1` — internal scheme used in digitizations
- `roman` — IAST (standard academic transliteration)
- `deva` — Devanagari
- `hk` — Harvard-Kyoto
- `roman_slp1.xml` / `slp1_roman.xml` — paired XML files that are the source of truth for the transcoder; must remain in sync

## Key scripts and how to run them

All scripts expect to be run from their containing directory. Paths to dictionary data assume the sibling repo layout `../../../cologne/csl-orig/v02/`.

### xmltag — analyze XML tags in a dictionary
```bash
# One dictionary:
sh redo_one.sh mw        # produces xmltag_mw.txt
# All dictionaries:
sh redo_all.sh
sh catall.sh > all_xmltags.txt

# Directly:
python xmltag.py <path/to/xxx.txt> <output.txt>

# Find <chg>...</chg> tags:
python chgtag.py <path/to/xxx.txt> <output.txt>
```

### eascii — find non-ASCII (Unicode > 127) characters in a dictionary
```bash
# One dictionary:
sh redo_one.sh mw        # produces eadata/ea_mw.txt
# All dictionaries:
sh redo_all.sh
sh catall.sh > all_ea.txt

# Directly:
python ea.py <path/to/xxx.txt> <output.txt>

# Cross-dictionary summaries (requires csl-orig sibling repo):
python easummary.py ../../../cologne/csl-orig easummary
python easummary_meta.py ../../../cologne/csl-orig easummary_meta
```

### iast — transliteration utilities
```bash
# Check slp1↔IAST consistency between the two XML files:
python slp1_iast.py slp1_roman.xml slp1_iast.txt

# Install updated XML files locally (XAMPP):
sh install_local.sh
```

### makemd — generate Hugo-compatible Markdown from dictionary XML
```bash
# Requires: pip install indic-transliteration
# Expects XML at ../../<dictcode>/pywork/<dictcode>.xml
python make_md.py snp    # produces MD/snp/*.md
```

### stardict — generate Babylon/StarDict output
```bash
# Note: make_babylon.py uses Python 2 syntax (print statements, xrange)
python make_babylon.py <pathToDicts> <dictId>
```

### updateByLine — apply corrections to a dictionary text file
```bash
python updateByLine.py OLDFILE CHGFILE NEWFILE
```
`CHGFILE` format: two-line transactions with `ln old <text>` / `ln new <text>` (or `ins`/`del`). Lines beginning with `;` are comments.

### Local dictionary setup (download working environment)
```bash
# From enhancements/code/, download orig+pywork+web from AWS blobs:
sh dictionary_init.sh mw

# From localinstall/mac/, download web1 zip from Cologne server:
sh download1.sh mw
```

### xmlvalidate
```bash
# Python 2 + lxml required
python xmlvalidate.py file.xml file.dtd
```

## Repository structure

| Directory | Purpose |
|-----------|---------|
| `xmltag/` | Analyze XML tags in digitizations; per-dictionary `xmltag_xxx.txt` files and `all_xmltags.txt` |
| `eascii/` | Analyze extended ASCII/Unicode chars; per-dictionary `eadata/ea_xxx.txt` files; `eachanges-degree/` tracks historical correction batches |
| `iast/` | Transliteration XML files (`slp1_roman.xml`, `roman_slp1.xml`) and consistency checker; `transcoder.py` is the shared FSM engine |
| `makemd/` | Convert dictionary XML to Devanagari-keyed Markdown for Hugo static sites |
| `stardict/` | Generate Babylon/StarDict format files (Python 2) |
| `enhancements/code/` | General-purpose utilities: `updateByLine.py`, `xmlvalidate.py`, `dictionary_init.sh`, encoding converters |
| `api/` | Design docs for proposed REST API (getword, servepdf, listhier) |
| `aws/` | Notes and file listings for the `s3://sanskrit-lexicon` S3 bucket |
| `localinstall/` | Scripts for downloading a local XAMPP-based installation |
| `issues/` | Per-issue working directories for bug fixes |
| `xsswork/` | Notes on XSS remediation in the PHP display layer |

## Related repositories

Scripts assume these repos are siblings of this one under a common parent (e.g., `cologne/`):
- `csl-orig` — raw digitizations (`v02/xxx/xxx.txt`)
- `csl-pywork` — Python pipeline for generating XML and SQLite from digitizations
- `csl-websanlexicon` — Mako/PHP web display layer
- `csl-apidev` — PHP API backend and simple-search
- `CORRECTIONS` / `csl-corrections` — correction files (`xxx_printchange.txt`)
