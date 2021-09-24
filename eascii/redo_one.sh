dictlo=$1
echo "dictionary=$dictlo"

 filein="../../../cologne/csl-orig/v02/${dictlo}/${dictlo}.txt"
 fileout="eadata/ea_${dictlo}.txt"
 cmd="python ea.py ${filein} ${fileout}"
 echo "$cmd"
 $cmd
