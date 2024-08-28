
Begin 08-27-2024

Ref: https://github.com/sanskrit-lexicon/COLOGNE/issues/423
This directory:
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue423

# -------------------------------------------------------------
Start with a copy of csl-orig/v02/ap90/ap90.txt at commit
  40eb85cec6857f21f313ac623e50d8f5da640a5f


# change to csl-orig repository on local installation
cd /c/xampp/htdocs/cologne/csl-orig/
# generate temp_ap90_0 .txt in this directory
git show  40eb85cec:v02/ap90/ap90.txt > /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue423/temp_ap90_0.txt
# return to this directory
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue423


# -------------------------------------------------------------
# similarly copy ap90_hwextra from csl-orig
cd /c/xampp/htdocs/COLOGNE/csl-orig/
git show  40eb85cec:v02/ap90/ap90_hwextra.txt > /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue423/ap90_hwextra.txt
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue423

--------------------------------------------------------
displays PRIOR to changes.  ap90hwx  (uses ap90_hwextra)
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh ap90 ../../ap90hwx
# local display url: http://localhost/cologne/ap90hwx/web/
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue423

--------------------------------------------------------
cd /c/xampp/htdocs/cologne/csl-orig/v02/ap90
mkdir althws
mv ap90_hwextra.txt althws/
touch ap90_hwextra.txt
echo "2024-08-27. ap90_hwextra.txt no longer used." >  althws/readme.txt

---------------------------------
temp_ap90_1.txt, ap90_front.txt, ap90_back.txt
Extract lines before first entry into ap90_front.txt
Extract lines after last entry into ap90_back.txt
Remove blank lines in the remaining, and write to temp_ap90_1.txt

python frontback.py temp_ap90_0.txt temp_ap90_1.txt ap90_front.txt ap90_back.txt


--------------------------------------------------------
AP90 
Extract additional front matter manually
Remove all matter not within an entry

python middle.py temp_ap90_1.txt temp_ap90_1a.txt ap90_middle.txt

266259 from temp_ap90_1.txt
264230 lines written to temp_ap90_1a.txt
2029 lines written to ap90_middle.txt

# Keep these 'just in case' of future use

cp ap90_front.txt /c/xampp/htdocs/cologne/csl-orig/v02/ap90/
cp ap90_back.txt  /c/xampp/htdocs/cologne/csl-orig/v02/ap90/
cp ap90_middle.txt /c/xampp/htdocs/cologne/csl-orig/v02/ap90/

--------------------------------------------------------
temp_ap90_2.txt
check that all <info .*?/> markup in an entry occurs at the end of last line
Rewrite as needed.
Why?  For AB version.

python infotag.py temp_ap90_1a.txt temp_ap90_2.txt

Notes:
1. there are no <info /> tags in temp_ap90_1a.txt
  So temp_ap90_2.txt is same as temp_ap90_1a.txt

--------------------------------------------------------
temp_ap90_3.txt
Lbody form constructed from version 2 and ap90_hwextra

ap90_hwextra.txt 465 items.

First 2 lines:
<L>185.01<pc>0009-b<k1>agatIka<k2>agatIka<type>alt<LP>185<k1P>agatika<ln1>2702<ln2>2709
<L>313.01<pc>0021-b<k1>aMhriH<k2>aMhriH<type>alt<LP>313<k1P>aMGri<ln1>5226<ln2>5242

----
# <pc>, <ln1> and <ln2> are not needed.  Adjust the parse in Extra __init__.

python convert_hwextra_lbody.py temp_ap90_2.txt ap90_hwextra.txt temp_ap90_3.txt

264230 lines read from temp_ap90_2.txt
31720 entries found
465 from ap90_hwextra.txt
32176 records written to temp_ap90_3.txt

(+ 31720 465) 32185

Q: Why not 49822 ?  
A: 9 comment lines (starting with ';') in ap90_hwextra.txt

-------------------------------------------------------
revise hw.py
edit /c/xampp/htdocs/cologne/csl-pywork/v02/makotemplates/pywork/hw.py
add 'ap90' to the 'Lbody' list.
--------------------------------------------------------
# xml and display Versions using {{LBody=N}}
cp temp_ap90_3.txt /c/xampp/htdocs/COLOGNE/csl-orig/v02/ap90/ap90.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
grep 'ap90 ' redo_xampp_all.sh
sh generate_dict.sh ap90  ../../ap90
sh xmlchk_xampp.sh ap90
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue423

Visual compare displays (ap90hwx) to revised.
Looks fine.

********************************************************

Finish syncing and installation
-------------------------------
csl-orig

cd /c/xampp/htdocs/cologne/csl-orig/v02
git status
        modified:   ap90/ap90.txt
        modified:   ap90/ap90_hwextra.txt

        Untracked files:
        (use "git add <file>..." to include in what will be committed)
        ap90/althws/
        ap90/ap90_back.txt
        ap90/ap90_front.txt
        ap90/ap90_middle.txt


git add .

git commit -m "AP90: hwxetra-Lbody conversion.
Ref: https://github.com/sanskrit-lexicon/COLOGNE/issues/423"

git push

-------------------------------
csl-pywork
cd /c/xampp/htdocs/cologne/csl-pywork/v02
git status
        modified:   makotemplates/pywork/hw.py

git add .

git commit -m "AP90: hwxetra-Lbody conversion.
Ref: https://github.com/sanskrit-lexicon/COLOGNE/issues/423"

git push

cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue423

-------------------------------------
install revised ap90 on COLOGNE server

cd csl-orig
git pull

# revise displays for ap90
cd csl-pywork/v02
git pull

sh generate_dict.sh ap90  ../../AP90Scan/2020/

-----------------------
Sync this AP90 repo
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue423

git add .
git commit -m "AP90: hwextra-Lbody conversion #423"
git push
=========================================================

