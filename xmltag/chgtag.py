""" chgtag.py
 Find occurrence of all instances of xml-type tags, 
 -  without attributes:  <tag>   
 - exclude closing tag:  </tag>
 - with attribute(s) :   <tag n="x" m="y>   (record only the tag name)
 - empty tags : <div n="P"/>
 - pseudo-tags: <>
 - exclude meta line <L>....
 - exclude meta ending <LEND>
 - include lines only between <L> and <LEND>
 - NOTE:  {#, {@ and {% are also 'pseudo' tags. (converted to xml tags)
 -      And there may be other curly-bracket pseudo tags. 
 -      This study omits these.
"""
import sys,re
import codecs
import os.path,time


def gather(filein):
 ans = []
 regex = re.compile(r'<chg.*?</chg>')
 with codecs.open(filein,"r","utf-8") as f:
  metaline = None
  for line in f:
   line = line.rstrip('\r\n')
   if line.startswith('<L>'):
    metaline = True
    continue
   if line.startswith('<LEND>'):
    metaline = False
    continue
   if not metaline:
    continue
   for m in re.finditer(regex,line):
    ans.append(m.group(0))
 return ans
 
if __name__=="__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2] # output path
 outarr = gather(filein)
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out+'\n')
 print(len(outarr),'instances written to',fileout)
