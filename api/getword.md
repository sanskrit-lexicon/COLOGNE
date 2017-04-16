# 1. Basic Display page

## 1.1. Get a single entry detail

### 1.1.1. URL

http://www.sanskrit-lexicon.uni-koeln.de/scans/MWScan/2014/web/webtc/getword.php?key=Davala&filter=deva&noLit=off&accent=no&transLit=slp1

### 1.1.2. Input parameters

accent	no
filter	deva
key	Davala
noLit	off
transLit	slp1

### 1.1.3. Suggested Clean URL

http://www.sanskrit-lexicon.uni-koeln.de/entries/dictcode/word/{inputtransliteration}/{outputtransliteration}/{accent}

### 1.1.4. Examples

1. http://www.sanskrit-lexicon.uni-koeln.de/entries/MW/Davala/slp1/deva/yes
2. http://www.sanskrit-lexicon.uni-koeln.de/entries/PW/अनुभूति/deva/hk
3. http://www.sanskrit-lexicon.uni-koeln.de/entries/MD/raama/itrans
4. http://www.sanskrit-lexicon.uni-koeln.de/entries/MD/sItA

### 1.1.5. Allowable values

1. dictcode - ACC / AE / AP / AP90 / BEN / BHS / BOP / BOR / BUR / CAE / CCS / GRA / GST / IEG / INM / KRM / MCI / MD / MW / MW72 / MWE / PD / PE / PGN / PUI / PW / PWG / SCH / SHS / SKD / SNP / STC / VCP / VEI / WIL / YAT. For full form see http://www.sanskrit-lexicon.uni-koeln.de/.
2. inputtransliteration - slp1/deva/hk/roman/itrans
3. outputtransliteration - slp1/deva/hk/roman/itrans
4. accent - yes/no

### 1.1.6. Defaults

1. inputtransliteration - slp1
2. outputtransliteration - deva
3. accent - no

### 1.1.7. Rewrite rules

```
RewriteRule ^entries/([^/]*)/([^/]*)/([^/]*)/([^/]*)/([^/]+)/$ http://www.sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2014/web/webtc/getword.php?key=$2&filter=$4&noLit=off&accent=$5&transLit=$3
RewriteRule ^entries/([^/]*)/([^/]*)/([^/]*)/([^/]*)/([^/]+)$ http://www.sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2014/web/webtc/getword.php?key=$2&filter=$4&noLit=off&accent=$5&transLit=$3
RewriteRule ^entries/([^/]*)/([^/]*)/([^/]*)/([^/]*)/$ http://www.sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2014/web/webtc/getword.php?key=$2&filter=$4&noLit=off&accent=no&transLit=$3
RewriteRule ^entries/([^/]*)/([^/]*)/([^/]*)/([^/]*)$ http://www.sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2014/web/webtc/getword.php?key=$2&filter=$4&noLit=off&accent=no&transLit=$3
RewriteRule ^entries/([^/]*)/([^/]*)/([^/]*)/$ http://www.sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2014/web/webtc/getword.php?key=$2&filter=deva&noLit=off&accent=no&transLit=$3
RewriteRule ^entries/([^/]*)/([^/]*)/([^/]*)$ http://www.sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2014/web/webtc/getword.php?key=$2&filter=deva&noLit=off&accent=no&transLit=$3
RewriteRule ^entries/([^/]*)/([^/]*)/$ http://www.sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2014/web/webtc/getword.php?key=$2&filter=deva&noLit=off&accent=no&transLit=slp1
RewriteRule ^entries/([^/]*)/([^/]*)$ http://www.sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2014/web/webtc/getword.php?key=$2&filter=deva&noLit=off&accent=no&transLit=slp1
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
		'imgUrl': 'http://www.sanskrit-lexicon.uni-koeln.de/scans/MWScan/2014/web/webtc/servepdf.php?page=513'
		'html': 'dictionary entry in HTML format',
		'text': 'dictionary entry in text format',
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
2. List of dictionaries still using 2013 display will have to be handled slightly differently. Their list is needed.
3. Any other missing parameter?



