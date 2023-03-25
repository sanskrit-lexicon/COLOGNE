# coding=utf-8
""" diff_to_changes_dict.py
   Generate change transactions from an 'old' and 'new' file
   The two files should have same number of lines
   ASSUME input file is a dictionary as in csl-orig/v02, e.g. mw.txt.
     This structure identifies the metaline for each change;
     and this is the only difference from diff_to_changes.py,
     which ignores this structure, and is thus available for 
     generating changes for any two text files with same number of lines.
  python diff_to_changes_dict.py old.txt new.txt changes.txt
  Now:
  python updateByLine.py old.txt changes.txt new1.txt
  then new1.txt is same as new.txt.
"""
from __future__ import print_function
import sys, re,codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

class Change(object):
 def __init__(self,iline,line1,line2,metaline1):
  self.iline = iline
  self.line1 = line1
  self.line2 = line2
  self.lnum = iline+1
  self.metaline1 = metaline1 
  a = []
  a.append('; %s' %metaline1)
  a.append('%s old %s' %(self.lnum,self.line1))
  a.append(';')
  a.append('%s new %s' %(self.lnum,self.line2))
  a.append(';---------------------------------------------------')
  self.changeout = a
  
def write_changes(fileout,changes):
 outarr = []
 for change in changes:
  for x in change.changeout:
   outarr.append(x)
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out+'\n')
 print(len(changes),"changes written to",fileout)
 
if __name__=="__main__":
 filein1 = sys.argv[1] # old.txt
 filein2 = sys.argv[2] # new.txt
 fileout = sys.argv[3] # changes.txt
 lines1 = read_lines(filein1)
 lines2 = read_lines(filein2)
 n = len(lines1)
 if n != len(lines2):
  print('ERROR: files have different number of lines')
  exit(1)
 changes = []
 metaline1 = None
 metaline2 = None
 for iline,line1 in enumerate(lines1):
  line2 = lines2[iline]
  if line1.startswith('<L>'):
   metaline1 = line1
   
  if line1 == line2:
   continue
  changes.append(Change(iline,line1,line2,metaline1))
 #
 write_changes(fileout,changes)
 
