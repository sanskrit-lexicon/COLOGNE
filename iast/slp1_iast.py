# coding=utf-8
"""convert.py
  Print information regarding slp1-iast transcoding.
"""
from __future__ import print_function
import sys,codecs,re
#sys.path.append('../')
import transcoder
transcoder.transcoder_set_dir('')
import xml.etree.ElementTree as ET  # for parsing slp1_roman.xml
import unicodedata  # used in freq_write to give unicode character names

def convert(filein,fileout,tranin,tranout):
 fp = codecs.open(filein,"r",'utf-8')
 fpout = codecs.open(fileout,"w",'utf-8')
 n=0;
 for x in fp:
  x = x.rstrip('\r\n')
  if (x == ''):
   continue
  n=n+1
  m = re.search(r'^([^ ]+) (.+)$',x)
  if not m:
   out = "line %s is unknown: %s" %(n,x)
   exit(1)
  head = m.group(1)
  body = m.group(2)
  #body = re.sub('/\|/',' # ',body); 
  #body = preg_replace('/ +/',' ',body);
  body1 = transcoder.transcoder_processString(body,tranin,tranout)
  y = "%s %s" % (head,body1)
  fpout.write("%s\n" % y)
 fp.close()
 fpout.close()
 print(n,"lines converted\n")

class INOUT(object):
 def __init__(self,xin,xout):
  self.slp1 = xin
  self.iastfile = xout
  self.iast = transcoder.transcoder_processString(self.slp1,'slp1','roman')
def parsexml(filein):
 tree = ET.parse(filein)
 xml = tree.getroot()
 entries = list(xml)  ## children
 recs = []
 for e in entries:
  if (e.tag != 'e'):
   # skip comments
   continue
  x = e.find("in")
  inval = x.text
  x = e.find("out") # out = the transformation of the input
  outval = x.text
  rec = INOUT(inval,outval)
  recs.append(rec)
 return recs

def write_recs(fileout,recs):
 outarr = []
 nprob = 0
 for rec in recs:
  slp1 = rec.slp1
  iast = rec.iast
  iastup = iast.upper()  # Use Python upper
  codes = [ord(c) for c in iast]
  ucodes = ["\\u%04x" %c for c in codes]
  ucode = ''.join(ucodes)
  names = [unicodedata.name(c) for c in iast]
  name = ' + '.join(names)
  out = '%s %s ( %s )    %s  %s' %(slp1,iast,iastup,ucode,name)
  """
  if ucode == rec.iastfile:
   flag = ''
  else:
   nprob = nprob + 1
   flag = ' (CHK)'
  out = '%s%s' %(out,flag)
  """
  outarr.append(out)
  #if ucode != rec.iastfile:
  # print('WARNING: ucode (%s) != iastfile (%s)' %(ucode,rec.iastfile))
  #assert ucode == rec.iastfile
 print(nprob,'possible problems found -- see CHK in',fileout)
 with codecs.open(fileout,"w",'utf-8') as f:
  for out in outarr:
   f.write(out+'\n')
 print(len(recs),"written to",fileout)
 
#-----------------------------------------------------
if __name__=="__main__":
 filein = sys.argv[1]  # slp1_roman.xml
 fileout = sys.argv[2]
 tranin = 'slp1'
 tranout = 'roman'
 recs = parsexml(filein)
 print(len(recs))
 write_recs(fileout,recs)



