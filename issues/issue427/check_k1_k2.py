#-*- coding:utf-8 -*-
""" check_k1_k2.py
"""
from __future__ import print_function
import sys,re,codecs,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

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

class METALINE:
 def __init__(self,line):
  self.line = line
  regex = r'^<L>(.*?)<pc>(.*?)<k1>(.*?)<k2>(.*?)<h>(.*)$'
  m = re.search(regex,line)
  if m == None:
   regex = r'^<L>(.*?)<pc>(.*?)<k1>(.*?)<k2>(.*?)$'
   m = re.search(regex,line)
  if m == None:
   print('METALINE init problem')
   print(line)
   exit(1)
  self.L = m.group(1)
  self.pc = m.group(2)
  self.k1 = m.group(3)
  self.k2 = m.group(4)

def check_k1_k2(k1,k2):
 newk1 = re.sub(r"[*°/^\\()' 3-]",'',k2)
 return newk1 == k1

def check_all_k2_k1_helper(line):
 rec = METALINE(line)
 k1 = rec.k1
 k2 = rec.k2
 flag = check_k1_k2(k1,k2)
 return flag

def check_all_k2_k1(lines):
 probs = []
 for line in lines:
  if not line.startswith('<L>'):
   continue
  if not check_all_k2_k1_helper(line):
   probs.append(line)
 n = len(probs)
 print('check_all_k2_k1 finds %s inconsistencies' % n)
 return probs

if __name__=="__main__":
 filein = sys.argv[1] #  
 fileout = sys.argv[2] # 
  
 lines = read_lines(filein)
 difflines = check_all_k2_k1(lines)
 write_lines(fileout,difflines)
