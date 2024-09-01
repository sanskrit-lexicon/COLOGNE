
Begin 08-31-2024

Ref: https://github.com/sanskrit-lexicon/COLOGNE/issues/431
This directory:
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue431

# -------------------------------------------------------------
Start with a copy of csl-orig/v02/skd/skd.txt at commit
  f8c6bf73209721fd43ed026d7b497eb5fefdaafb

# change to csl-orig repository on local installation
cd /c/xampp/htdocs/cologne/csl-orig/
# generate temp_skd_0 .txt in this directory
git show  f8c6bf73:v02/skd/skd.txt > /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue431/temp_skd_0.txt
# return to this directory
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue431


# -------------------------------------------------------------
# similarly copy skd_hwextra from csl-orig
cd /c/xampp/htdocs/COLOGNE/csl-orig/
git show  f8c6bf73:v02/skd/skd_hwextra.txt > /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue431/skd_hwextra.txt
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue431

wc -l skd_hwextra.txt
335 skd_hwextra.txt

Sample:
<L>8094.01<k1>kuveraH<k2>kuveraH<type>alt<LP>8094<k1P>kuberaH
<L>10108.01<k1>KarvvaH<k2>KarvvaH<type>alt<LP>10108<k1P>KarbbaH


--------------------------------------------------------
# displays PRIOR to changes.  skdhwx  (uses skd_hwextra)
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh skd ../../skdhwx
# local display url: http://localhost/cologne/skdhwx/web/
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue431

--------------------------------------------------------
cd /c/xampp/htdocs/cologne/csl-orig/v02/skd
mkdir althws
mv skd_hwextra.txt althws/
touch skd_hwextra.txt
echo "2024-08-31. skd_hwextra.txt no longer used." >  althws/readme.txt

cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue431

---------------------------------
temp_skd_1.txt, skd_front.txt, skd_back.txt
Extract lines before first entry into skd_front.txt
Extract lines after last entry into skd_back.txt
Remove blank lines in the remaining, and write to temp_skd_1.txt

python frontback.py temp_skd_0.txt temp_skd_1.txt skd_front.txt skd_back.txt
580774 from temp_skd_0.txt
2 580773
skip_empty_lines 0
580772 lines written to temp_skd_1.txt
2 lines written to skd_front.txt
0 lines written to skd_back.txt


--------------------------------------------------------
Remove all matter not within an entry

python middle.py temp_skd_1.txt temp_skd_1a.txt skd_middle.txt

580772 from temp_skd_1.txt
578957 lines written to temp_skd_1a.txt
1815 lines written to skd_middle.txt

# Keep these 'just in case' of future use

cp skd_front.txt /c/xampp/htdocs/cologne/csl-orig/v02/skd/
cp skd_back.txt  /c/xampp/htdocs/cologne/csl-orig/v02/skd/
cp skd_middle.txt /c/xampp/htdocs/cologne/csl-orig/v02/skd/

--------------------------------------------------------
temp_skd_2.txt
check that all <info .*?/> markup in an entry occurs at the end of last line
Rewrite as needed.
Why?  For AB version.

python infotag.py temp_skd_1a.txt temp_skd_2.txt

Notes:
1. there are no <info /> tags in temp_skd_1a.txt
  So temp_skd_2.txt is same as temp_skd_1a.txt

--------------------------------------------------------

temp_skd_3.txt
Lbody form constructed from version 2 and skd_hwextra

python convert_hwextra_lbody.py temp_skd_2.txt skd_hwextra.txt temp_skd_3.txt

578957 lines read from temp_skd_2.txt
42196 entries found
335 from skd_hwextra.txt
42531 records written to temp_skd_3.txt

-------------------------------------------------------
check k1-k2 consistency
python check_k1_k2.py temp_skd_3.txt check_k1_k2.txt

579962 from temp_skd_3.txt
check_all_k2_k1 finds 349 inconsistencies
349 lines written to check_k1_k2.txt

-------------------------------------------------------

I think most of these inconsistencies are in the first
record of groups of alternates, and can be corrected
by merely remove a parenthetica expression in k2

Example:
OLD: <L>15901<pc>2-681-a<k1>daDisaktavaH<k2>daDisa(Sa)ktavaH
NEW: <L>15901<pc>2-681-a<k1>daDisaktavaH<k2>daDisaktavaH

Will write a program to do this.

python k2_paren.py temp_skd_3.txt temp_skd_4.txt

579962 from temp_skd_3.txt
remove_k2_parens: 345 lines changed
579962 lines written to temp_skd_4.txt

-----

python check_k1_k2.py temp_skd_4.txt check_k1_k2_4.txt

579962 from temp_skd_4.txt
check_all_k2_k1 finds 6 inconsistencies
6 lines written to check_k1_k2_4.txt

----------------------------
temp_skd_5.txt  correct those 6
cp temp_skd_4.txt temp_skd_5.txt
manual edit temp_skd_5.txt
<L>3648<pc>1-185-b<k1>AyattiH<k2>AyattiH:  remove colon
<L>17250<pc>2-758-b<k1>draviqI<k2>draviqI;  remove semicolon
<L>18724<pc>2-865-b<k1>nArA<k2>nArA;  remove semicolon
<L>20119<pc>3-026-b<k1>patraM<k2>pattraM  patraM
<L>22221<pc>3-222-a<k1>pUrvvaH<k2>pUrbbaH  k1=pUrbbaH
<L>41771<pc>5-537-a<k1>hiqaM<k2>hiqa  hiqaM

check

python check_k1_k2.py temp_skd_5.txt check_k1_k2_5.txt

579962 from temp_skd_5.txt
check_all_k2_k1 finds 0 inconsistencies
0 lines written to check_k1_k2_5.txt

Ready to install version 5
-------------------------------------------------------
revise hw.py
edit /c/xampp/htdocs/cologne/csl-pywork/v02/makotemplates/pywork/hw.py
add 'skd' to the 'Lbody' list.

--------------------------------------------------------
# xml and display Versions using {{LBody=N}}
cp temp_skd_5.txt /c/xampp/htdocs/COLOGNE/csl-orig/v02/skd/skd.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
grep 'skd ' redo_xampp_all.sh
sh generate_dict.sh skd  ../../skd
sh xmlchk_xampp.sh skd
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue431

Visual compare displays (skdhwx) to revised.
Looks fine.

********************************************************

Finish syncing and installation
-------------------------------
csl-orig

cd /c/xampp/htdocs/cologne/csl-orig/v02
git status
        modified:   skd/skd.txt
        modified:   skd/skd_hwextra.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        skd/althws/
        skd/skd_back.txt
        skd/skd_front.txt
        skd/skd_middle.txt

git add .

git commit -m "SKD: hwxetra-Lbody conversion.
Ref: https://github.com/sanskrit-lexicon/COLOGNE/issues/431"

git push

-------------------------------
csl-pywork
cd /c/xampp/htdocs/cologne/csl-pywork/v02
git status
        modified:   makotemplates/pywork/hw.py

git add .

git commit -m "SKD: hwxetra-Lbody conversion.
Ref: https://github.com/sanskrit-lexicon/COLOGNE/issues/431"

git push

cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue431

-------------------------------------
install revised skd on COLOGNE server

cd csl-orig
git pull

# revise displays for skd
cd csl-pywork/v02
git pull

sh generate_dict.sh skd  ../../SKDScan/2020/

-----------------------
Sync this SKD repo
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue431

git add .
git commit -m "SKD: hwextra-Lbody conversion #431"
git push
=========================================================

