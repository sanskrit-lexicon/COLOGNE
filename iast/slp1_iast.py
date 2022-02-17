# coding=utf-8
"""slp1_iast.py
  Print information regarding slp1-iast transcoding.
"""
from __future__ import print_function
import sys,codecs,re
#sys.path.append('../')
import transcoder
transcoder.transcoder_set_dir('')
import xml.etree.ElementTree as ET  # for parsing slp1_roman.xml
import unicodedata  # used in freq_write to give unicode character names


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

def write_recs(fileout,recs0):
 outarr = []
 nprob = 0
 recs = sorted(recs0,key = lambda rec: rec.iast.lower())
 for rec in recs:
  slp1 = rec.slp1
  iast = rec.iast
  iastup = iast.upper()  # Use Python upper
  codes = [ord(c) for c in iast]
  ucodes = ["\\u%04x" %c for c in codes]
  ucode = ''.join(ucodes)
  names = [unicodedata.name(c) for c in iast]
  name = ' + '.join(names)
  #out = '%s %s ( %s )    %s  %s' %(slp1,iast,iastup,ucode,name)
  outa = '%s %s ( %s )' %(slp1,iast,iastup)
  outb = '%s %s' %(ucode.lstrip(),name)
  #outa1 = outa.ljust(15)
  #out = outa1 + outb
  out = '%s\t%s' %(outa,outb)
  outarr.append(out)

 print(nprob,'possible problems found -- see CHK in',fileout)
 with codecs.open(fileout,"w",'utf-8') as f:
  for out in outarr:
   f.write(out+'\n')
 print(len(recs),"written to",fileout)

def check1_invert(recs):
 # transcode iast back to slp1 using roman_slp1.xml
 # and compare with original slp1
 nprob = 0
 for rec in recs:
  iast = rec.iast
  slp1 = rec.slp1
  slp1_invert = transcoder.transcoder_processString(iast,'roman','slp1')
  if slp1_invert != rec.slp1:
   nprob = nprob + 1
   #print('slp1 inversion problem:',slp1)
   # 
   print('<e> <s>SKT</s> <in>%s</in> <out>%s</out></e>' %(rec.iastfile,rec.slp1))
 print('check1_invert.', nprob,'slp1 iast inversion problems')

def file_to_slp_dict(filein,islp):
 d = {}
 with codecs.open(filein,"r","utf-8") as f:
  for iline,line in enumerate(f):
   m = re.search(r'^<e> *<s>SKT</s> *<in>(.*?)</in> *<out>(.*?)</out> *</e>',line)
   if m == None:
    continue
   if islp == 1:
    slp1 = m.group(1)
    iast = m.group(2)
   else:
    slp1 = m.group(2)
    iast = m.group(1)
   if slp1 in d:
    print('duplicate slp1 in %s at line %s' %(filein,iline+1))
   else:
    d[slp1] = iast
 return d
def check2():
 file1 = 'slp1_roman.xml'
 file2 = 'roman_slp1.xml'
 d1 = file_to_slp_dict(file1,1)
 d2 = file_to_slp_dict(file2,2)
 slp1_d1 = list(d1.keys())
 slp1_d2 = list(d2.keys())
 print('%s has %s slp1 keys' %(file1,len(slp1_d1)))
 print('%s has %s slp1 keys' %(file2,len(slp1_d2)))
 for k in d2:
  if k not in d1:
   print('slp1 %s in %s but not in %s' %(k,file2,file1))
 if sorted(slp1_d1) == sorted(slp1_d2):
  print('GOOD: slp1 keys same for %s and %s'%(file1,file2))
 else:
  print('WARNING: slp1 key difference in %s and %s' %(file1,file2))

def file_to_iast_dict(filein,islp):
 d = {}
 with codecs.open(filein,"r","utf-8") as f:
  for iline,line in enumerate(f):
   m = re.search(r'^<e> *<s>SKT</s> *<in>(.*?)</in> *<out>(.*?)</out> *</e>',line)
   if m == None:
    continue
   if islp == 1:
    slp1 = m.group(1)
    iast = m.group(2)
   else:
    slp1 = m.group(2)
    iast = m.group(1)
   if iast in d:
    print('duplicate iast in %s at line %s' %(filein,iline+1))
   else:
    d[iast] = slp1
 return d
def check3():
 file1 = 'slp1_roman.xml'
 file2 = 'roman_slp1.xml'
 d1 = file_to_iast_dict(file1,1)
 d2 = file_to_iast_dict(file2,2)
 iast_d1 = list(d1.keys())
 iast_d2 = list(d2.keys())
 print('%s has %s iast keys' %(file1,len(iast_d1)))
 print('%s has %s iast keys' %(file2,len(iast_d2)))
 for k in d2:
  if k not in d1:
   print('iast %s in %s but not in %s' %(k,file2,file1))
 if sorted(iast_d1) == sorted(iast_d2):
  print('GOOD: iast keys same for %s and %s'%(file1,file2))
 else:
  print('WARNING: iast key difference in %s and %s' %(file1,file2))

#-----------------------------------------------------
if __name__=="__main__":
 filein = sys.argv[1]  # slp1_roman.xml
 fileout = sys.argv[2]
 tranin = 'slp1'
 tranout = 'roman'
 recs = parsexml(filein)
 print(len(recs))
 write_recs(fileout,recs)
 check1_invert(recs)
 check2()
 check3()
