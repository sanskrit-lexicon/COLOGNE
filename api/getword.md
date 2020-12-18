# 1. Basic Display page

## 1.1. Get a single entry detail

### 1.1.1. URL

http://sanskrit-lexicon.uni-koeln.de/scans/MWScan/2020/web/webtc/getword.php?key=Davala&filter=deva&noLit=off&accent=no&transLit=slp1

### 1.1.2. Input parameters

accent	no
filter	deva
key	Davala
noLit	off
transLit	slp1

### 1.1.3. Suggested Clean URL

http://sanskrit-lexicon.uni-koeln.de/dictcode/word/{inputtransliteration}/{outputtransliteration}/{accent}

### 1.1.4. Examples

1. http://sanskrit-lexicon.uni-koeln.de/MW/Davala/s/d/y
2. http://sanskrit-lexicon.uni-koeln.de/PW/अनुभूति/d/h
3. http://sanskrit-lexicon.uni-koeln.de/MD/raama/i
4. http://sanskrit-lexicon.uni-koeln.de/MD/sItA

### 1.1.5. Allowable values

1. dictcode - ACC / AE / AP / AP90 / BEN / BHS / BOP / BOR / BUR / CAE / CCS / GRA / GST / IEG / INM / KRM / MCI / MD / MW / MW72 / MWE / PD / PE / PGN / PUI / PW / PWG / SCH / SHS / SKD / SNP / STC / VCP / VEI / WIL / YAT. For full form see http://sanskrit-lexicon.uni-koeln.de/.
2. inputtransliteration - s/d/h/r/i (for slp1/deva/hk/roman/itrans respectively)
3. outputtransliteration - s/d/h/r/i (for slp1/deva/hk/roman/itrans respectively)
4. accent - y/n

### 1.1.6. Defaults

1. inputtransliteration - s
2. outputtransliteration - d
3. accent - n

### 1.1.7. Rewrite rules

```
RewriteRule ^entries/([^/]*)/([^/]*)/([^/]*)/([^/]*)/([^/]+)/$ http://sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2020/web/webtc/getword.php?key=$2&filter=$4&noLit=off&accent=$5&transLit=$3
RewriteRule ^entries/([^/]*)/([^/]*)/([^/]*)/([^/]*)/([^/]+)$ http://sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2020/web/webtc/getword.php?key=$2&filter=$4&noLit=off&accent=$5&transLit=$3
RewriteRule ^entries/([^/]*)/([^/]*)/([^/]*)/([^/]*)/$ http://sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2020/web/webtc/getword.php?key=$2&filter=$4&noLit=off&accent=no&transLit=$3
RewriteRule ^entries/([^/]*)/([^/]*)/([^/]*)/([^/]*)$ http://sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2020/web/webtc/getword.php?key=$2&filter=$4&noLit=off&accent=no&transLit=$3
RewriteRule ^entries/([^/]*)/([^/]*)/([^/]*)/$ http://sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2020/web/webtc/getword.php?key=$2&filter=deva&noLit=off&accent=no&transLit=$3
RewriteRule ^entries/([^/]*)/([^/]*)/([^/]*)$ http://sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2020/web/webtc/getword.php?key=$2&filter=deva&noLit=off&accent=no&transLit=$3
RewriteRule ^entries/([^/]*)/([^/]*)/$ http://sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2020/web/webtc/getword.php?key=$2&filter=deva&noLit=off&accent=no&transLit=slp1
RewriteRule ^entries/([^/]*)/([^/]*)$ http://sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2020/web/webtc/getword.php?key=$2&filter=deva&noLit=off&accent=no&transLit=slp1
```

### 1.1.8. Expected output

```
{
'params': {
	'dictcode': 'MW',
	'keyword': 'Davala',
	'inputtransliteration': 'slp1',
	'outputtransliteration': 'deva',
	'accent': 'yes'
	},
'results': [
		[
		'recordId': '100564',
		'pageNumber': '513',
		'columnId': '2',
		'imgUrl': 'http://sanskrit-lexicon.uni-koeln.de/scans/MWScan/2020/web/webtc/servepdf.php?page=513'
		'html': 'dictionary entry in HTML format',
		'text': 'dictionary entry in text format',
		'xml': 'dictionary entry in xml format',
		'references': [
			'Var.', 
			'Kāv.',
			'Pur.'
			]
		],
		[
		.....SAME FORMAT AS ABOVE
		],
		[
		.....SAME FORMAT AS ABOVE
		]
	]

}
```
### 1.1.9. Questions

1. What is the purpose of noLit?
2. Any other missing parameter?



