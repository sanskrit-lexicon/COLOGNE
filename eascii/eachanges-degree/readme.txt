Code to generate, apply, and install changes.
Change the MASCULINE ORDINAL INDICATOR character º
to the DEGREE SIGN character °

These are the dictionaries changed, and the preliminary number
of occurrences (within entries - i.e. excluding front matter, etc.)
acc 46, ap90 4050, ben 506, gst 205, ieg 45
inm 19532, krm 1, mci 65, yat 2
mw72 21109, pwg 4 , shs 3, vei 10  

However, we also make the change in front matter, etc. as well as withn entries.
  and note the number of changes in these two sections.
Sample:
python make_change.py ../../../../cologne/csl-orig/v02/acc/acc.txt changes/acc_changes.txt


python make_change.py ../../../../cologne/csl-orig/v02/ap90/ap90.txt temp_ap90_changes.txt

sh redo_changes.sh > log_changes.txt

For each dictionary, generate change transactions and apply the changes.
The change transactions are in file changes/xxx_changes.txt.
The revised digitization is in file temporig/xxx.txt

sh copy_orig.sh
 # copies all the new digitizations to csl-orig
 
