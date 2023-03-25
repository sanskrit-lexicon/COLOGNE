sanskrit-lexicon/COLOGNE issue407 work
https://github.com/sanskrit-lexicon/COLOGNE/issues/407


These might be
a. errors in accentcoding
b. superscript notation

-------------------------------------------------------
Count incidences of [^<][/\\\^][fxaiueoFXAIUEO] in dictionaries per
csl-orig/v02.

# ****************************************************************
problems passing backslashes to python
python count.py cae "[^<][/\\\\^][fxaiueoFXAIUEO]" count.txt
Note: Can't pass this regex.
  it is changed to [^<][C:/^][fxaiueoFXAIUEO]
# define the regex internally
python count.py cae count.txt
"[^<][/\\^][fxaiueoFXAIUEO]"
python count.py cae "[^<][/\\\\\^][fxaiueoFXAIUEO]" count.txt

Solution:  put the regex inside count.py
# ****************************************************************

python count.py cae count.txt  

python count.py ALL  count.txt
36 dictionary codes known
acc, ae, ap90, ben, bhs, bop, bor, bur, cae, ccs, gra, gst, ieg, inm, krm, mci,
md, mw, mw72, mwe, pe, pgn, pui, pw, pwg, sch, shs, skd, snp, stc, vcp, vei, wil
, yat, lan, armh
regex = [^<][/\\^][fxaiueoFXAIUEO]

36 counts written to count.txt

--------------------------------------------------
python count1.py ALL  count1.txt

--------------------------------------------------
# lines written to details/details_cae.txt
python details.py cae
# do the above for all dictionaries
python details.py ALL

--------------------------------------------------
# lines written to details1/details1_cae.txt
  sorted by type of character precedeing accent
python details1.py pw
# do the above for all dictionaries
python details1.py ALL

----------------------------------------------------------------------
Notes on changes
----------------------------------------------------------------------

-----
bhs 1 no changes  and/or
55819  : formation from these nouns, and/or from such Bhvr. cpds.
-----
bop 22 no changes. superscript
-----
cae 17 no changes  vowel before accent
-----
ccs 17
  made 5 changes (consonant before accent).
  ref changes/change_ccs.txt
; 5 instances with character before accent of type Consonant
-----
inm   3 C-1, ?-2
  add space around '/'  -- not an accent.
  ref changes/change_inm.txt
-----
krm   13 V-2, ?-11
  ref changes/change-inm.txt
     ^x  changed to <sup>x</sup>
     Several punctuaion changes also.
-----
mci   374 C-76, V-100, ?-198
    '/' usually represents a danda in italic iast text.
    Put a space on either side of '/' or '//'.
    3799 changes written to changes/change_mci.txt
-----
mw    3 V-3
    i/A, u/a   no change needed. vowel+accent+vowel
-----
pui   1 ?-1
   many changes of '^' to either (a) <sup>X</sup>, or (b) <F>x..</F>
   see changes/change_pui.txt
-----
pwkvn 4 V-4
  No changes made
-----
pw    298 C-2, V-296
    2 changes, changes/change_pw.txt
-----
pwg   86 V-86
    no changes
-----
sch   1 V-1
    no changes
-----
stc   52 ?-52
    {^me^} etc. <sup>me</sup>
    no changes
lan   1 V-1
    1 change:  see changes/change_lan.txt
    Incidentally found a flaw in validation:
    <ls n="lan,16,4">16<sup>4</sup></ls>
     " Element sup is not declared in ls list of possible children"
    Changed csl-pywork: one.dtd to
; ----- 
gra   175 C-154, V-20, ?-1
     Accented semivowels y,v.
     no changes made
**********************************************************************
**********************************************************************


----------------------------------------------
cae and ccs
nitodin   the Devanagari looks like 'nitedin'
----------------------------------------------
