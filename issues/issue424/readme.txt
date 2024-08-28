
Begin 08-27-2024

Ref: https://github.com/sanskrit-lexicon/COLOGNE/issues/424
This directory:
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue424

# -------------------------------------------------------------
Start with a copy of csl-orig/v02/bur/bur.txt at commit
  f8c6bf73209721fd43ed026d7b497eb5fefdaafb


# change to csl-orig repository on local installation
cd /c/xampp/htdocs/cologne/csl-orig/
# generate temp_bur_0 .txt in this directory
git show  f8c6bf73:v02/bur/bur.txt > /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue424/temp_bur_0.txt
# return to this directory
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue424


# -------------------------------------------------------------
# similarly copy bur_hwextra from csl-orig
cd /c/xampp/htdocs/COLOGNE/csl-orig/
git show  f8c6bf73:v02/bur/bur_hwextra.txt > /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue424/bur_hwextra.txt
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue424

only 1 instance.

--------------------------------------------------------
# displays PRIOR to changes.  burhwx  (uses bur_hwextra)
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh bur ../../burhwx
# local display url: http://localhost/cologne/burhwx/web/
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue424

--------------------------------------------------------
cd /c/xampp/htdocs/cologne/csl-orig/v02/bur
mkdir althws
mv bur_hwextra.txt althws/
touch bur_hwextra.txt
echo "2024-08-27. bur_hwextra.txt no longer used." >  althws/readme.txt

cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue424

---------------------------------
temp_bur_1.txt, bur_front.txt, bur_back.txt
Extract lines before first entry into bur_front.txt
Extract lines after last entry into bur_back.txt
Remove blank lines in the remaining, and write to temp_bur_1.txt

python frontback.py temp_bur_0.txt temp_bur_1.txt bur_front.txt bur_back.txt

135479 from temp_bur_0.txt
6 135477
skip_empty_lines 35062
100410 lines written to temp_bur_1.txt
6 lines written to bur_front.txt
1 lines written to bur_back.txt

--------------------------------------------------------
Remove all matter not within an entry

python middle.py temp_bur_1.txt temp_bur_1a.txt bur_middle.txt

100410 from temp_bur_1.txt
99477 lines written to temp_bur_1a.txt
933 lines written to bur_middle.txt

# Keep these 'just in case' of future use

cp bur_front.txt /c/xampp/htdocs/cologne/csl-orig/v02/bur/
cp bur_back.txt  /c/xampp/htdocs/cologne/csl-orig/v02/bur/
cp bur_middle.txt /c/xampp/htdocs/cologne/csl-orig/v02/bur/

--------------------------------------------------------
temp_bur_2.txt
check that all <info .*?/> markup in an entry occurs at the end of last line
Rewrite as needed.
Why?  For AB version.

python infotag.py temp_bur_1a.txt temp_bur_2.txt

Notes:
1. there are no <info /> tags in temp_bur_1a.txt
  So temp_bur_2.txt is same as temp_bur_1a.txt

--------------------------------------------------------
temp_bur_3.txt
Lbody form constructed from version 2 and bur_hwextra


First (and only) line:
<L>1043.1<pc>036,1<k1>aBAva<k2>aBAva<type>alt<LP>1043<k1P>aBava

----
# <pc> is not needed.  Adjust the parse in Extra __init__.

python convert_hwextra_lbody.py temp_bur_2.txt bur_hwextra.txt temp_bur_3.txt

99477 lines read from temp_bur_2.txt
19775 entries found
1 from bur_hwextra.txt
19776 records written to temp_bur_3.txt

(+ 19775 1) = 19776

-------------------------------------------------------
revise hw.py
edit /c/xampp/htdocs/cologne/csl-pywork/v02/makotemplates/pywork/hw.py
add 'bur' to the 'Lbody' list.
--------------------------------------------------------
# xml and display Versions using {{LBody=N}}
cp temp_bur_3.txt /c/xampp/htdocs/COLOGNE/csl-orig/v02/bur/bur.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
grep 'bur ' redo_xampp_all.sh
sh generate_dict.sh bur  ../../bur
sh xmlchk_xampp.sh bur
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue424

Visual compare displays (burhwx) to revised.
Looks fine.

********************************************************

Finish syncing and installation
-------------------------------
csl-orig

cd /c/xampp/htdocs/cologne/csl-orig/v02
git status
        modified:   bur/bur.txt
        modified:   bur/bur_hwextra.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        bur/althws/
        bur/bur_back.txt
        bur/bur_front.txt
        bur/bur_middle.txt

git add .

git commit -m "BUR: hwxetra-Lbody conversion.
Ref: https://github.com/sanskrit-lexicon/COLOGNE/issues/424"

git push

-------------------------------
csl-pywork
cd /c/xampp/htdocs/cologne/csl-pywork/v02
git status
        modified:   makotemplates/pywork/hw.py

git add .

git commit -m "BUR: hwxetra-Lbody conversion.
Ref: https://github.com/sanskrit-lexicon/COLOGNE/issues/424"

git push

cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue424

-------------------------------------
install revised bur on COLOGNE server

cd csl-orig
git pull

# revise displays for bur
cd csl-pywork/v02
git pull

sh generate_dict.sh bur  ../../BURScan/2020/

-----------------------
Sync this BUR repo
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue424

git add .
git commit -m "BUR: hwextra-Lbody conversion #424"
git push
=========================================================

