## list xml tags  in each dictionary

python xmltags.py <input> <output>
Input assumed to be one of the digitizations at Cologne
Output lists all xml-type tags, with counts.
For some details see comments in xmltags.py.

# To redo for one dictionary xxx
sh redo_one.sh xxx
# Relative file location designed to work on local installation

# Do redo for all 
sh redo_all.sh
# one file with all the tag frequencies for each dictionary
sh catall.sh > all_xmltags.txt
