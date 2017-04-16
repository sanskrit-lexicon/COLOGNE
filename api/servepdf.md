# 1. Basic Display page

## 1.2. Get a PDF page for given input.

### 1.2.1. URL

http://www.sanskrit-lexicon.uni-koeln.de/scans/MWScan/2014/web/webtc/servepdf.php?page=513

### 1.2.2. Input parameters

page

### 1.2.3. Suggested Clean URL

http://www.sanskrit-lexicon.uni-koeln.de/pdf/dictcode/mode/value

### 1.2.4. Examples

1. http://www.sanskrit-lexicon.uni-koeln.de/entries/MW/word/Davala
3. http://www.sanskrit-lexicon.uni-koeln.de/entries/MD/page/513

### 1.2.5. Allowable values

1. dictcode - ACC / AE / AP / AP90 / BEN / BHS / BOP / BOR / BUR / CAE / CCS / GRA / GST / IEG / INM / KRM / MCI / MD / MW / MW72 / MWE / PD / PE / PGN / PUI / PW / PWG / SCH / SHS / SKD / SNP / STC / VCP / VEI / WIL / YAT. For full form see http://www.sanskrit-lexicon.uni-koeln.de/.
2. mode - word / page
3. value - headword in SLP1 / page number

### 1.2.6. Defaults

None.
All items are mandatory.

### 1.2.7. Rewrite rules

```
RewriteRule ^pdf/([^/]*)/word/([^/]*)$/ http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=$1&key=$2
RewriteRule ^pdf/([^/]*)/word/([^/]*)$ http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=$1&key=$2
RewriteRule ^pdf/([^/]*)/page/([^/]*)$/ http://www.sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2014/web/webtc/servepdf.php?page=$2
RewriteRule ^pdf/([^/]*)/page/([^/]*)$ http://www.sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2014/web/webtc/servepdf.php?page=$2
```

### 1.2.8. Expected output

```
{
'params': {
	'dictcode': 'MW',
	'mode': 'word',
	'value': 'Davala',
	},
'result': 'http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=$1&key=$2'
}
```
### 1.2.9. Questions

	

