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
