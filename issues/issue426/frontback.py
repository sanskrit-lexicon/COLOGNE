#-*- coding:utf-8 -*-
""" frontback.py

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
 
def analyze_lines(lines):
 ifirst = None
 ilast = None
 for i,line in enumerate(lines):
  if line.startswith('<L>'):
   if ifirst == None:
    ifirst = i
  if line.startswith('<LEND>'):
   ilast = i
 print(ifirst,ilast)
 return (ifirst,ilast)

def skip_empty_lines(lines):
 newlines = []
 n = 0
 for line in lines:
  if re.search(r'^ *$',line):
   n = n + 1
   continue
  newlines.append(line)
 print('skip_empty_lines',n)
 return newlines
  
if __name__=="__main__":
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx)
 filemain = sys.argv[2] # xxx.txt
 filefront = sys.argv[3]
 fileback = sys.argv[4]
 
 lines = read_lines(filein)
 ifirst,ilast = analyze_lines(lines)
 # ,frontlines,backlines
 frontlines = lines[:ifirst]
 mainlines = skip_empty_lines(lines[ifirst:ilast + 1])
 backlines = lines[ilast+1:]
 write_lines(filemain,mainlines)
 write_lines(filefront,frontlines)
 write_lines(fileback,backlines)
 
