
It is desireable to have supplementary materials for the IAST representation
of Sanskrit, since there are numerous extensions to the standard described
in https://en.wikipedia.org/wiki/International_Alphabet_of_Sanskrit_Transliteration.

These materials not only exhibit the relations between the slp1 and iast (roman) representations of Sanskrit, but also provide a source from which one
may 'copy and paste' text into dictionaries that have embedded IAST.

The slp1_roman.xml file herein is the source of truth for the current Cologne
dictionaries.  This file should agree with copies used by php programs that generate Cologne displays:

* (for simple search) in csl-apidev repository: e.g. [slp1_roman.xml](https://github.com/sanskrit-lexicon/csl-apidev/blob/master/utilities/transcoder/slp1_roman.xml)
* (for basic, adv. search, etc ) in csl-websanlexicon repository e.g. [slp1_roman.xml](https://github.com/sanskrit-lexicon/csl-websanlexicon/blob/master/v02/makotemplates/web/utilities/transcoder/slp1_roman.xml).



python slp1_iast.py slp1_roman.xml slp1_iast.txt
