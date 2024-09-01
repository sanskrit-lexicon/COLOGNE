
Begin 08-31-2024

Ref: https://github.com/sanskrit-lexicon/COLOGNE/issues/429
This directory:
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue429

# -------------------------------------------------------------
Start with a copy of csl-orig/v02/shs/shs.txt at commit
  f8c6bf73209721fd43ed026d7b497eb5fefdaafb

# change to csl-orig repository on local installation
cd /c/xampp/htdocs/cologne/csl-orig/
# generate temp_shs_0 .txt in this directory
git show  f8c6bf73:v02/shs/shs.txt > /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue429/temp_shs_0.txt
# return to this directory
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue429


# -------------------------------------------------------------
# similarly copy shs_hwextra from csl-orig
cd /c/xampp/htdocs/COLOGNE/csl-orig/
git show  f8c6bf73:v02/shs/shs_hwextra.txt > /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue429/shs_hwextra.txt
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue429

wc -l shs_hwextra.txt
13 shs_hwextra.txt

Sample:
<L>2187.01<pc>039-b<k1>apAYc<k2>apAYc<type>alt<LP>2187<k1P>apAc<ln1>9099<ln2>9101
<L>3938.01<pc>068-b<k1>avAYc<k2>avAYc<type>alt<LP>3938<k1P>avAc<ln1>16170<ln2>16175

--------------------------------------------------------
# displays PRIOR to changes.  shshwx  (uses shs_hwextra)
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh shs ../../shshwx
# local display url: http://localhost/cologne/shshwx/web/
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue429

--------------------------------------------------------
cd /c/xampp/htdocs/cologne/csl-orig/v02/shs
mkdir althws
mv shs_hwextra.txt althws/
touch shs_hwextra.txt
echo "2024-08-31. shs_hwextra.txt no longer used." >  althws/readme.txt

cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue429

---------------------------------
temp_shs_1.txt, shs_front.txt, shs_back.txt
Extract lines before first entry into shs_front.txt
Extract lines after last entry into shs_back.txt
Remove blank lines in the remaining, and write to temp_shs_1.txt

python frontback.py temp_shs_0.txt temp_shs_1.txt shs_front.txt shs_back.txt

196776 from temp_shs_0.txt
98 196775
skip_empty_lines 0
196678 lines written to temp_shs_1.txt
98 lines written to shs_front.txt
0 lines written to shs_back.txt

--------------------------------------------------------
Remove all matter not within an entry

python middle.py temp_shs_1.txt temp_shs_1a.txt shs_middle.txt

196678 from temp_shs_1.txt
195394 lines written to temp_shs_1a.txt
1284 lines written to shs_middle.txt

# Keep these 'just in case' of future use

cp shs_front.txt /c/xampp/htdocs/cologne/csl-orig/v02/shs/
cp shs_back.txt  /c/xampp/htdocs/cologne/csl-orig/v02/shs/
cp shs_middle.txt /c/xampp/htdocs/cologne/csl-orig/v02/shs/

--------------------------------------------------------
temp_shs_2.txt
check that all <info .*?/> markup in an entry occurs at the end of last line
Rewrite as needed.
Why?  For AB version.

python infotag.py temp_shs_1a.txt temp_shs_2.txt

Notes:
1. there are no <info /> tags in temp_shs_1a.txt
  So temp_shs_2.txt is same as temp_shs_1a.txt

--------------------------------------------------------

temp_shs_3.txt
Lbody form constructed from version 2 and shs_hwextra

python convert_hwextra_lbody.py temp_shs_2.txt shs_hwextra.txt temp_shs_3.txt

195394 lines read from temp_shs_2.txt
47313 entries found
13 from shs_hwextra.txt
47326 records written to temp_shs_3.txt

(+ 47313 13) = 47326

-------------------------------------------------------
check k1-k2 consistency
python check_k1_k2.py temp_shs_3.txt check_k1_k2.txt

check_all_k2_k1 finds 844 inconsistencies
844 lines written to check_k1_k2.txt

Most are where alternates are in parentheses in k2
Example: <L>23619<pc>428-a<k1>pariba<k2>pariba(-va)rha
The k1 also is wrong. Should be
<L>23619<pc>428-a<k1>paribarha<k2>paribarha
And there should be an alternate entry
<L>23619.1<pc>428-a<k1>parivarha<k2>parivarha
{{Lbody=23619}}
<LEND>

Don't want to correct all these now.

-------------------------------------------------------
revise hw.py
edit /c/xampp/htdocs/cologne/csl-pywork/v02/makotemplates/pywork/hw.py
add 'shs' to the 'Lbody' list.

--------------------------------------------------------
# xml and display Versions using {{LBody=N}}
cp temp_shs_3.txt /c/xampp/htdocs/COLOGNE/csl-orig/v02/shs/shs.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
grep 'shs ' redo_xampp_all.sh
sh generate_dict.sh shs  ../../shs
sh xmlchk_xampp.sh shs
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue429

Visual compare displays (shshwx) to revised.
Looks fine.

********************************************************

Finish syncing and installation
-------------------------------
csl-orig

cd /c/xampp/htdocs/cologne/csl-orig/v02
git status
        modified:   shs/shs.txt
        modified:   shs/shs_hwextra.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        shs/althws/
        shs/shs_back.txt
        shs/shs_front.txt
        shs/shs_middle.txt

git add .

git commit -m "SHS: hwxetra-Lbody conversion.
Ref: https://github.com/sanskrit-lexicon/COLOGNE/issues/429"

git push

-------------------------------
csl-pywork
cd /c/xampp/htdocs/cologne/csl-pywork/v02
git status
        modified:   makotemplates/pywork/hw.py

git add .

git commit -m "SHS: hwxetra-Lbody conversion.
Ref: https://github.com/sanskrit-lexicon/COLOGNE/issues/429"

git push

cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue429

-------------------------------------
install revised shs on COLOGNE server

cd csl-orig
git pull

# revise displays for shs
cd csl-pywork/v02
git pull

sh generate_dict.sh shs  ../../SHSScan/2020/

-----------------------
Sync this SHS repo
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue429

git add .
git commit -m "SHS: hwextra-Lbody conversion #429"
git push
=========================================================

