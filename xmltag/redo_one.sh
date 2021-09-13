dictlo=$1
 echo "dictionary=$dictlo"
 filein="../../../csl-orig/v02/${dictlo}/${dictlo}.txt"
 fileout="xmltag_${dictlo}.txt"
 cmd="python xmltag.py ${filein} ${fileout}"
 echo "$cmd"
 $cmd
