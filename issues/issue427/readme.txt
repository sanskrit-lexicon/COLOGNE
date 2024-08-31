
Begin 08-31-2024

Ref: https://github.com/sanskrit-lexicon/COLOGNE/issues/427
This directory:
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue427

# -------------------------------------------------------------
Start with a copy of csl-orig/v02/pw/pw.txt at commit
  40eb85cec6857f21f313ac623e50d8f5da640a5f

# change to csl-orig repository on local installation
cd /c/xampp/htdocs/cologne/csl-orig/
# generate temp_pw_0 .txt in this directory
git show  40eb85cec:v02/pw/pw.txt > /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue427/temp_pw_0.txt
# return to this directory
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue427

# -------------------------------------------------------------
# similarly copy pw_hwextra from csl-orig
cd /c/xampp/htdocs/COLOGNE/csl-orig/
git show  40eb85cec:v02/pw/pw_hwextra.txt > /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue427/pw_hwextra.txt
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue427

wc -l pw_hwextra.txt
12186 pw_hwextra.txt
# first two
<L>2.1<pc>1-001-a<k1>an<k2>2. a°, an°<type>alt<LP>2<k1P>a
<L>46.1<pc>1-001-b<k1>aMseBArika<k2>*aMseBAra, *aMseBArika<type>alt<LP>46<k1P>aMseBAra


--------------------------------------------------------
displays PRIOR to changes.  pwhwx  (uses pw_hwextra)
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh pw ../../pwhwx
sh xmlchk_xampp.sh pw
#
ok
# local display url: http://localhost/cologne/pwhwx/web/

cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue427

--------------------------------------------------------
cd /c/xampp/htdocs/cologne/csl-orig/v02/pw
mkdir althws
mv pw_hwextra.txt althws/
touch pw_hwextra.txt
echo "2024-08-27. pw_hwextra.txt no longer used." >  althws/readme.txt
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue427

---------------------------------
temp_pw_1.txt, pw_front.txt, pw_back.txt
Extract lines before first entry into pw_front.txt
Extract lines after last entry into pw_back.txt
Remove blank lines in the remaining, and write to temp_pw_1.txt

python frontback.py temp_pw_0.txt temp_pw_1.txt pw_front.txt pw_back.txt

764942 from temp_pw_0.txt
3 764941
skip_empty_lines 158377
606562 lines written to temp_pw_1.txt
3 lines written to pw_front.txt
0 lines written to pw_back.txt

--------------------------------------------------------
PW 
Extract additional front matter manually
Remove all matter not within an entry

python middle.py temp_pw_1.txt temp_pw_1a.txt pw_middle.txt

606562 from temp_pw_1.txt
606553 lines written to temp_pw_1a.txt
9 lines written to pw_middle.txt

# Keep these 'just in case' of future use

cp pw_front.txt /c/xampp/htdocs/cologne/csl-orig/v02/pw/
cp pw_back.txt  /c/xampp/htdocs/cologne/csl-orig/v02/pw/
cp pw_middle.txt /c/xampp/htdocs/cologne/csl-orig/v02/pw/

--------------------------------------------------------
temp_pw_2.txt
check that all <info .*?/> markup in an entry occurs at the end of last line
Rewrite as needed.
Why?  For AB version.

python infotag.py temp_pw_1a.txt temp_pw_2.txt
606553 lines read from temp_pw_1a.txt
158370 entries found
1 lines written to infotag_attr.txt
0 lines written to infotag_notend.txt
0 entries with non-standard info last line
revise_entries: 0 entries revised
158370 records written to temp_pw_2.txt

Notes:
grep '<info n="sup_' temp_pw_1a.txt | wc -l
22611

These info tags are already at end of last line,
so temp_pw_1a.txt is same as temp_pw_2.txt

--------------------------------------------------------
--------------------------------------------------------

--------------------------------------------------------
temp_pw_3.txt
Lbody form constructed from version 2 and pw_hwextra.txt

python convert_hwextra_lbody.py temp_pw_2.txt pw_hwextra.txt temp_pw_3.txt

(+ 47603 5839) = 53442


-------------------------------------------------------
convert pw metalines to cdsl standard form.
This is similar to the conversion for grassman
Ref: https://github.com/sanskrit-lexicon/GRA/tree/master/issues/issue34/readme.txt
at "revert to standard cdsl form for metaline"
cp /c/xampp/htdocs/sanskrit-lexicon/MWS/mwsissues/issue176/convert_ab1.py convert_metaline.py

In temp_pw_3,  there are
example:
temp_pw_3.txt
<L>2<pc>1-001-a<k1>a<k2>2. a°, an°
 [MISC. txt]
<LEND>
<L>2.1<pc>1-001-a<k1>an<k2>2. a°, an°
{{Lbody=2}}
<LEND>

NEW:
<L>2<pc>1-001-a<k1>a<k2>a°<h>2
 [MISC. txt]
<LEND>
<L>2.1<pc>1-001-a<k1>an<k2>an°
{{Lbody=2}}
<LEND>

------------------------------
commas in k2
21068 matches for "<k2>.*?," in buffer: temp_pw_3.txt
12185 matches for "{{Lbody" in buffer: temp_pw_3.txt

-------------------------------------------------------
temp_pw_4.txt


python convert_metaline_pw.py ab,cdsl temp_pw_3.txt temp_pw_4.txt temp_pw_3_groups.txt

643111 lines read from temp_pw_3.txt
170556 entries found
170556 records written to temp_pw_4.txt
170556 new entries written to temp_pw_4.txt


-------------------------------------------------------
# check consistency of k1 and k2 for all metalines
Write the metalines with inconsistency.

python check_k1_k2.py temp_pw_4.txt check_k1_k2.txt
643111 from temp_pw_4.txt
check_all_k2_k1 finds 0 inconsistencies
0 lines written to check_k1_k2.txt

This is the conversion from cdsl k2 to k1 for pw

def check_k1_k2(k1,k2):
 newk1 = re.sub(r"[*°/^\\()' 3-]",'',k2)
 return newk1 == k1

This is the conversion from k2 to k1 for pw
------------------------------------------------------

-------------------------------------------------------
revise hw.py
edit /c/xampp/htdocs/cologne/csl-pywork/v02/makotemplates/pywork/hw.py
add 'pw' to the 'Lbody' list.
--------------------------------------------------------
# xml and display Versions using {{LBody=N}}
cp temp_pw_4.txt /c/xampp/htdocs/COLOGNE/csl-orig/v02/pw/pw.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
grep 'pw ' redo_xampp_all.sh
sh generate_dict.sh pw  ../../pw
sh xmlchk_xampp.sh pw
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue427

Visual compare displays (pwhwx) to revised.
Looks ok. 

********************************************************

Finish syncing and installation
-------------------------------
csl-orig

cd /c/xampp/htdocs/cologne/csl-orig/v02
git status
        modified:   pw/althws/readme.txt
        modified:   pw/pw.txt
        modified:   pw/pw_hwextra.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        pw/althws/pw_hwextra.txt
        pw/pw_back.txt
        pw/pw_front.txt
        pw/pw_middle.txt

git add .

git commit -m "PW: hwxetra-Lbody conversion
Ref: https://github.com/sanskrit-lexicon/COLOGNE/issues/427"

git push

-------------------------------
csl-pywork
cd /c/xampp/htdocs/cologne/csl-pywork/v02
git status
        modified:   makotemplates/pywork/hw.py

git add .

git commit -m "PW: hwxetra-Lbody conversion.
Ref: https://github.com/sanskrit-lexicon/COLOGNE/issues/427"

git push

cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue427

-------------------------------------
install revised pw on COLOGNE server

cd csl-orig
git pull

# revise displays for pw
cd csl-pywork/v02
git pull

 grep pw redo_cologne_all.sh
sh generate_dict.sh pw  ../../PWScan/2020/

-----------------------
Sync this repo
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue427

git add .
git commit -m "PW: hwextra-Lbody conversion #427"
git push
=========================================================

********************************************************
THE END
