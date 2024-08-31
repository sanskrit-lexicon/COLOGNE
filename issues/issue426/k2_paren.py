#-*- coding:utf-8 -*-
""" k2_paren.py
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

class Extra:
 def __init__(self,line):
  self.line = line
  regex = r'^<L>(.*?)<pc>(.*?)<k1>(.*?)<k2>(.*?)<type>(.*?)<LP>(.*?)<k1P>(.*?)$'
  m = re.search(regex,line)
  if m == None:
   print('Extra init problem')
   print(line)
   exit(1)
  self.L = m.group(1)
  self.pc = m.group(2)
  self.k1 = m.group(3)
  self.k2 = m.group(4)
  self.type = m.group(5)
  self.LP = m.group(6)
  self.k1P = m.group(7)
  self.status = False
  self.method = None
 def get_abc(self):
  return a,b,c

def get_abc(k2):
 m = re.search(r'^([^<]*)\(([^<]+)\)([^<]*)$',k2)
 if m == None:
  print('get_abc problem:',k2)
  return 'x','y','z'

 # a(b)c
 a = m.group(1) # before () elt
 b = m.group(2) # () elt
 c = m.group(3) # after () elt
 return a,b,c

def check_k1_k2(k1,k2):
 newk1 = re.sub(r'[˚-]','',k2)
 return newk1 == k1

vowel_sandhi_replacements = [
 ('a-a','A'),
 ('a-A','A'),
 ('A-a','A'),
 ('A-A','A'),
 ('a-u','o'),
 ('A-I','e'),
 ]
def apply_vowel_sandhi(x):
 # a-a -> A, etc.
 for old,new in vowel_sandhi_replacements:
  x = x.replace(old,new)
 return x

def adjust_rec_1(rec):
 """
OLD:
<L>00085.1<pc>002-32<k1>akUvAra<k2>akUpA(vA)ra<type>alt<LP>00085<k1P>akUpAra
NEW
<L>00085.1<pc>002-32<k1>akUvAra<k2>akUvAra<type>alt<LP>00085<k1P>akUpAra

"""
 a,b,c = get_abc(rec.k2)
 oldk2 = a + '(' + b + ')' + c
 assert oldk2 == rec.k2
 
 # construct newk2
 nb = len(b) # number of characters in b
 # remove nb characters from end of a
 nb = len(b)
 a1 = a[:-nb]  
 newk2 = a1 + b + c
 newk2a = apply_vowel_sandhi(newk2)
 #if rec.L == '21397.2':
 # print('adjust_rec_1:',a,b,c,newk2,newk2a)
 newline = rec.line.replace('<k2>' + oldk2, '<k2>' + newk2a)
 if check_k1_k2(rec.k1,newk2a):
  rec.newline = newline
  rec.status = True
  rec.method = 'm1'

def adjust_rec_2(rec):
 a,b,c = get_abc(rec.k2)
 oldk2 = a + '(' + b + ')' + c
 assert oldk2 == rec.k2
 # Xn(nI) -> XnI
 if not (a.endswith('n') and (b in ['nI','RI']) and (c == '')):
  return
 newk2 = a[:-1] + b
 newk2a = apply_vowel_sandhi(newk2)
 newline = rec.line.replace('<k2>' + oldk2, '<k2>' + newk2a)
 #if rec.L == '21397.2':
 # print('adjust_rec_2:',a,b,c,newk2,newk2a)
 # check
 if check_k1_k2(rec.k1,newk2a):
  rec.newline = newline
  rec.status = True
  rec.method = 'm2'

def adjust_rec_3(rec):
 a,b,c = get_abc(rec.k2)
 oldk2 = a + '(' + b + ')' + c
 assert oldk2 == rec.k2
 # XY(YW)Z -> XYWZ
 aend = a[-1]
 if rec.L == '21397.2':
  print('adjust_rec_3: a=%s, b=%s, c=%s, aend=%s, b0=%s' % (a,b,c,aend,b[0]))
 if not b.startswith(aend):
  return
 newk2 = a[:-1] + b + c
 newk2a = apply_vowel_sandhi(newk2)
 newline = rec.line.replace('<k2>' + oldk2, '<k2>' + newk2a)
 if check_k1_k2(rec.k1,newk2a):
  rec.newline = newline
  rec.status = True
  rec.method = 'm3'

def adjust_rec_4(rec):
 a,b,c = get_abc(rec.k2)
 oldk2 = a + '(' + b + ')' + c
 assert oldk2 == rec.k2
 # Xtf(trI) -> XtrI
 # if rec.L == '12761.1':
 # print(a,b,c,newk2,rec.k1)
 if not a.endswith('tf'):
  return
 if b != 'trI':
  return
 if c != '':
  return
 newk2 = a[:-2] + b
 newk2a = apply_vowel_sandhi(newk2)
 newline = rec.line.replace('<k2>' + oldk2, '<k2>' + newk2a)
 if check_k1_k2(rec.k1,newk2a):
  rec.newline = newline
  rec.status = True
  rec.method = 'm4'

def adjust_rec_5(rec):
 a,b,c = get_abc(rec.k2)
 oldk2 = a + '(' + b + ')' + c
 assert oldk2 == rec.k2
 # XYtf(YtrI) -> XYtrI
 if not a.endswith('tf'):
  return
 y = a[-3]
 if b != (y + 'trI'):
  return
 if c != '':
  return
 newk2 = a[:-3] + b
 newk2a = apply_vowel_sandhi(newk2)
 newline = rec.line.replace('<k2>' + oldk2, '<k2>' + newk2a)
 if check_k1_k2(rec.k1,newk2a):
  rec.newline = newline
  rec.status = True
  rec.method = 'm5'

def adjust_rec_6(rec):
 a,b,c = get_abc(rec.k2)
 oldk2 = a + '(' + b + ')' + c
 assert oldk2 == rec.k2
 # t(ntI)

 if not a.endswith('t'):
  return
 if b != 'ntI':
  return
 newk2 = a[:-1] + b + c
 newk2a = apply_vowel_sandhi(newk2)
 newline = rec.line.replace('<k2>' + oldk2, '<k2>' + newk2a)
 if check_k1_k2(rec.k1,newk2a):
  rec.newline = newline
  rec.status = True
  rec.method = 'm6'

def adjust_rec_7(rec):
 a,b,c = get_abc(rec.k2)
 oldk2 = a + '(' + b + ')' + c
 assert oldk2 == rec.k2
 # XYu(YvI) -> XYvI

 if not a.endswith('u'):
  return
 if not (b == (a[-2] + 'vI')):
  return 
 newk2 = a[:-2] + b + c
 newk2a = apply_vowel_sandhi(newk2)
 newline = rec.line.replace('<k2>' + oldk2, '<k2>' + newk2a)
 if check_k1_k2(rec.k1,newk2a):
  rec.newline = newline
  rec.status = True
  rec.method = 'm7'

def adjust_rec_8(rec):
 a,b,c = get_abc(rec.k2)
 oldk2 = a + '(' + b + ')' + c
 assert oldk2 == rec.k2
 # UrDva(rdDva) -> UrdDva
 if not a.endswith('UrDva'):
  return
 if not b == 'rdDva':
  return 
 newk2 = a[:-4] + b + c
 newk2a = apply_vowel_sandhi(newk2)
 newline = rec.line.replace('<k2>' + oldk2, '<k2>' + newk2a)
 if check_k1_k2(rec.k1,newk2a):
  rec.newline = newline
  rec.status = True
  rec.method = 'm8'

def adjust_rec_9(rec):
 a,b,c = get_abc(rec.k2)
 oldk2 = a + '(' + b + ')' + c
 assert oldk2 == rec.k2
 # 
 if not a.endswith('a'):
  return
 if b != (a[-2] + 'y' + 'a'):
  return
 
 newk2 = a[:-2] + b + c
 newk2a = apply_vowel_sandhi(newk2)
 newline = rec.line.replace('<k2>' + oldk2, '<k2>' + newk2a)
 if check_k1_k2(rec.k1,newk2a):
  rec.newline = newline
  rec.status = True
  rec.method = 'm9'

def adjust_rec_10(rec):
 a,b,c = get_abc(rec.k2)
 oldk2 = a + '(' + b + ')' + c
 assert oldk2 == rec.k2
 # 
 if not a.endswith('ya'):
  return
 if b != (a[-3] + 'a'):
  return
 newk2 = a[:-3] + b + c
 newk2a = apply_vowel_sandhi(newk2)
 newline = rec.line.replace('<k2>' + oldk2, '<k2>' + newk2a)
 if check_k1_k2(rec.k1,newk2a):
  rec.newline = newline
  rec.status = True
  rec.method = 'm10'

def adjust_rec_11(rec):
 a,b,c = get_abc(rec.k2)
 oldk2 = a + '(' + b + ')' + c
 assert oldk2 == rec.k2
 # 
 if not b.endswith('t'):
  return
 if not a.endswith(b[:-1]):
  return
 newk2 = a + 't'
 newk2a = apply_vowel_sandhi(newk2)
 newline = rec.line.replace('<k2>' + oldk2, '<k2>' + newk2a)
 if check_k1_k2(rec.k1,newk2a):
  rec.newline = newline
  rec.status = True
  rec.method = 'm11'

def adjust_rec_12(rec):
 a,b,c = get_abc(rec.k2)
 oldk2 = a + '(' + b + ')' + c
 assert oldk2 == rec.k2
 #
 m = re.search(r'^(.*)(r.*)$',a)
 if m == None:
  return
 a1 = m.group(1)
 a2 = m.group(2)
 if not b.startswith('r'):
  return
 newk2 = a1 + b + c
 newk2a = apply_vowel_sandhi(newk2)
 newline = rec.line.replace('<k2>' + oldk2, '<k2>' + newk2a)
 if check_k1_k2(rec.k1,newk2a):
  rec.newline = newline
  rec.status = True
  rec.method = 'm12'

def adjust_rec_13(rec):
 a,b,c = get_abc(rec.k2)
 oldk2 = a + '(' + b + ')' + c
 assert oldk2 == rec.k2
 #
 b0 = b[0]
 m = re.search(r'^(.*)(%s.*)$' % b0,a)
 if m == None:
  return
 a1 = m.group(1)
 a2 = m.group(2)
 newk2 = a1 + b + c
 newk2a = apply_vowel_sandhi(newk2)
 newline = rec.line.replace('<k2>' + oldk2, '<k2>' + newk2a)
 if check_k1_k2(rec.k1,newk2a):
  rec.newline = newline
  rec.status = True
  rec.method = 'm13'

def adjust_rec_0(rec):
 # must handle all cases with no paren in k2
 if '(' in rec.k2:
  return
 oldk2 = rec.k2
 newk2 = rec.k2 # no change
 newk2a = apply_vowel_sandhi(newk2)
 newline = rec.line.replace('<k2>' + oldk2, '<k2>' + newk2a)
 if check_k1_k2(rec.k1,newk2a):
  rec.newline = newline
  rec.status = True
  rec.method = 'm0'
 else:
  print('ERROR: adjust_rec_0 fails.')
  print(rec.k2)
  exit(1)
  
def adjust_rec(rec):
 rec.newline = rec.line # default
 # various methods required
 adjust_rec_0(rec)  # no parens, only a few
 if not rec.status: 
  adjust_rec_1(rec)
 if not rec.status:
  adjust_rec_2(rec)
 if not rec.status:
  adjust_rec_3(rec)
 if not rec.status:
  adjust_rec_4(rec)
 if not rec.status:
  adjust_rec_5(rec)
 if not rec.status:
  adjust_rec_6(rec)
 if not rec.status:
  adjust_rec_7(rec)
 if not rec.status:
  adjust_rec_8(rec)
 if not rec.status:
  adjust_rec_9(rec)
 if not rec.status:
  adjust_rec_10(rec)
 if not rec.status:
  adjust_rec_11(rec)
 if not rec.status:
  adjust_rec_12(rec)
 if not rec.status:
  adjust_rec_13(rec)
 #if not rec.status:
 # adjust_rec_14(rec)

def count_methods(recs):
 methods = [None,'m0','m1','m2','m3','m4','m5','m6','m7',
            'm8','m9','m10','m11','m12','m13']
 d = {}
 for method in methods:
  d[method] = 0
 for rec in recs:
  d[rec.method] = d[rec.method] + 1
 for method in methods:
  print(method,d[method])

class METALINE:
 def __init__(self,line):
  self.line = line
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

def remove_k2_parens_helper(line):
 rec = METALINE(line)
 if '(' not in rec.k2:
  return line
 newline = re.sub(r'\(.*?\)', '', line)
 return newline

def remove_k2_parens(lines):
 nchg = 0
 newlines = []
 for line in lines:
  if not line.startswith('<L>'):
   newlines.append(line)
   continue
  newline = remove_k2_parens_helper(line)
  newlines.append(newline)
  if newline != line:
   nchg = nchg + 1
 print('remove_k2_parens: %s lines changed' %nchg)
 return newlines

def check_all_k2_k1_helper(line):
 rec = METALINE(line)
 k1 = rec.k1
 k2 = rec.k2
 flag = check_k1_k2(k1,k2)
 if not flag:
  print('k1-k2 WARNING:',line)
 return flag

def check_all_k2_k1(lines):
 n = 0
 for line in lines:
  if not line.startswith('<L>'):
   continue
  if not check_all_k2_k1_helper(line):
   n = n + 1
 print('check_all_k2_k1 finds %s inconsistencies' % n)
 
if __name__=="__main__":
 filein = sys.argv[1] #  
 fileout = sys.argv[2] # 
  
 lines = read_lines(filein)
 newlines = remove_k2_parens(lines)
 write_lines(fileout,newlines)
 # check_all_k2_k1(newlines)
 
