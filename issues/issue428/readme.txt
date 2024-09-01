
Begin 08-31-2024

Ref: https://github.com/sanskrit-lexicon/COLOGNE/issues/428
This directory:
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue428

# -------------------------------------------------------------
Start with a copy of csl-orig/v02/pwkvn/pwkvn.txt at commit
  40eb85cec6857f21f313ac623e50d8f5da640a5f

# change to csl-orig repository on local installation
cd /c/xampp/htdocs/cologne/csl-orig/
# generate temp_pwkvn_0 .txt in this directory
git show  40eb85cec:v02/pwkvn/pwkvn.txt > /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue428/temp_pwkvn_0.txt
# return to this directory
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue428

# -------------------------------------------------------------
# similarly copy pwkvn_hwextra from csl-orig
cd /c/xampp/htdocs/COLOGNE/csl-orig/
git show  40eb85cec:v02/pwkvn/pwkvn_hwextra.txt > /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue428/pwkvn_hwextra.txt
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue428

wc -l pwkvn_hwextra.txt
2365 pwkvn_hwextra.txt


# first two
head -n 2 pwkvn_hwextra.txt
<L>115.1<pc>1-283-a<k1>agfhapatika<k2>*agfhapati, *agfhapatika<type>alt<LP>115<k1P>agfhapati
<L>147.1<pc>1-283-b<k1>agnyADeyadevatA<k2>agnyADeya, agnyADeyadevatA<type>alt<LP>147<k1P>agnyADeya


--------------------------------------------------------
displays PRIOR to changes.  pwkvnhwx  (uses pwkvn_hwextra)
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh pwkvn ../../pwkvnhwx
sh xmlchk_xampp.sh pwkvn
#
ok
# local display url: http://localhost/cologne/pwkvnhwx/web/

cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue428

--------------------------------------------------------
cd /c/xampp/htdocs/cologne/csl-orig/v02/pwkvn
mkdir althws
mv pwkvn_hwextra.txt althws/
touch pwkvn_hwextra.txt
echo "2024-08-31. pwkvn_hwextra.txt no longer used." >  althws/readme.txt
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue428

---------------------------------
temp_pwkvn_1.txt, pwkvn_front.txt, pwkvn_back.txt
Extract lines before first entry into pwkvn_front.txt
Extract lines after last entry into pwkvn_back.txt
Remove blank lines in the remaining, and write to temp_pwkvn_1.txt

python frontback.py temp_pwkvn_0.txt temp_pwkvn_1.txt pwkvn_front.txt pwkvn_back.txt

90460 from temp_pwkvn_0.txt
2 90459
skip_empty_lines 22617
67841 lines written to temp_pwkvn_1.txt
2 lines written to pwkvn_front.txt
0 lines written to pwkvn_back.txt


--------------------------------------------------------
PWKVN 
Extract additional front matter manually
Remove all matter not within an entry

python middle.py temp_pwkvn_1.txt temp_pwkvn_1a.txt pwkvn_middle.txt

67841 from temp_pwkvn_1.txt
67833 lines written to temp_pwkvn_1a.txt
8 lines written to pwkvn_middle.txt


# Keep these 'just in case' of future use

cp pwkvn_front.txt /c/xampp/htdocs/cologne/csl-orig/v02/pwkvn/
cp pwkvn_back.txt  /c/xampp/htdocs/cologne/csl-orig/v02/pwkvn/
cp pwkvn_middle.txt /c/xampp/htdocs/cologne/csl-orig/v02/pwkvn/

--------------------------------------------------------
temp_pwkvn_2.txt
check that all <info .*?/> markup in an entry occurs at the end of last line
Rewrite as needed.
Why?  For AB version.

python infotag.py temp_pwkvn_1a.txt temp_pwkvn_2.txt

67833 lines read from temp_pwkvn_1a.txt
22611 entries found
0 lines written to infotag_attr.txt
0 lines written to infotag_notend.txt
0 entries with non-standard info last line
revise_entries: 0 entries revised
22611 records written to temp_pwkvn_2.txt


Notes:
There are no <info /> tags in pwkvn.
temp_pwkvn_1a.txt and temp_pwkvn_2.txt are identical.

These info tags are already at end of last line,
so temp_pwkvn_1a.txt is same as temp_pwkvn_2.txt

--------------------------------------------------------
--------------------------------------------------------

--------------------------------------------------------
temp_pwkvn_3.txt
Lbody form constructed from version 2 and pwkvn_hwextra.txt

python convert_hwextra_lbody.py temp_pwkvn_2.txt pwkvn_hwextra.txt temp_pwkvn_3.txt

67833 lines read from temp_pwkvn_2.txt
22611 entries found
2365 from pwkvn_hwextra.txt
2365  len of extras
2365 entriesx created
24976 records written to temp_pwkvn_3.txt

(+ 22611 2365) = 24976


-------------------------------------------------------
temp_pwkvn_4.txt

convert pwkvn metalines to cdsl standard form.
This is similar to the conversion for pw

------------------------------
commas in k2
3865 matches for "<k2>.*?," in buffer: temp_pwkvn_3.txt

------------------------------

python convert_metaline_pw.py ab,cdsl temp_pwkvn_3.txt temp_pwkvn_4.txt temp_pwkvn_3_groups.txt

74928 lines read from temp_pwkvn_3.txt
24976 entries found
revise_k2_ab_cdsl found 1500 groups, with identical k2
revise_k2_ab_cdsl changes 3865 metalines
24976 records written to temp_pwkvn_4.txt
24976 new entries written to temp_pwkvn_4.txt



-------------------------------------------------------
# check consistency of k1 and k2 for all metalines
Write the metalines with inconsistency.

python check_k1_k2.py temp_pwkvn_4.txt check_k1_k2.txt
643111 from temp_pwkvn_4.txt
check_all_k2_k1 finds 5 inconsistencies

old: <L>3227.4<pc>2-301-a<k1>Cando'mbuDi<k2>Cando'mbuDi
new: <L>3227.4<pc>2-301-a<k1>CandombuDi<k2>Cando'mbuDi

old: <L>4850<pc>3-264-a<k1>duHKasparSa<k2>duHKasparSa(m)
new: <L>4850<pc>3-264-a<k1>duHKasparSa<k2>duHKasparSa

old: <L>4867.1<pc>3-264-a<k1>die<k2>die richtige Form ist dfQekzurA
new: <L>4867.1<pc>3-264-a<k1>dfQekzurA<k2>dfQekzurA

old: <L>4904.3<pc>3-264-b<k1>dvyAcitikI<k2>(*dvyAcitikI) und *dvyAcitIna
new: <L>4904.3<pc>3-264-b<k1>dvyAcitIna<k2>*dvyAcitIna

old: <L>19198.1<pc>7-357-a<k1>paroM'hu<k2>paroM'hu
new: <L>19198.1<pc>7-357-a<k1>paroMhu<k2>paroM'hu

------------------------------------------------------
temp_pwkvn_5.txt
cp temp_pwkvn_4.txt temp_pwkvn_5.txt

Make changes in above 5 lines

# confirm k1k2 consistency with version 5
python check_k1_k2.py temp_pwkvn_5.txt check_k1_k2_5.txt

check_all_k2_k1 finds 0 inconsistencies
0 lines written to check_k1_k2.txt

def check_k1_k2(k1,k2):  
 newk1 = re.sub(r"[*°/^\\()' 3-]",'',k2)
 return newk1 == k1

This is the conversion from k2 to k1 for pwkvn; same as for pw.
------------------------------------------------------

-------------------------------------------------------
revise hw.py
edit /c/xampp/htdocs/cologne/csl-pywork/v02/makotemplates/pywork/hw.py
add 'pwkvn' to the 'Lbody' list.
--------------------------------------------------------
# xml and display Versions using {{LBody=N}}
cp temp_pwkvn_5.txt /c/xampp/htdocs/COLOGNE/csl-orig/v02/pwkvn/pwkvn.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
grep 'pwkvn ' redo_xampp_all.sh
sh generate_dict.sh pwkvn  ../../pwkvn
sh xmlchk_xampp.sh pwkvn
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue428

Visual compare displays (pwkvnhwx) to revised.
Looks ok. 

********************************************************

Finish syncing and installation
-------------------------------
csl-orig

cd /c/xampp/htdocs/cologne/csl-orig/v02
git status
        modified:   pwkvn/althws/readme.txt
        modified:   pwkvn/pwkvn.txt
        modified:   pwkvn/pwkvn_hwextra.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        pwkvn/althws/pwkvn_hwextra.txt
        pwkvn/pwkvn_back.txt
        pwkvn/pwkvn_front.txt
        pwkvn/pwkvn_middle.txt


git add .

git commit -m "PWKVN: hwxetra-Lbody conversion
Ref: https://github.com/sanskrit-lexicon/COLOGNE/issues/428"

git push

-------------------------------
csl-pywork
cd /c/xampp/htdocs/cologne/csl-pywork/v02
git status
        modified:   makotemplates/pywork/hw.py

git add .

git commit -m "PWKVN: hwxetra-Lbody conversion.
Ref: https://github.com/sanskrit-lexicon/COLOGNE/issues/428"

git push

cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue428

-------------------------------------
install revised pwkvn on COLOGNE server

cd csl-orig
git pull

# revise displays for pwkvn
cd csl-pywork/v02
git pull

 grep pwkvn redo_cologne_all.sh
sh generate_dict.sh pwkvn  ../../PWKVNScan/2020/

-----------------------
Sync this repo
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue428

git add .
git commit -m "PWKVN: hwextra-Lbody conversion #428"
git push
=========================================================

********************************************************
THE END
