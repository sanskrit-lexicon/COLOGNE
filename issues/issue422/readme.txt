
Begin 08-27-2024

Ref: https://github.com/sanskrit-lexicon/COLOGNE/issues/422
This directory:
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue422

# -------------------------------------------------------------
Start with a copy of csl-orig/v02/acc/acc.txt at commit
  090fa0323deeb6c4be455dea72a1c1656351f502

# change to csl-orig repository on local installation
cd /c/xampp/htdocs/cologne/csl-orig/
# generate temp_acc_0 .txt in this directory
  git show  090fa0323:v02/acc/acc.txt > /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue422/temp_acc_0.txt
# return to this directory
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue422


# -------------------------------------------------------------
# similarly copy acc_hwextra from csl-orig
cd /c/xampp/htdocs/COLOGNE/csl-orig/
git show  090fa0323:v02/acc/acc_hwextra.txt > /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue422/acc_hwextra.txt
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue422

--------------------------------------------------------
displays PRIOR to changes.  acchwx  (uses acc_hwextra)
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh acc ../../acchwx
# local display url: http://localhost/cologne/acchwx/web/
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue422

--------------------------------------------------------
cd /c/xampp/htdocs/cologne/csl-orig/v02/acc
mkdir althws
mv acc_hwextra.txt althws/
touch acc_hwextra.txt
echo "2024-08-27. acc_hwextra.txt no longer used." >  althws/readme.txt

---------------------------------
temp_acc_1.txt, acc_front.txt, acc_back.txt
Extract lines before first entry into acc_front.txt
Extract lines after last entry into acc_back.txt
Remove blank lines in the remaining, and write to temp_acc_1.txt

python frontback.py temp_acc_0.txt temp_acc_1.txt acc_front.txt acc_back.txt
210469 from temp_acc_0.txt
2 210191
skip_empty_lines 2
210188 lines written to temp_acc_1.txt
2 lines written to acc_front.txt
277 lines written to acc_back.txt

--------------------------------------------------------
ACC has multiple volumes
Extract additional front matter manually
Remove all matter not within an entry

python middle.py temp_acc_1.txt temp_acc_1a.txt acc_middle.txt
 
210188 from temp_acc_1.txt
209621 lines written to temp_acc_1a.txt
567 lines written to acc_middle.txt

(+ 209621 567) = 210188

cp acc_front.txt /c/xampp/htdocs/cologne/csl-orig/v02/acc/
cp acc_back.txt  /c/xampp/htdocs/cologne/csl-orig/v02/acc/
cp acc_middle.txt /c/xampp/htdocs/cologne/csl-orig/v02/acc/

--------------------------------------------------------
temp_acc_2.txt
check that all <info .*?/> markup in an entry occurs at the end of last line
Rewrite as needed.
Why?  For AB version.

python infotag.py temp_acc_1a.txt temp_acc_2.txt

Notes:
1. there are no <info /> tags in temp_acc_1a.txt
  So temp_acc_2.txt is same as temp_acc_1a.txt

--------------------------------------------------------
temp_acc_3.txt
Lbody form constructed from version 2 and acc_hwextra

python convert_hwextra_lbody.py temp_acc_2.txt acc_hwextra.txt temp_acc_3.txt
acc_hwextra.txt 1593 items.
First 2 lines:
<L>12.1<k1>akzacaraRa<k2>akzacaraRa,<type>alt<LP>12<k1P>akzapAda
<L>39.1<k1>agastisaMhitA<k2>agastisaMhitA<type>alt<LP>39<k1P>agastyasaMhitA

209621 lines read from temp_acc_2.txt
48230 entries found
1593 from acc_hwextra.txt
49822 records written to temp_acc_3.txt

(+ 48230 1593) 49823

Q: Why not 49822 ?
A: One comment line (starting with ';') in acc_hwextra.txt


-------------------------------------------------------
revise hw.py
edit /c/xampp/htdocs/cologne/csl-pywork/v02/makotemplates/pywork/hw.py
add 'acc' to the 'Lbody' list.
--------------------------------------------------------
# xml and display Versions using {{LBody=N}}
cp temp_acc_3.txt /c/xampp/htdocs/COLOGNE/csl-orig/v02/acc/acc.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
 grep 'acc ' redo_xampp_all.sh
sh generate_dict.sh acc  ../../acc
sh xmlchk_xampp.sh acc
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue422

Visual compare displays (acchwx) to revised.
Looks fine.


********************************************************

Finish syncing and installation
-------------------------------
csl-orig

cd /c/xampp/htdocs/cologne/csl-orig/v02
git status
        modified:   acc.txt
        modified:   acc_hwextra.txt

        Untracked files:
        (use "git add <file>..." to include in what will be committed)
        acc_back.txt
        acc_front.txt
        acc_middle.txt
        althws/

git add .

git commit -m "ACC: hwxetra-Lbody conversion.
Ref: https://github.com/sanskrit-lexicon/COLOGNE/issues/422"

git push

-------------------------------
csl-pywork
cd /c/xampp/htdocs/cologne/csl-pywork/v02
git status
        modified:   makotemplates/pywork/hw.py

git add .

git commit -m "ACC: hwxetra-Lbody conversion.
Ref: https://github.com/sanskrit-lexicon/COLOGNE/issues/422"

git push


cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue422

-------------------------------------
install revised acc on COLOGNE server

cd csl-orig
git pull

# revise displays for acc
cd csl-pywork/v02
git pull

sh generate_dict.sh acc  ../../ACCScan/2020/

-----------------------
Sync this ACC repo
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue422


git add .
git commit -m "ACC: hwextra-Lbody conversion #422"
git push
=========================================================

