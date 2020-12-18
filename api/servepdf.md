# 1. Basic Display page

## 1.2. Get a PDF page for given input.

### 1.2.1. URL

http://sanskrit-lexicon.uni-koeln.de/scans/MWScan/2020/web/webtc/servepdf.php?page=513

### 1.2.2. Input parameters

page

### 1.2.3. Suggested Clean URL

http://sanskrit-lexicon.uni-koeln.de/pdf/dictcode/mode/value

### 1.2.4. Examples

1. http://sanskrit-lexicon.uni-koeln.de/pdf/MW/w/Davala
2. http://sanskrit-lexicon.uni-koeln.de/pdf/MD/p/513

### 1.2.5. Allowable values

1. dictcode - ACC / AE / AP / AP90 / BEN / BHS / BOP / BOR / BUR / CAE / CCS / GRA / GST / IEG / INM / KRM / MCI / MD / MW / MW72 / MWE / PD / PE / PGN / PUI / PW / PWG / SCH / SHS / SKD / SNP / STC / VCP / VEI / WIL / YAT. For full form see http://sanskrit-lexicon.uni-koeln.de/.
2. mode - w/p (for word / page respectively)
3. value - headword in SLP1 / page number

### 1.2.6. Defaults

None.
All items are mandatory.

### 1.2.7. Rewrite rules

```
RewriteRule ^pdf/([^/]*)/word/([^/]*)$/ http://sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=$1&key=$2
RewriteRule ^pdf/([^/]*)/word/([^/]*)$ http://sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=$1&key=$2
RewriteRule ^pdf/([^/]*)/page/([^/]*)$/ http://sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2020/web/webtc/servepdf.php?page=$2
RewriteRule ^pdf/([^/]*)/page/([^/]*)$ http://sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2020/web/webtc/servepdf.php?page=$2
```

### 1.2.8. Expected output

```
{
'params': {
	'dictcode': 'MW',
	'mode': 'word',
	'value': 'Davala',
	},
'result': 'http://sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=MW&key=Davala'
}
```
or 
```
{
'params': {
	'dictcode': 'MW',
	'mode': 'page',
	'value': '513',
	},
'result': 'http://sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=MW&key=513'
}
```
### 1.2.9. Questions

1. Can there be a mode like http://sanskrit-lexicon.uni-koeln.de/pdf/MD/l/100564 where `l` stands for lnum and 100564 is the lnum to search PDF for.


