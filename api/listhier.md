# 2. List Display page

## 2.1. Get a list of 25 nearby headwords for a given word.

Not working for non SLP1 inputs. Need examination

### 2.1.1. URL

http://www.sanskrit-lexicon.uni-koeln.de/scans/MW72Scan/2014/web/webtc1/disphier.php?key=Davala&keyboard=yes&inputType=phonetic&unicodeInput=devInscript&phoneticInput=slp1&serverOptions=deva&viewAs=phonetic

### 2.1.2. Input parameters

inputType	phonetic
key	Davala
keyboard	yes
phoneticInput	slp1
serverOptions	deva
unicodeInput	devInscript
viewAs	phonetic

### 2.1.3. Suggested Clean URL

http://www.sanskrit-lexicon.uni-koeln.de/list/dictcode/word/{inputtransliteration}/{outputtransliteration}/{accent}

### 2.1.4. Examples

1. http://www.sanskrit-lexicon.uni-koeln.de/list/MW/Davala/slp1/deva/yes
2. http://www.sanskrit-lexicon.uni-koeln.de/list/PW/अनुभूति/deva/hk
3. http://www.sanskrit-lexicon.uni-koeln.de/list/MD/raama/itrans
4. http://www.sanskrit-lexicon.uni-koeln.de/list/MD/sItA

### 2.1.5. Allowable values

1. dictcode - ACC / AE / AP / AP90 / BEN / BHS / BOP / BOR / BUR / CAE / CCS / GRA / GST / IEG / INM / KRM / MCI / MD / MW / MW72 / MWE / PD / PE / PGN / PUI / PW / PWG / SCH / SHS / SKD / SNP / STC / VCP / VEI / WIL / YAT. For full form see http://www.sanskrit-lexicon.uni-koeln.de/.
2. inputtransliteration - slp1/deva/hk/roman/it
3. outputtransliteration - slp1/deva/hk/roman/itrans

### 2.1.6. Defaults

1. inputtransliteration - slp1
2. outputtransliteration - deva
3. accent - no

### 2.1.7. Rewrite rules

```
RewriteRule ^list/([^/]*)/([^/]*)/([^/]*)/([^/]*)/([^/]+)/$ http://www.sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2014/web/webtc1/listhier.php?key=$2&keyboard=yes&inputType=phonetic&unicodeInput=devInscript&phoneticInput=$3&serverOptions=$4&accent=$5&viewAs=phonetic
RewriteRule ^list/([^/]*)/([^/]*)/([^/]*)/([^/]*)/([^/]+)$ http://www.sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2014/web/webtc1/listhier.php?key=$2&keyboard=yes&inputType=phonetic&unicodeInput=devInscript&phoneticInput=$3&serverOptions=$4&accent=$5&viewAs=phonetic
RewriteRule ^list/([^/]*)/([^/]*)/([^/]*)/([^/]*)/$ http://www.sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2014/web/webtc1/listhier.php?key=$2&keyboard=yes&inputType=phonetic&unicodeInput=devInscript&phoneticInput=$3&serverOptions=$4&accent=no&viewAs=phonetic
RewriteRule ^list/([^/]*)/([^/]*)/([^/]*)/([^/]*)$ http://www.sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2014/web/webtc1/listhier.php?key=$2&keyboard=yes&inputType=phonetic&unicodeInput=devInscript&phoneticInput=$3&serverOptions=$4&accent=no&viewAs=phonetic
RewriteRule ^list/([^/]*)/([^/]*)/([^/]*)/$ http://www.sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2014/web/webtc1/listhier.php?key=$2&keyboard=yes&inputType=phonetic&unicodeInput=devInscript&phoneticInput=$3&serverOptions=deva&accent=no&viewAs=phonetic
RewriteRule ^list/([^/]*)/([^/]*)/([^/]*)$ http://www.sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2014/web/webtc1/listhier.php?key=$2&keyboard=yes&inputType=phonetic&unicodeInput=devInscript&phoneticInput=$3&serverOptions=deva&accent=no&viewAs=phonetic
RewriteRule ^list/([^/]*)/([^/]*)/$ http://www.sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2014/web/webtc1/listhier.php?key=$2&keyboard=yes&inputType=phonetic&unicodeInput=devInscript&phoneticInput=slp1&serverOptions=deva&accent=no&viewAs=phonetic
RewriteRule ^list/([^/]*)/([^/]*)$ http://www.sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2014/web/webtc1/listhier.php?key=$2&keyboard=yes&inputType=phonetic&unicodeInput=devInscript&phoneticInput=slp1&serverOptions=deva&accent=no&viewAs=phonetic
```

### 2.1.8. Expected output

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
### 2.1.9. Questions

1. Not working for non-SLP1 items. The current Cologne API is a bit confusing.

