# Step1. Make it work.
1. Created a folder 'xxx' in csl-orig/v02
2. Put the xxx.txt file in csl-orig/v02/xxx folder.
3. Add a blank file csl-orig/v02/xxx_hwextra.txt.
4. Add a blank file csl-orig/v02/xxx-meta2.txt.
5. Add a blank file csl-orig/v02/xxxheader.xml
6. Create a folder csl-websanlexicon/v02/distinctfiles/xxx/web/webtc.
7. Add a file pdffiles.txt in csl-websanlexicon/v02/distinctfiles/xxx/web/webtc. It has the following format. `pc:pdffilename:headword` e.g. `1-005:pg1_005.pdf:akzakrIqA`. It can also have `pc:pdffilename` format. headword is optional.
8. Add the following data in csl-pywork/v02/dictparams.py
```
"armh": {
  "dictup":"ARMH",
  "dictlo":"armh",
  "dictname":u"Abhidhānaratnamālā of Halāyudha",
  "dictversion":"02",
 },
```
9. Add the following data in csl-websanlexicon/v02/dictparams.py
```
 "armh":{
  "dictup":"ARMH",
  "dictlo":"armh",
  "dictname":u"Abhidhānaratnamālā of Halāyudha",
  "dictversion":"02",
  "dictyear":"2020",
  "dictaccent":False,
  "webtc2devatextoption":True,
  "dictwc":"https://www.worldcat.org/title/halayudhas-abhidhanaratnamala-a-sanskrit-vocabulary/oclc/320893849",
  "dictbe":u"HALĀYUDHA & JOSHĪ JAYAŚAṄKARA , Halāyudhakśa (Abhidhānaratnamālā) of Halāyudha",
  "dicttitle":u"Abhidhānaratnamālā of Halāyudha 1957",
 }
```
10. Add the following line to csl-pywork/v02/redo_cologne_all.sh file. `sh generate_dict.sh xxx  ../../XXXScan/2020/`
11. Add the following line to csl-pywork/v02/redo_xampp_all.sh file. `sh generate_dict.sh xxx  ../../xxx`
12. Similarly, Add the following line to csl-websanlexicon/v02/redo_cologne_all.sh file. `sh generate_web.sh xxx  ../../XXXScan/2020/`
  * For regeneration just of the dictionary displays (Basic, etc.) at Cologne
13. Similarly, Add the following line to csl-websanlexicon/v02/redo_xampp_all.sh file. `sh generate_web.sh xxx  ../../xxx`
  * For regeneration just of the dictionary displays (Basic, etc.) in local installation.
14. Modify csl-websanlexicon/v02/makotemplates/web/webtc/dictinfo.php.
    * add line to '$cologne_pdfpages_urls' associative array, e.g.
    * "ARMH"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/ARMHScan/2020/web/pdfpages"
15. Modify csl-apidev/dictinfo.php, in two places:
   * To `$dictyear`, add e.g. `"ARMH"=>"2020"`
   * To `$cologne_pdfpages_urls`, add same as in `14` above.
16. Modify csl-apidev/sample/dictnames.js, add line to `dictnames`, e.g.
   * `['ARMH','Abhidhānaratnamālā of Halāyudha']`
17. Modify csl-apidev/simple-search/v1.1/parse_uri.php, add item to 
   * `$parmvalues['dict']`,  e.g. 'armh'
18. Modify hwnorm1/sanhw1/sanhw1.py in two places:
   * in `dictyear` array, add `"ARMH":"2020"`
   * in `san_san_dicts` array, add `"ARMH"`
     * for sanskrit-english dictionary, modify `san_en_dicts`
     * etc.
   * Note that the 'redo' procedure of hwnorm1/sanhw1 (see the readme therein)
     has to be redone after the pywork/v02 generate_dict script is run and
   * also the hwnorm1c.sqlite file has to be copied to csl-apidev, and
     csl-apidev has to be pushed in order for the csl-apidev displays to work
     for the new dictionary (displays such as simple-search and servepdf)

Doing steps upto `sh generate_dict.sh xxx  ../../xxx` added the XXX dictionary for local usage.
But it did not have the line breaks properly displayed. It also did not have Sanskrit text properly marked up for transliteration facility. So, even with 'Devanagari' as output, I used to get 'SLP1' output only.

# Step2. Add markup.

1. Add the dictcode in the following lines in csl-pywork/v02/makotemplates/pywork. This will add `<s>` tag to the whole entry. This will allow the conversion to various transliteration schemes.

```python
%if dictlo in ['skd','vcp','armh']:
def adjust_slp1(x):
 # in skd, all text is Devanagari.  But, the text is skd.txt does not use
%endif
%if dictlo not in ['skd','vcp','sch','md','shs','wil','ap90','bur','acc','yat','armh']:
def unused_adjust_slp1(x):
 # in vcp, all text is Devanagari.  But, the text is vcp.txt does not use
```

```python
%if dictlo in ['vcp','armh']:
 x = adjust_slp1(x) # add <s> markup to text
```

```python
%if dictlo in ['armh']:
 x = re.sub(r'(.)$', '\g<1><br/>', x)
 x = adjust_slp1(x) # add <s> markup to text
%endif
````

# Step3. Image for local installation.

1. Split the frontmatter, content and endmatter of the PDF. e.g. `pdftk ARMH.pdf cat 19-119 output ARMH_content.pdf`. Please put the ARMH.pdf file in the home folder. Otherwise pdftk may not work. 
2. Similarly generate `ARMH_frontmatter.pdf` and `ARMH_endmattaer.pdf` using pdftk.
3. Split the `ARMH_content.pdf` file into single page pdf using `pdftk ARMH_content.pdf burst output ARMH_split/ARMH_%04d.pdf`. 
4. Similarly split `ARMH_frontmatter.pdf` by using `pdftk ARMH_frontmatter.pdf burst output ARMH_split/ARMH_frontmatter_%04d.pdf`
5. Similarly split `ARMH_endmatter.pdf` by using `pdftk ARMH_endmatter.pdf burst output ARMH_split/ARMH_endmatter_%04d.pdf`
6. Create a folder `cologne/scans/xxx/pdfpages` e.g. `cologne/scans/armh/pdfpages`. scans folder is sibling of `csl-orig` folder.
7. Put the single page PDFs in this folder.
8. Generate the pdffiles.txt file. The following code may be of use. Modify, run and copy paste the output in pdffiles.txt.
```python
for x in range(102):
	print("{}:{}".format(str(x).zfill(4), 'ARMH_'+str(x).zfill(4)+'.pdf'))
```
9. Put the pdffiles.txt into csl-websanlexicon/v02/distinctfiles/armh/web/webtc

# Step 4. Images on sanskrit-lexicon-scans

1. Create a new repository xxx in sanskrit-lexicon-scans organization.
2. Copy README.md from some other repository, and make changes in the dictionary name.
3. Copy single page PDF files generated earlier into pdfpages directory.
4. add, commit and push to the repository.


# Still not handled

1. csl-homepage
2. csl-doc

