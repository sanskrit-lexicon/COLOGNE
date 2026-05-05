# Cologne Digital Sanskrit Dictionaries — Development Tools

Development of http://www.sanskrit-lexicon.uni-koeln.de/

This repository contains analysis and utility scripts for the Cologne Digital Sanskrit Dictionaries — a collection of ~35 Sanskrit lexicons digitized and hosted by the University of Cologne. The dictionary data itself lives in the related repositories listed below.

---

## Dictionary data format

Each dictionary `xxx` has a UTF-8 text file `xxx.txt` in `csl-orig/v02/xxx/`. Content lines within an entry are bounded by a metaline starting with `<L>` and a closing `<LEND>` line; most scripts ignore anything outside those markers. Sanskrit text in the digitizations uses the SLP1 transliteration scheme internally.

Dictionary codes are lowercase (e.g., `mw`, `pw`, `cae`); the uppercase form (e.g., `MW`) is used in URLs and display names.

## Transliteration schemes

The `iast/transcoder.py` module implements an FSM-based transcoder between:

| Code | Scheme |
|------|--------|
| `slp1` | Internal scheme used in digitizations |
| `roman` | IAST (standard academic transliteration) |
| `deva` | Devanagari |
| `hk` | Harvard-Kyoto |
| `itrans` | ITRANS |

The paired files `iast/slp1_roman.xml` and `iast/roman_slp1.xml` are the source of truth for the transcoder and must remain in sync.

---

## Tools

### xmltag — analyze XML tags

Finds all XML-type tags in a dictionary digitization, with occurrence counts.

```bash
cd xmltag
sh redo_one.sh mw          # produces xmltag_mw.txt
sh redo_all.sh             # all dictionaries
sh catall.sh > all_xmltags.txt

# or directly:
python xmltag.py path/to/xxx.txt output.txt

# find <chg>...</chg> tags specifically:
python chgtag.py path/to/xxx.txt output.txt
```

### eascii — find non-ASCII Unicode characters

Finds all characters with code point > 127 inside dictionary entries, with counts.

```bash
cd eascii
sh redo_one.sh mw          # produces eadata/ea_mw.txt
sh redo_all.sh
sh catall.sh > all_ea.txt

# or directly:
python ea.py path/to/xxx.txt output.txt

# cross-dictionary summaries (requires csl-orig sibling repo):
python easummary.py ../../../cologne/csl-orig easummary
python easummary_meta.py ../../../cologne/csl-orig easummary_meta
```

### iast — transliteration utilities

```bash
cd iast
# Check consistency between the two transcoder XML files:
python slp1_iast.py slp1_roman.xml slp1_iast.txt

# Install updated XML files into a local XAMPP setup:
sh install_local.sh
```

### makemd — generate Markdown from dictionary XML

Converts a processed dictionary XML file into Devanagari-keyed Markdown files for use with Hugo static sites.

```bash
cd makemd
# Requires: pip install indic-transliteration
# Expects XML at ../../<dictcode>/pywork/<dictcode>.xml
python make_md.py snp      # produces MD/snp/*.md
```

### stardict — generate Babylon/StarDict output

> **Note:** `make_babylon.py` uses Python 2 syntax.

```bash
cd stardict
python make_babylon.py <pathToDicts> <dictId>
```

### updateByLine — apply corrections to a digitization

Applies a structured diff file to a dictionary text file.

```bash
python enhancements/code/updateByLine.py OLDFILE CHGFILE NEWFILE
```

`CHGFILE` format: two-line transactions with `ln old <text>` / `ln new|ins|del <text>`. Lines beginning with `;` are comments.

### xmlvalidate — validate XML against a DTD

```bash
# Requires Python 2 + lxml
python enhancements/code/xmlvalidate.py file.xml file.dtd
```

### Local dictionary setup

Download a working environment (orig + pywork + web) for one dictionary from AWS blobs:

```bash
cd enhancements/code
sh dictionary_init.sh mw
```

Or download just the web display files from the Cologne server:

```bash
cd localinstall/mac
sh download1.sh mw
```

---

## Repository structure

| Directory | Purpose |
|-----------|---------|
| `xmltag/` | XML tag analysis; per-dictionary `xmltag_xxx.txt` and combined `all_xmltags.txt` |
| `eascii/` | Extended ASCII/Unicode analysis; `eadata/ea_xxx.txt` files; `eachanges-degree/` tracks historical correction batches |
| `iast/` | Transliteration XML files and consistency checker; shared `transcoder.py` FSM engine |
| `makemd/` | Convert dictionary XML to Devanagari-keyed Markdown for Hugo |
| `stardict/` | Generate Babylon/StarDict format (Python 2) |
| `enhancements/code/` | General utilities: `updateByLine.py`, `xmlvalidate.py`, `dictionary_init.sh`, encoding converters |
| `api/` | Design docs for the REST API (getword, servepdf, listhier) |
| `aws/` | Notes and file listings for the `s3://sanskrit-lexicon` S3 bucket |
| `localinstall/` | Scripts for setting up a local XAMPP installation |
| `issues/` | Per-issue working directories |

## Related repositories

These scripts assume the following repos are siblings under a common parent directory:

- [`csl-orig`](https://github.com/sanskrit-lexicon/csl-orig) — raw digitizations (`v02/xxx/xxx.txt`)
- [`csl-pywork`](https://github.com/sanskrit-lexicon/csl-pywork) — Python pipeline for generating XML and SQLite
- [`csl-websanlexicon`](https://github.com/sanskrit-lexicon/csl-websanlexicon) — Mako/PHP web display layer
- [`csl-apidev`](https://github.com/sanskrit-lexicon/csl-apidev) — PHP API backend and simple search
- [`csl-corrections`](https://github.com/sanskrit-lexicon/csl-corrections) — correction files (`xxx_printchange.txt`)

---

## License

The data (digitizations, scanned images, and PDFs) in this directory or in the AWS sanskrit-lexicon bucket (`https://s3.amazonaws.com/sanskrit-lexicon/*`) are available under the following licence statement:

All rights reserved other than those granted under the Creative Commons Attribution Non-Commercial Share Alike license available in full [here](http://creativecommons.org/licenses/by-nc-sa/3.0/legalcode), and summarized [here](http://creativecommons.org/licenses/by-nc-sa/3.0/). Permission is granted to build upon this work non-commercially, as long as credit is explicitly acknowledged exactly as described herein and derivative work is distributed under the same license.
