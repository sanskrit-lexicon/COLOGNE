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
2. http://www.sanskrit-lexicon.uni-koeln.de/entries/PW/anubhUti/hk/hk
3. http://www.sanskrit-lexicon.uni-koeln.de/entries/MD/raama/itrans
4. http://www.sanskrit-lexicon.uni-koeln.de/entries/MD/sItA

### 1.1.5. Allowable values

1. inputtransliteration - slp1/deva/hk/roman/itrans
2. outputtransliteration - slp1/deva/hk/roman/itrans
3. accent - yes/no

### 1.1.6. Defaults

1. inputtransliteration - slp1
2. outputtransliteration - deva
3. accent - no

### 1.1.7. Rewrite rules

```
RewriteRule ^entries/([^/]*)/([^/]*)/([^/]*)/([^/]*)/([^/]+)$ http://www.sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2014/web/webtc/getword.php?key=$2&filter=$4&noLit=off&accent=$5&transLit=$3
RewriteRule ^entries/([^/]*)/([^/]*)/([^/]*)/([^/]*)/$ http://www.sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2014/web/webtc/getword.php?key=$2&filter=$4&noLit=off&accent=no&transLit=$3
RewriteRule ^entries/([^/]*)/([^/]*)/([^/]*)/([^/]*)$ http://www.sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2014/web/webtc/getword.php?key=$2&filter=$4&noLit=off&accent=no&transLit=$3
RewriteRule ^entries/([^/]*)/([^/]*)/([^/]*)/$ http://www.sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2014/web/webtc/getword.php?key=$2&filter=deva&noLit=off&accent=no&transLit=$3
RewriteRule ^entries/([^/]*)/([^/]*)/([^/]*)$ http://www.sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2014/web/webtc/getword.php?key=$2&filter=deva&noLit=off&accent=no&transLit=$3
RewriteRule ^entries/([^/]*)/([^/]*)/$ http://www.sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2014/web/webtc/getword.php?key=$2&filter=deva&noLit=off&accent=no&transLit=slp1
RewriteRule ^entries/([^/]*)/([^/]*)$ http://www.sanskrit-lexicon.uni-koeln.de/scans/$1Scan/2014/web/webtc/getword.php?key=$2&filter=deva&noLit=off&accent=no&transLit=slp1
```

### 1.1.8. Questions

1. What is the purpose of noLit?
2. List of dictionaries still using 2013 display will have to be handled slightly differently. Their list is needed.
3. Any other missing parameter?



