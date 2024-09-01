#-*- coding:utf-8 -*-
""" infotag.py
"""
from __future__ import print_function
import sys,re,codecs,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import digentry
## https:##stackoverflow.com/questions/27092833/unicodeencodeerror-charmap-codec-cant-encode-characters
## This required by git bash to avoid error
## UnicodeEncodeError: 'charmap' codec cannot encode characters 
## when run in a git bash script.

sys.stdout.reconfigure(encoding='utf-8') 

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 print(len(lines),"from",filein)
 return lines

def write_lines(fileout,lines):
 with codecs.open(fileout,"w","utf-8") as f:
  for out in lines:
   f.write(out+'\n')  
 print(len(lines),"lines written to",fileout)

def write_recs(fileout,outrecs,printflag=True,blankflag=True):
 # outrecs is array of array of lines
 with codecs.open(fileout,"w","utf-8") as f:
  for outarr in outrecs:
   for out in outarr:
    f.write(out+'\n')
   if blankflag:
    out = ''  # blank line separates recs
    f.write(out+'\n')
 if printflag:
  print(len(outrecs),"records written to",fileout)

def write_entries_helper(entry):
 outarr = []
 outarr.append(entry.metaline)
 for line in entry.datalines:
  outarr.append(line)
 outarr.append(entry.lend)
 return outarr

def write_entries(fileout,entries):
 outrecs = []
 for entry in entries:
  outrec = write_entries_helper(entry)
  outrecs.append(outrec)
 write_recs(fileout,outrecs,blankflag=False)


def parse_attrs(x):
 # X="Y" Z="W"   -> X Z
 # attribute values "V" to space
 x = re.sub(r'=".*?"', ' ',x)
 # remove spaces at either end
 x = x.strip()
 # compact multiple spaces to single space
 x = re.sub(r' +',' ',x)
 # split into array
 attrs = x.split(' ')
 return attrs
 
def info_analyze(fileout,entries):
 n = 0 #
 # entry attributes
 d = {}
 for entry in entries:
  txt = ' '.join(entry.datalines)
  for m in re.finditer(r'<info (.*?)/>',txt):
   attrvals = m.group(1)
   attrs = parse_attrs(attrvals)
   temp = ','.join(attrs)
   if temp not in d:
    d[temp] = 0  # count
   d[temp] = d[temp] + 1
 attrs = d.keys()
 attrs1 = sorted(attrs)
 outarr = []
 for a in attrs1:
  n = d[a] #
  outarr.append('%s %s' %(a,n))
 write_lines(fileout,outarr)

def info_analyze1(fileout,entries):
 n = 0 #
 # entries with info tag not on last bodyline
 outarr = []
 for entry in entries:
  txt = '\n'.join(entry.datalines[:-1])
  infos = re.findall(r'<info .*?/>',txt,re.DOTALL)
  if infos != []:
   n = n + 1
   infostr = ''.join(infos)
   L = entry.metad['L']
   L10 = L.ljust(10)
   outarr.append('%s %s' %(L10,infostr))
 write_lines(fileout,outarr)
 #print('%s entries with "<info " not on last line' % n)

def info_analyze2(fileout,entries):
 n = 0 #
 # entries with
 # a. info on last line
 # b non-info after first info on last line
 outarr = []
 for entry in entries:
  lastline = entry.datalines[-1]
  if '<info ' not in lastline:
   continue
  m = re.search(r'^(.*?)(<info .*?/>)(.*)$',lastline)
  afterinfo = m.group(3) # text after first info
  # remove info's from afterinfo
  noninfotxt = re.sub(r'<info .*?/>', '',afterinfo)
  noninfotxt1 = re.sub(r' ', '',noninfotxt)
  if noninfotxt1 == '':
   # ok.
   continue
  n = n + 1
  L = entry.metad['L']
  L10 = L.ljust(10)
  outarr.append('%s %s' %(L10,afterinfo))
 if n != 0:
  write_lines(fileout,outarr)
 else:
  print('%s entries with non-standard info last line' % n)

def revise_entries(entries):
 n = 0 # number of metalines changed
 for entry in entries:
  txt = '\n'.join(entry.datalines[:-1])
  infos = re.findall(r'<info .*?/>',txt,re.DOTALL)
  if infos == []:
   continue
  n = n + 1
  # revise entry.datalines
  # 1. remove infos
  lines = entry.datalines
  newlines = []
  nlines = len(lines)
  for i,line in enumerate(lines[:-1]):
   newline = re.sub(r'<info .*?/>', '',line)
   newlines.append(newline)
  # 2. put the 'infos' at end of last line
  line = lines[-1] # last dataline
  infos_str = ''.join(infos)
  newline = '%s%s' %(line,infos_str)
  newlines.append(newline)
  # --- change entry
  entry.datalines = newlines
 print('revise_entries: %s entries revised' % n)

if __name__=="__main__":
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx)
 fileout = sys.argv[2] # 
 entries = digentry.init(filein)
 Ldict = digentry.Entry.Ldict;
 fileout1 = 'infotag_attr.txt'
 info_analyze(fileout1,entries) # attributes
 fileout2 = 'infotag_notend.txt'
 info_analyze1(fileout2,entries)
 fileout3 = 'infotag_extralast.txt'
 info_analyze2(fileout3,entries)

 revise_entries(entries)
 write_entries(fileout,entries)
 #print(len(entries),'entries written to',fileout)

