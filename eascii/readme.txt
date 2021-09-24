## list extended ascii characters  in each dictionary

python ea.py <input> <output>
Input assumed to be one of the digitizations at Cologne
Output lists all extended ascii characters, with counts.
Only considers lines within an 'entry',
 i.e., the metaline and lines between the metaline and the '<LEND>' line.
Thus, excludes characters in digitization of front-matter, appendices, etc.
that are not within an entry.

# To redo for one dictionary xxx
sh redo_one.sh xxx
# Relative file location designed to work on local installation
# output is a file in eadata directory.

# Do redo for all 
sh redo_all.sh
# all_ea.txt : all the ea frequencies for each dictionary
sh catall.sh > all_ea.txt

# another view of which dictionaries have each extended ascii character.
# dictlos variable has list of dictionary codes. excludes restricted dictionaries
# generate easummary_greek.tsv, easummary_arabic.tsv, easummary_cyrillic.tsv, easummary.tsv
python easummary.py ../../../cologne/csl-orig easummary

# Consider ONLY the metalines
# generate easummary_meta.tsv
python easummary_meta.py ../../../cologne/csl-orig easummary_meta

Unicode blocks:
03  GREEK and COPTIC
04  Cyrillic
1f  GREEK EXTENDED
06  Arabic
A640..A69F	Cyrillic Extended-B
0080-00ff  Latin-1 Supplement
01  Latin Extended-A
