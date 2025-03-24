#cd ../../../csl-pywork/v02/
#sh generate_dict.sh pwg ../../pwg
#cd ../../COLOGNE/issues/issue438
#cp ../../../pwg/pywork/pwg.xml temp_pwg_0.xml
python expand_ls1.py temp_pwg_0.xml book_names.txt temp_pwg_1.xml
python expand_ls2.py temp_pwg_1.xml book_names1.txt temp_pwg_2.xml
#python reversal.py temp_pwg_2.xml temp_reverted_pwg_0.xml
#diff temp_pwg_0.xml temp_reverted_pwg_0.xml > log.diff
#cat log.diff | wc -l
python expand_ls3.py temp_pwg_2.xml temp_pwg_3.xml
python expand_ls4.py temp_pwg_3.xml book_names3.txt temp_pwg_4.xml
python expand_ls5.py temp_pwg_4.xml book_names4.txt temp_pwg_5.xml
python expand_ls6.py temp_pwg_5.xml book_names5.txt temp_pwg_6.xml
python expand_ls7.py temp_pwg_6.xml book_names6.txt temp_pwg_7.xml
python expand_ls8.py temp_pwg_7.xml book_names7.txt temp_pwg_8.xml
python expand_ls9.py temp_pwg_8.xml temp_pwg_9.xml

