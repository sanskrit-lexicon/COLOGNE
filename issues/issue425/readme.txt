
Begin 08-27-2024

Ref: https://github.com/sanskrit-lexicon/COLOGNE/issues/425
This directory:
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue425

# -------------------------------------------------------------
Start with a copy of csl-orig/v02/cae/cae.txt at commit
  40eb85cec6857f21f313ac623e50d8f5da640a5f


# change to csl-orig repository on local installation
cd /c/xampp/htdocs/cologne/csl-orig/
# generate temp_cae_0 .txt in this directory
git show  40eb85cec:v02/cae/cae.txt > /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue425/temp_cae_0.txt
# return to this directory
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue425


# -------------------------------------------------------------
# similarly copy cae_hwextra from csl-orig
cd /c/xampp/htdocs/COLOGNE/csl-orig/
git show  40eb85cec:v02/cae/cae_hwextra.txt > /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue425/cae_hwextra.txt
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue425

only 1 instance:
<L>14238.1<k1>duha<k2>duha<type>alt<LP>14238<k1P>duh

--------------------------------------------------------
displays PRIOR to changes.  caehwx  (uses cae_hwextra)
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh cae ../../caehwx
# local display url: http://localhost/cologne/caehwx/web/
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue425

--------------------------------------------------------
cd /c/xampp/htdocs/cologne/csl-orig/v02/cae
mkdir althws
mv cae_hwextra.txt althws/
touch cae_hwextra.txt
echo "2024-08-27. cae_hwextra.txt no longer used." >  althws/readme.txt
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue425

---------------------------------
temp_cae_1.txt, cae_front.txt, cae_back.txt
Extract lines before first entry into cae_front.txt
Extract lines after last entry into cae_back.txt
Remove blank lines in the remaining, and write to temp_cae_1.txt

python frontback.py temp_cae_0.txt temp_cae_1.txt cae_front.txt cae_back.txt

177428 from temp_cae_0.txt
3 177426
skip_empty_lines 41087
136337 lines written to temp_cae_1.txt
3 lines written to cae_front.txt
1 lines written to cae_back.txt


--------------------------------------------------------
CAE 
Extract additional front matter manually
Remove all matter not within an entry

python middle.py temp_cae_1.txt temp_cae_1a.txt cae_middle.txt

136337 from temp_cae_1.txt
135793 lines written to temp_cae_1a.txt
544 lines written to cae_middle.txt

[Page...]

# Keep these 'just in case' of future use

cp cae_front.txt /c/xampp/htdocs/cologne/csl-orig/v02/cae/
cp cae_back.txt  /c/xampp/htdocs/cologne/csl-orig/v02/cae/
cp cae_middle.txt /c/xampp/htdocs/cologne/csl-orig/v02/cae/

--------------------------------------------------------
temp_cae_2.txt
check that all <info .*?/> gmarkup in an entry occurs at the end of last line
Rewrite as needed.
Why?  For AB version.

python infotag.py temp_cae_1a.txt temp_cae_2.txt

Notes:
1. there are no <info /> tags in temp_cae_1a.txt
  So temp_cae_2.txt is same as temp_cae_1a.txt

--------------------------------------------------------
temp_cae_3.txt
Lbody form constructed from version 2 and cae_hwextra

cae_hwextra.txt 1 item

Only line:
<L>14238.1<k1>duha<k2>duha<type>alt<LP>14238<k1P>duh

----
# <pc>, <ln1> and <ln2> are not needed.  Adjust the parse in Extra __init__.

python convert_hwextra_lbody.py temp_cae_2.txt cae_hwextra.txt temp_cae_3.txt

135793 lines read from temp_cae_2.txt
40068 entries found
1 from cae_hwextra.txt
40069 records written to temp_cae_3.txt


-------------------------------------------------------
revise hw.py
edit /c/xampp/htdocs/cologne/csl-pywork/v02/makotemplates/pywork/hw.py
add 'cae' to the 'Lbody' list.
--------------------------------------------------------
# xml and display Versions using {{LBody=N}}
cp temp_cae_3.txt /c/xampp/htdocs/COLOGNE/csl-orig/v02/cae/cae.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
grep 'cae ' redo_xampp_all.sh
sh generate_dict.sh cae  ../../cae
sh xmlchk_xampp.sh cae
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue425

Visual compare displays (caehwx) to revised.
Looks fine.

********************************************************

Finish syncing and installation
-------------------------------
csl-orig

cd /c/xampp/htdocs/cologne/csl-orig/v02
git status
        modified:   cae/cae.txt
        modified:   cae/cae_hwextra.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        cae/althws/
        cae/cae_back.txt
        cae/cae_front.txt
        cae/cae_middle.txt


git add .

git commit -m "CAE: hwxetra-Lbody conversion.
Ref: https://github.com/sanskrit-lexicon/COLOGNE/issues/425"

git push

-------------------------------
csl-pywork
cd /c/xampp/htdocs/cologne/csl-pywork/v02
git status
        modified:   makotemplates/pywork/hw.py

git add .

git commit -m "CAE: hwxetra-Lbody conversion.
Ref: https://github.com/sanskrit-lexicon/COLOGNE/issues/425"

git push

cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue425

-------------------------------------
install revised cae on COLOGNE server

cd csl-orig
git pull

# revise displays for cae
cd csl-pywork/v02
git pull

sh generate_dict.sh cae  ../../CAEScan/2020/

-----------------------
Sync this repo
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue425

git add .
git commit -m "CAE: hwextra-Lbody conversion #425"
git push
=========================================================

