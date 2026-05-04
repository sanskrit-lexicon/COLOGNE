## list xml tags  in each dictionary

Ref: https://github.com/sanskrit-lexicon/COLOGNE/issues/366

python xmltag.py <input> <output>
Input assumed to be one of the digitizations at Cologne
Output lists all xml-type tags, with counts.
For some details see comments in xmltag.py.

# To redo for one dictionary xxx
sh redo_one.sh xxx
# Relative file location designed to work on local installation

# Do redo for all 
sh redo_all.sh
# one file with all the tag frequencies for each dictionary
sh catall.sh > all_xmltags.txt

------------------------------
chgtag.py:  Generate all instances of <chg...</chg> in xxx.txt
 for a given dictionary xxx

python chgtag.py ../../../cologne/csl-orig/v02/gra/gra.txt chgtag_gra.txt
381 instances written to chgtag_gra.txt

python chgtag.py ../../../cologne/csl-orig/v02/mw/mw.txt chgtag_mw.txt
39 instances written to chgtag_mw.txt
