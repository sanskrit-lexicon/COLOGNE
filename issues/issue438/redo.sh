cd ../../../csl-pywork/v02/
sh generate_dict.sh pwg ../../pwg
cd ../../COLOGNE/issues/issue438
cp ../../../pwg/pywork/pwg.xml temp_pwg_0.xml
python expand_ls1.py temp_pwg_0.xml book_names.txt temp_pwg_1.xml
python expand_ls2.py temp_pwg_1.xml book_names1.txt temp_pwg_2.xml
python reversal.py temp_pwg_2.xml temp_reverted_pwg_0.xml
diff temp_pwg_0.xml temp_reverted_pwg_0.xml > log.diff
cat log.diff | wc -l
cp temp_reverted_pwg_0.xml ../../../useless/temp_pwg.xml
#cd ../../../useless
#git diff --word-diff
#cd ../COLOGNE/issues/issue438
