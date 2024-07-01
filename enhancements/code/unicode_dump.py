#-*- coding:utf-8 -*-
"""unicode_dump.py
 
  python unicode_dump.py input.txt output.txt


"""
from __future__ import print_function
import sys, re,codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

def write_lines(fileout,outarr):
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out+'\n')
 print(len(outarr),"lines written to",fileout)

def unicode_to_hex(u):
 """ Sample output:
u = arbitrary unicode
0905 | अ | DEVANAGARI LETTER A
0951 | ॑ | DEVANAGARI STRESS SIGN UDATTA
0902 | ं | DEVANAGARI SIGN ANUSVARA
0936 | श | DEVANAGARI LETTER SHA
2014 | — | EM DASH
092D | भ | DEVANAGARI LETTER BHA
0942 | ू | DEVANAGARI VOWEL SIGN UU
0951 | ॑ | DEVANAGARI STRESS SIGN UDATTA
 """
 import unicodedata
 outarr = []
 # outarr.append('INPUT = %s' %u)
 for c in u:
  try:
   name = unicodedata.name(c)
  except:
   if c == '\n':
    name = '{{NEWLINE}}'
   else:
    name = 'NO NAME'
  icode = ord(c)
  a = f"{icode:04X} | {c} | {name}"
  outarr.append(a)
 return outarr


if __name__=="__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 lines = read_lines(filein)
 text = '\n'.join(lines)
 outarr = unicode_to_hex(text)
 write_lines(fileout,outarr)
