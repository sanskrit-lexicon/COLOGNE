
Begin 09-01-2024

Ref: https://github.com/sanskrit-lexicon/COLOGNE/issues/432
This directory:
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue432

# -------------------------------------------------------------
Start with a copy of csl-orig/v02/vcp/vcp.txt at commit
  e8cb1b637e838fc36357f1ac3c58038b1e6a923b

# change to csl-orig repository on local installation
cd /c/xampp/htdocs/cologne/csl-orig/
# generate temp_vcp_0 .txt in this directory
git show  e8cb1b637:v02/vcp/vcp.txt > /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue432/temp_vcp_0.txt
# return to this directory
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue432


# -------------------------------------------------------------
# similarly copy vcp_hwextra from csl-orig
cd /c/xampp/htdocs/COLOGNE/csl-orig/
git show  e8cb1b637:v02/vcp/vcp_hwextra.txt > /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue432/vcp_hwextra.txt
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue432

wc -l vcp_hwextra.txt
1764 vcp_hwextra.txt

Sample:
<L>28.1<k1>aMseBAra<k2>aMseBAra<type>alt<LP>28<k1P>aMsaBAra
<L>29.1<k1>aMseBArika<k2>aMseBArika<type>alt<LP>29<k1P>aMsaBArika

--------------------------------------------------------
# displays PRIOR to changes.  vcphwx  (uses vcp_hwextra)
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh vcp ../../vcphwx
# local display url: http://localhost/cologne/vcphwx/web/
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue432

--------------------------------------------------------
cd /c/xampp/htdocs/cologne/csl-orig/v02/vcp
mkdir althws
mv vcp_hwextra.txt althws/
touch vcp_hwextra.txt
echo "2024-09-01. vcp_hwextra.txt no longer used." >  althws/readme.txt

cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue432

---------------------------------
temp_vcp_1.txt, vcp_front.txt, vcp_back.txt
Extract lines before first entry into vcp_front.txt
Extract lines after last entry into vcp_back.txt
Remove blank lines in the remaining, and write to temp_vcp_1.txt

python frontback.py temp_vcp_0.txt temp_vcp_1.txt vcp_front.txt vcp_back.txt

517597 from temp_vcp_0.txt
3 517596
skip_empty_lines 0
517594 lines written to temp_vcp_1.txt
3 lines written to vcp_front.txt
0 lines written to vcp_back.txt

--------------------------------------------------------
Remove all matter not within an entry

python middle.py temp_vcp_1.txt temp_vcp_1a.txt vcp_middle.txt

517594 from temp_vcp_1.txt
515861 lines written to temp_vcp_1a.txt
1733 lines written to vcp_middle.txt

# Keep these 'just in case' of future use

cp vcp_front.txt /c/xampp/htdocs/cologne/csl-orig/v02/vcp/
cp vcp_back.txt  /c/xampp/htdocs/cologne/csl-orig/v02/vcp/
cp vcp_middle.txt /c/xampp/htdocs/cologne/csl-orig/v02/vcp/

--------------------------------------------------------
temp_vcp_2.txt
check that all <info .*?/> markup in an entry occurs at the end of last line
Rewrite as needed.
Why?  For AB version.

python infotag.py temp_vcp_1a.txt temp_vcp_2.txt

Notes:
1. there are no <info /> tags in temp_vcp_1a.txt
  So temp_vcp_2.txt is same as temp_vcp_1a.txt

--------------------------------------------------------

temp_vcp_3.txt
Lbody form constructed from version 2 and vcp_hwextra

python convert_hwextra_lbody.py temp_vcp_2.txt vcp_hwextra.txt temp_vcp_3.txt

515861 lines read from temp_vcp_2.txt
48370 entries found
1764 from vcp_hwextra.txt
50134 records written to temp_vcp_3.txt

(+ 48370 1764) = 50134

-------------------------------------------------------
check k1-k2 consistency
python check_k1_k2.py temp_vcp_3.txt check_k1_k2.txt

521153 from temp_vcp_3.txt
check_all_k2_k1 finds 1747 inconsistencies
1747 lines written to check_k1_k2.txt

-------------------------------------------------------

I think most of these inconsistencies are in the first
record of groups of alternates, and can be corrected
by merely remove a parenthetica expression in k2

Example:
OLD: <L>28<pc>0037,a<k1>aMsaBAra<k2>aMsa(se)BAra
NEW: <L>28<pc>0037,a<k1>aMsaBAra<k2>aMsaBAra

python k2_paren.py temp_vcp_3.txt temp_vcp_4.txt

521153 from temp_vcp_3.txt
remove_k2_parens: 1741 lines changed
521153 lines written to temp_vcp_4.txt

-----

python check_k1_k2.py temp_vcp_4.txt check_k1_k2_4.txt

521153 from temp_vcp_4.txt
check_all_k2_k1 finds 10 inconsistencies
10 lines written to check_k1_k2_4.txt


----------------------------
temp_vcp_5.txt  correct those 10
cp temp_vcp_4.txt temp_vcp_5.txt
manual edit temp_vcp_5.txt

<L>1679<pc>0159,a<k1>anAmayitna<k2>anAmayitna,      remove ,
<L>8366<pc>0982,a<k1>ira<k2>ira--IrzAyAM            remove --IrzAyAM 
<L>8387<pc>0983,b<k1>ivAruSuktikA<k2>irvAruSuktikA  irv -> iv
<L>14081<pc>2104,b<k1>kubera<k2>kuvera              kub -> kuv
<L>15418<pc>2281,b<k1>kOtakI<k2>kOzItakI            kOzItakI -> kOtakI
  also new entry for alternate 
<L>15418.1<pc>2281,b<k1>kOzItakI<k2>kOzItakI   
{{Lbody=15418}}
<LEND>
<L>15514<pc>2309,a<k1>kravizRa<k2>kravizRa,         remove comma
<L>16466<pc>2468,b<k1>Karba<k2>Karva                Karba -> Karva
<L>16687<pc>2482,b<k1>gaganasinDa<k2>gaganasinDa,   remove comma
<L>26445<pc>3783,b<k1>drAvayitnu<k2>drAvayitnu,     remove comma
<L>28189<pc>3990,b<k1>navabaDU<k2>navavaDU          baDU -> vaDU 

----- check version 5
python check_k1_k2.py temp_vcp_5.txt check_k1_k2_5.txt

521156 from temp_vcp_5.txt
check_all_k2_k1 finds 0 inconsistencies
0 lines written to check_k1_k2_5.txt

Ready to install version 5
-------------------------------------------------------
revise hw.py
edit /c/xampp/htdocs/cologne/csl-pywork/v02/makotemplates/pywork/hw.py
add 'vcp' to the 'Lbody' list.

--------------------------------------------------------
# xml and display Versions using {{LBody=N}}
cp temp_vcp_5.txt /c/xampp/htdocs/COLOGNE/csl-orig/v02/vcp/vcp.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
grep 'vcp ' redo_xampp_all.sh
sh generate_dict.sh vcp  ../../vcp
sh xmlchk_xampp.sh vcp
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue432

Visual compare displays (vcphwx) to revised.
Looks fine.

********************************************************

Finish syncing and installation
-------------------------------
csl-orig

cd /c/xampp/htdocs/cologne/csl-orig/v02
git status
        modified:   vcp/vcp.txt
        modified:   vcp/vcp_hwextra.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        vcp/althws/
        vcp/vcp_back.txt
        vcp/vcp_front.txt
        vcp/vcp_middle.txt

git add .

git commit -m "VCP: hwxetra-Lbody conversion.
Ref: https://github.com/sanskrit-lexicon/COLOGNE/issues/432"

git push

-------------------------------
csl-pywork
cd /c/xampp/htdocs/cologne/csl-pywork/v02
git status
        modified:   makotemplates/pywork/hw.py

git add .

git commit -m "VCP: hwxetra-Lbody conversion.
Ref: https://github.com/sanskrit-lexicon/COLOGNE/issues/432"

git push

cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue432

-------------------------------------
install revised vcp on COLOGNE server

cd csl-orig
git pull

# revise displays for vcp
cd csl-pywork/v02
git pull

sh generate_dict.sh vcp  ../../VCPScan/2020/

-----------------------
Sync this VCP repo
cd /c/xampp/htdocs/sanskrit-lexicon/COLOGNE/issues/issue432

git add .
git commit -m "VCP: hwextra-Lbody conversion #432"
git push
=========================================================

