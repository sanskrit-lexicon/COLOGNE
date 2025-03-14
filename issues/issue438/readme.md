# Trial to expand ls tags from pwg.xml

1. Current approach at CDSL seems to be adding literary resources as a layer while the data is served from website.
2. I intend to add that data to xml itself. temp_pwg_0.xml is copy of pwg/pywork/pwg.xml. 
3. ls_parameters.tsv stores the literary source and its parameters. It is a manual work, done in the descending order of occurrences of literary source as per sanskrit-lexicon/PWG/pwgissues/issue94/lsexamine2_summary.txt. It may have some human readable notes too.
4. Whatever liteary sources have consistent format of references are copied to book_names.tsv with tab separated values of LS and number of paramters e.g. `AV.	3` would mean that Atharvaveda has system of reference like 3,4,65.
5. `python expand_ls1.py temp_pwg_0.xml book_names.tsv temp_pwg_1.xml`
6. This will take temp_pwg_0.xml and book_names.tsv as input files and generate temp_pwg_1.xml which will have the literary sources expanded.
7. For example `<ls>MBH. 1,2523.</ls> des 11ten, <ls>HARIV. 176.</ls>` would be transformed `<ls n="MBH." id="1,2523">MBH. 1,2523.</ls> des 11ten, <ls n="HARIV." id="176">HARIV. 176.</ls>`. Attributes 'n' would hold name of the book and 'id' would hold the ID.
 