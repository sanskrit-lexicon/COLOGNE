
Begin 08-28-2024

Ref: https://github.com/sanskrit-lexicon/COLOGNE/issues/426
This directory:
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue426

# -------------------------------------------------------------
Start with a copy of csl-orig/v02/lrv/lrv.txt at commit
  40eb85cec6857f21f313ac623e50d8f5da640a5f

# change to csl-orig repository on local installation
cd /c/xampp/htdocs/cologne/csl-orig/
# generate temp_lrv_0 .txt in this directory
git show  40eb85cec:v02/lrv/lrv.txt > /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue426/temp_lrv_0.txt
# return to this directory
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue426


# -------------------------------------------------------------
# similarly copy lrv_hwextra from csl-orig
cd /c/xampp/htdocs/COLOGNE/csl-orig/
git show  40eb85cec:v02/lrv/lrv_hwextra.txt > /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue426/lrv_hwextra.txt
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue426

wc -l lrv_hwextra.txt
5838 lrv_hwextra.txt
# first two
<L>00085.1<pc>002-32<k1>akUvAra<k2>akUpA(vA)ra<type>alt<LP>00085<k1P>akUpAra
<L>00163.1<pc>003-10<k1>akzIva<k2>akzi(kzI)va<type>alt<LP>00163<k1P>akziva

--------------------------------------------------------
displays PRIOR to changes.  lrvhwx  (uses lrv_hwextra)
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh lrv ../../lrvhwx
sh xmlchk_xampp.sh lrv
#
ok
# local display url: http://localhost/cologne/lrvhwx/web/

cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue426

--------------------------------------------------------
cd /c/xampp/htdocs/cologne/csl-orig/v02/lrv
mkdir althws
mv lrv_hwextra.txt althws/
touch lrv_hwextra.txt
echo "2024-08-27. lrv_hwextra.txt no longer used." >  althws/readme.txt
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue426

---------------------------------
temp_lrv_1.txt, lrv_front.txt, lrv_back.txt
Extract lines before first entry into lrv_front.txt
Extract lines after last entry into lrv_back.txt
Remove blank lines in the remaining, and write to temp_lrv_1.txt

python frontback.py temp_lrv_0.txt temp_lrv_1.txt lrv_front.txt lrv_back.txt

190412 from temp_lrv_0.txt
0 190410
skip_empty_lines 47602
142809 lines written to temp_lrv_1.txt
0 lines written to lrv_front.txt
1 lines written to lrv_back.txt


--------------------------------------------------------
LRV 
Extract additional front matter manually
Remove all matter not within an entry

python middle.py temp_lrv_1.txt temp_lrv_1a.txt lrv_middle.txt

142809 from temp_lrv_1.txt
142809 lines written to temp_lrv_1a.txt
0 lines written to lrv_middle.txt


# Keep these 'just in case' of future use

cp lrv_front.txt /c/xampp/htdocs/cologne/csl-orig/v02/lrv/
cp lrv_back.txt  /c/xampp/htdocs/cologne/csl-orig/v02/lrv/
cp lrv_middle.txt /c/xampp/htdocs/cologne/csl-orig/v02/lrv/

--------------------------------------------------------
temp_lrv_2.txt
check that all <info .*?/> gmarkup in an entry occurs at the end of last line
Rewrite as needed.
Why?  For AB version.

python infotag.py temp_lrv_1a.txt temp_lrv_2.txt

Notes:
1. there are no <info /> tags in temp_lrv_1a.txt
  So temp_lrv_2.txt is same as temp_lrv_1a.txt


--------------------------------------------------------
lrv_hwextra_edit/txt

cp lrv_hwextra.txt lrv_hwextra_edit.txt
# manual edit

Correct inconsistencies uncovered by hwextra_adj.py program below.

diff lrv_hwextra.txt lrv_hwextra_edit.txt | wc -l
153
Approximately 40 lines changed. (out of 5839)
--------------------------------------------------------
lrv_hwextra_adj.txt

The given file has parenthetical groups somehow showing alternates.
The convention for 'k2' field in most (all?) cdsl dictionaries is that
k2 should 'generate' k1 by a simple algorithm (e.g. drop '-' in k2).
lrv_hwextra_adj.txt does this, by various ad-hoc rules (m0,m1,..,m14  see below for counts)
Here si application of rule 1.
OLD:
<L>00085.1<pc>002-32<k1>akUvAra<k2>akUpA(vA)ra<type>alt<LP>00085<k1P>akUpAra
<L>00163.1<pc>003-10<k1>akzIva<k2>akzi(kzI)va<type>alt<LP>00163<k1P>akziva
NEW:

<L>00085.1<pc>002-32<k1>akUvAra<k2>akUvAra<type>alt<LP>00085<k1P>akUpAra
<L>00163.1<pc>003-10<k1>akzIva<k2>akzIva<type>alt<LP>00163<k1P>akziva

python hwextra_adj.py lrv_hwextra_edit.txt lrv_hwextra_adj.txt lrv_hwextra_adj_method.txt
5839 from lrv_hwextra_edit.txt
5839 lines written to lrv_hwextra_adj.txt
5839 lines written to lrv_hwextra_adj_method.txt
0 lines written to temp_problem.txt
None 0
m0 10
m1 5374
m2 266
m3 59
m4 14
m5 9
m6 6
m7 25
m8 27
m9 8
m10 2
m11 7
m12 11
m13 21

--------------------------------------------------------
temp_lrv_3.txt
Lbody form constructed from version 2 and lrv_hwextra_adj.txt

lrv_hwextra.txt 1 item

python convert_hwextra_lbody.py temp_lrv_2.txt lrv_hwextra_adj.txt temp_lrv_3.txt

142809 lines read from temp_lrv_2.txt
47603 entries found
5839 from lrv_hwextra_adj.txt
5839  len of extras
5839 entriesx created
53442 records written to temp_lrv_3.txt

(+ 47603 5839) = 53442


-------------------------------------------------------
temp_lrv_4.txt

Another adjustment to the Parent k2 which have parenthesis.

242 matches for "k2>.*(.*-" in buffer: temp_lrv_3.txt


example:
OLD:
<L>00415<pc>006-27<k1>aMgulitoraRa<k2>aMguli(lI)-toraRa
NEW:
<L>00415<pc>006-27<k1>aMgulitoraRa<k2>aMguli-toraRa

python k2_paren.py temp_lrv_3.txt temp_lrv_4.txt

160326 from temp_lrv_3.txt
remove_k2_parens: 793 lines changed
160326 lines written to temp_lrv_4.txt

check_all_k2_k1 finds 5887 inconsistencies
-------------------------------------------------------
# check consistency of k1 and k2 for all metalines
Write the metalines with inconsistency.

python check_k1_k2.py temp_lrv_4.txt check_k1_k2.txt
check_all_k2_k1 finds 5887 inconsistencies
5887 lines written to check_k1_k2.txt

-------------------------------------------------------
python k1k2_change.py

python k1k2_change.py temp_lrv_4.txt change_lrv_5.txt temp_k1k2_change.txt

Add correction to change_lrv_5.txt
; Case 5887 Last case special  - bad invisible character in temp_lrv_4.txt in k1
; oldk1: brahma‌fzi  (invisible char between 'a' and 'f')
; newk1: brahmafzi
98848 old <L>26791<pc>512-24<k1>brahma‌fzi<k2>brahmafzi
98848 new <L>26791<pc>512-24<k1>brahmafzi<k2>brahmafzi

# temp_lrv_5.txt : apply the change file
python updateByLine.py temp_lrv_4.txt change_lrv_5.txt temp_lrv_5.txt

160326 lines read from temp_lrv_4.txt
160326 records written to temp_lrv_5.txt
5887 change transactions from change_lrv_5.txt
5887 of type new

# confirm version 5 no k2-k1 inconsistencies
python check_k1_k2.py temp_lrv_5.txt temp.txt

160326 from temp_lrv_5.txt
check_all_k2_k1 finds 0 inconsistencies
0 lines written to temp.txt

-------------------------------------------------------
revise hw.py
edit /c/xampp/htdocs/cologne/csl-pywork/v02/makotemplates/pywork/hw.py
add 'lrv' to the 'Lbody' list.
--------------------------------------------------------
# xml and display Versions using {{LBody=N}}
cp temp_lrv_5.txt /c/xampp/htdocs/COLOGNE/csl-orig/v02/lrv/lrv.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
grep 'lrv ' redo_xampp_all.sh
sh generate_dict.sh lrv  ../../lrv
sh xmlchk_xampp.sh lrv
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue426

Visual compare displays (lrvhwx) to revised.
Looks ok. (But see note at bottom of this file at
 "Possible problems with lrv."

********************************************************

Finish syncing and installation
-------------------------------
csl-orig

cd /c/xampp/htdocs/cologne/csl-orig/v02
git status
        modified:   lrv/lrv.txt
        modified:   lrv/lrv_hwextra.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        lrv/althws/
        lrv/lrv_back.txt
        lrv/lrv_front.txt
        lrv/lrv_middle.txt


git add .

git commit -m "LRV: hwxetra-Lbody conversion.
Ref: https://github.com/sanskrit-lexicon/COLOGNE/issues/426"

git push

-------------------------------
csl-pywork
cd /c/xampp/htdocs/cologne/csl-pywork/v02
git status
        modified:   makotemplates/pywork/hw.py

git add .

git commit -m "LRV: hwxetra-Lbody conversion.
Ref: https://github.com/sanskrit-lexicon/COLOGNE/issues/426"

git push

cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue426

-------------------------------------
install revised lrv on COLOGNE server

cd csl-orig
git pull

# revise displays for lrv
cd csl-pywork/v02
git pull

 grep lrv redo_cologne_all.sh
sh generate_dict.sh lrv  ../../LRVScan/2022/

-----------------------
Sync this repo
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue426

git add .
git commit -m "LRV: hwextra-Lbody conversion #426"
git push
=========================================================

********************************************************
Possible problems with lrv.
1. <pc>001-04    What is -NN ?   Not a column
2. In displays, the body line header (before broken bar)
   does NOT have <s>X</s> --- thus displays always show the slp1 spelling!
3. Avagraha in k1
