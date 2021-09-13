""" xmltag.py
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

def chkgreek(path):
 ans=[]
 f = codecs.open(path,"r","utf-8") 
 ntot = 0
 nline = 0
 for line in f:
  instances = re.findall(r'<lang n="greek">.*?</lang>',line)
  ntot = ntot + len(instances)
  if len(instances) != 0:
   nline = nline + 1
 f.close()
 return ntot,nline


def gather(filein):
 d = {}
 regex = re.compile(r'<(.*?)>')
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
    e = m.group(1)
    tag = re.sub(r' .*$','',e)  # remove attributes, if any
    # exclude closing tags
    if tag.startswith('/'):
     continue
    if tag not in d:
     d[tag] = 0
    d[tag] = d[tag] + 1
 return d
 print("%s lines written to %s" %(n,fileout))
if __name__=="__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2] # output path
 tagsd = gather(filein)  # dictionary with counts
 tags = sorted(tagsd.keys()) # present results alphabetical order
 with codecs.open(fileout,"w","utf-8") as f:
  for tag in tags:
   out = '<%s> %s' %(tag,tagsd[tag])
   f.write(out+'\n')
 print(len(tags),'distinct tags written to',fileout)
