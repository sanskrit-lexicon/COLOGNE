# 2. List Display page

## 2.1. Get a list of 25 nearby headwords for a given word.

Not working for non SLP1 inputs. Need examination

### 2.1.1. URL

https://sanskrit-lexicon.uni-koeln.de/scans/MWScan/2020/web/webtc1/listhier.php?key=Davala&keyboard=yes&inputType=phonetic&unicodeInput=devInscript&phoneticInput=slp1&serverOptions=deva&accent=no&viewAs=phonetic

### 2.1.2. Input parameters

inputType	phonetic
key	Davala
keyboard	yes
phoneticInput	slp1
serverOptions	deva
unicodeInput	devInscript
viewAs	phonetic

### 2.1.3. Suggested Clean URL

http://sanskrit-lexicon.uni-koeln.de/list/dictcode/word/{inputtransliteration}/{outputtransliteration}/{accent}

### 2.1.4. Examples

1. http://sanskrit-lexicon.uni-koeln.de/list/MW/Davala/s/d/y
2. http://sanskrit-lexicon.uni-koeln.de/list/PW/अनुभूति/d/h
3. http://sanskrit-lexicon.uni-koeln.de/list/MD/raama/i
4. http://sanskrit-lexicon.uni-koeln.de/list/MD/sItA

### 2.1.5. Allowable values

1. dictcode - ACC / AE / AP / AP90 / BEN / BHS / BOP / BOR / BUR / CAE / CCS / GRA / GST / IEG / INM / KRM / MCI / MD / MW / MW72 / MWE / PD / PE / PGN / PUI / PW / PWG / SCH / SHS / SKD / SNP / STC / VCP / VEI / WIL / YAT. For full form see http://sanskrit-lexicon.uni-koeln.de/.
2. inputtransliteration - s/d/h/r/i (for slp1/deva/hk/roman/itrans respectively)
3. outputtransliteration - s/d/h/r/i (for slp1/deva/hk/roman/itrans respectively)

### 2.1.6. Defaults

1. inputtransliteration - s
2. outputtransliteration - d

### 2.1.7. Rewrite rules

```
RewriteRule ^list/([^/]*)/([^/]*)/([^/]*)/([^/]*)/([^/]+)/$ http://sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2020/web/webtc1/listhier.php?key=$2&keyboard=yes&inputType=phonetic&unicodeInput=devInscript&phoneticInput=$3&serverOptions=$4&accent=$5&viewAs=phonetic
RewriteRule ^list/([^/]*)/([^/]*)/([^/]*)/([^/]*)/([^/]+)$ http://sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2020/web/webtc1/listhier.php?key=$2&keyboard=yes&inputType=phonetic&unicodeInput=devInscript&phoneticInput=$3&serverOptions=$4&accent=$5&viewAs=phonetic
RewriteRule ^list/([^/]*)/([^/]*)/([^/]*)/([^/]*)/$ http://sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2020/web/webtc1/listhier.php?key=$2&keyboard=yes&inputType=phonetic&unicodeInput=devInscript&phoneticInput=$3&serverOptions=$4&accent=no&viewAs=phonetic
RewriteRule ^list/([^/]*)/([^/]*)/([^/]*)/([^/]*)$ http://sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2020/web/webtc1/listhier.php?key=$2&keyboard=yes&inputType=phonetic&unicodeInput=devInscript&phoneticInput=$3&serverOptions=$4&accent=no&viewAs=phonetic
RewriteRule ^list/([^/]*)/([^/]*)/([^/]*)/$ http://sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2020/web/webtc1/listhier.php?key=$2&keyboard=yes&inputType=phonetic&unicodeInput=devInscript&phoneticInput=$3&serverOptions=deva&accent=no&viewAs=phonetic
RewriteRule ^list/([^/]*)/([^/]*)/([^/]*)$ http://sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2020/web/webtc1/listhier.php?key=$2&keyboard=yes&inputType=phonetic&unicodeInput=devInscript&phoneticInput=$3&serverOptions=deva&accent=no&viewAs=phonetic
RewriteRule ^list/([^/]*)/([^/]*)/$ http://sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2020/web/webtc1/listhier.php?key=$2&keyboard=yes&inputType=phonetic&unicodeInput=devInscript&phoneticInput=slp1&serverOptions=deva&accent=no&viewAs=phonetic
RewriteRule ^list/([^/]*)/([^/]*)$ http://sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2020/web/webtc1/listhier.php?key=$2&keyboard=yes&inputType=phonetic&unicodeInput=devInscript&phoneticInput=slp1&serverOptions=deva&accent=no&viewAs=phonetic
```

### 2.1.8. Expected output

```
{
'params': {
	'dictcode': 'MW',
	'headword': 'Davala',
	},
'result': [
		['..', 'DarzaRAtman'],
		['.', 'DarzaRIya'],
		['.', 'Darzita'],
		['.', 'Darzin'],
		['', 'DalaRqa'],
		['', 'Dalila'],
		['', 'Dav'],
		['.', 'DAvIyas'],
		['', 'Dava 1'],
		['', 'Dava 2'],
		['', 'DavanI'],
		['', 'Davara'],
		['', 'Davala'],
		['..', 'Davalagiri'],
		['..', 'Davalagfha'],
		['..', 'Davalacandra'],
		['..', 'DavalatA'],
		['..', 'Davalatva'],
		['..', 'DavalanibanDa'],
		['..', 'Davalapakza'],
		['..', 'DavalamuKa'],
		['..', 'DavalamfttikA'],
		['..', 'DavalayAvanAla'],
		['..', 'Davalasmfti'],
		['..', 'DavalANka']
	]
}
```
### 2.1.9. Questions

1. What are the use of all the input parameters used currently?
2. What is the importance of 0 / 1 / 2 dots before the word? Indentation level?


