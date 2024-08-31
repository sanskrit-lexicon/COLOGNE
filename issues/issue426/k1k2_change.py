#-*- coding:utf-8 -*-
""" k1k2_change.py
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

def check_k1_k2(k1,k2):
 newk1 = re.sub(r'[˚-]','',k2)
 return newk1 == k1

vowel_sandhi_replacements = [
 ('a-a','A'), ('a-A','A'), ('A-a','A'), ('A-A','A'),
 ('i-i','I'), ('i-I','I'), ('I-i','I'), ('I-I','I'),
 ('u-u','U'), ('u-U','U'), ('U-u','U'), ('U-U','U'),
 
 ('a-u','o'), ('a-U','o'), ('A-u','o'), ('A-U','o'),
 ('a-i','e'), ('a-I','e'), ('A-i','e'), ('A-I','e'),
 ('a-e','E'), ('A-e','E'), ('a-E','E'), ('A-E','E'),
 ('a-o','O'), ('A-o','O'), ('a-O','O'), ('A-O','O'),
 ('a-f','ar'),
 ('i-a','ya'), ('i-A','yA'), ('i-u','yu'), ('i-U','yU'),
 ('i-e','ye'),  ('i-E','yE'),  ('i-o','yo'),  ('i-O','yO'), 
 ('i-f','yf'),
 ('I-a','ya'), ('I-A','yA'), ('I-u','yu'), ('I-U','yU'),
 ('I-e','ye'),  ('I-E','yE'),  ('I-o','yo'),  ('I-O','yO'),
 
 ('u-a','va'), ('u-A','vA'), ('u-i','vi'), ('u-I','vI'), ('u-f','vf'),
 ('u-O', 'vO'), ('u-e','ve'),
 ('A-f','ar'),
 ('f-a', 'ra'), ('f-A','rA'),

 ('as˚B', 'oB'), ('as˚m', 'om'),
 
 ]

def apply_vowel_sandhi(x):
 # a-a -> A, etc.
 for old,new in vowel_sandhi_replacements:
  x = x.replace(old,new)
 return x

class METALINE:
 def __init__(self,iline,line):
  self.iline = iline
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
  # is k2 consistent with k1 ? (using
  self.status = False   # default: not consistent
  self.status_rev = False  # after adjustment
  self.newk2 = None
  self.newline = None
  self.method = None

def init_extras(lines):
 extras = []
 for iline,line in enumerate(lines):
  if not line.startswith('<L>'):
   continue
  rec = METALINE(iline,line)
  status = check_k1_k2(rec.k1,rec.k2)
  rec.status = status
  if not status:
   extras.append(rec)
 print(len(extras),"metalines marked as k2-k1 inconsistent")
 return extras

cpd_stem_replacements = [
 # very specific

 # less specific
 ('s-c','S-c'), ('s-C','S-C'),
 ('an-a','A'), ('an-A','A'),
 ('as-a','o'), ('an-e','E'), ('an-u','o'), ('an-i','e'), ('an-I','e'),
 ('an-f','ar'), ('an-o','O'), ('an-I','e'),
 ('an-','a-'), 
 ('as-k', 'aHk'), ('as-K', 'aHK'), ('as-g','og'), ('as-G','oG'),
 ('as-d', 'od'),  ('as-D', 'oD'),  ('as-n', 'on'),  
 ('as-b', 'ob'),  ('as-B', 'oB'),  ('as-m', 'om'),
 ('as-p', 'aHp'), ('as-P', 'aHP'),
 ('as-y', 'oy'),  ('as-r', 'or'),  ('as-l', 'ol'),  ('as-v', 'ov'),
 ('as-a', "o"), ('as-s','aHs'), ('as-S','aHS'), ('as-z','aHz'),
 ('ar-k','aHk'), ('ar-t','ast'), ('ar-p','aHp'), ('ar-s', 'aHs'), ('ar-S', 'aHS'),
 ('as-u','au'), 
 ('an˚a','A'),  ('an˚A','A'), 
 ('an˚','a-'),  ('d-k','t-k'), ('d-j','jj'),
 ('us-s','uHs'), ('us-S','uHS'), ('ur-z', 'uHz'), ('ur-s','uHs'),
 ('d-t','tt'),  ('d-p','tp'), ('d-s','ts'),('d-m','nm'),
 ('D-n','nn'), ('D-k','tk'), ('D-p','tp'), ('d-c','cc'), 
 ('t-m','nm'),  ('t-v','dv'), ('t-a','da'), ('t-A','dA'),
 ('a-C','acC'), ('t-c','cc'), ('t-n','nn'), ('t-B','dB'), ('t-b','db'), ('t-r','dr'), 
 ('t-e','de'), ('t-g','dg'),  ('t-u','du'), ('t-i','di'), ('t-j','jj'), ('t-y','dy'),
 ('t-D','dD'), ('t-d','dd'), ('t-y','dy'), ('t-h','dD'), ('t-I','dI'), 
 ('t-l','ll'), ('t-I','dI'),
 ('is-i','iri'),
 ('ac-s','aks'),
 ('am-d','aMd'), ('am-t','aMt'), ('am-p','aMp'),
 ('Am-','AM'), ('am-','aM'), ('Um-k', 'UMk'),
 ('nf-a', 'narA'),
 ('in-i','I'), ('in-I','I'), ('in-a','ya'), ('in-A', 'yA'),
 ('in-','i'),
 ('c-p','kp'), ('c-P','kP'), ('c-b','gb'), ('c-B','gB'),
 ('c-v','gv'), ('c-S','kS'),   ('c-d','gd'),  ('c-s','ks'),
 ('c-t','kt'), ('c-j','gj'), ('c-c','kc'),  ('c-k','kk'), ('c-a','ga'), ('c-A','gA'),
 ('j-v', 'gv'), ('j-s','ks'), ('us-p','uzp'),
 ('um-k', 'uMk'), ('am-B', 'aMB'), ('am-v', 'aMv'),  ('am-g', 'aMg'), ('am-c', 'aMc'),
 ('an-o','O'), ('am-k','aMk'), ('im-c','iMc'), ('im-C','iMC'), ('im-k', 'iMk'),
 
 ('im-t','iMt'), ('im-n','iMn'), ('im-p','iMp'), ('im-B','iMB'), ('im-r', 'iMr'),
 ('im-v','iMv'), ('im-S','iMS'), ('im-s','iMs'), ('im-g','iMg'), ('im-d','iMd'),
 ('im-D','iMD'), ('Im-S','IMS'),
 ('k-B','gB'), ('k-A','gA'), ('k-j','gj'), ('k-r','gr'), ('k-v','gv'), ('k-d','gd'),
 ('us-k', 'uzk'), ('us-d','urd'), ('us-v','urv'),
 ('u-C','ucC'), ('m_S', 'MS'), ('m-B','MB'),
 ('s-S','HS'), ('s-k','Hk'), ('s-G','rG'),
 ('m-t','Mt'), ('m-p','Mp'), 
 ('t˚B', 'dB'), ('t˚v','dv'),
 #  even more specific
 ('an˚a', 'A'),  
 ]
def apply_cpd_stem(x):
 for old,new in cpd_stem_replacements:
  y = x.replace(old,new)
  if False and (old == 'am-p') and (y != x):
   print('stemchk: x=%s, y=%s, old=%s, new=%s' %(x,y,old,new))
  if y != x:
   return y
 return x

def revise_extra_helper1(rec,newk2):
 rec.status = True
 rec.status_rev = True
 rec.newk2 = newk2
 rec.method = 'vowel-sandhi'
 rec.newline = rec.line.replace('<k2>' + rec.k2, '<k2>' + rec.newk2)

specific_newk2 =  {
  "agra-anIka" : "agrARIka",  # agrARIka
  "atas-arTam" : "ato'rTam",  # ato'rTam
  "atas-arTAt" : "ato'rTAt",  # ato'rTAt
  "atas-UrDvam" : "ata-UrDvam",  # ataUrDvam
  "atas-eva" : "ata-eva",  # ataeva
  "aDara-ozWa" : "aDarozWa",  # aDarozWa
  "antar-pura˚aDyakza" : "antaH-purADyakza",  # antaHpurADyakza
  "arTa-tas˚gOravam" : "arTa-to-gOravam",  # arTatogOravam
  "azwan-guRa˚ASraya" : "azwa-guRASraya",  # azwaguRASraya
  "azwan-rasa˚ASraya" : "azwa-rasASraya",  # azwarasASraya
  "azwan-aMga˚arGa" : "azwAMgArGa",  # azwAMgArGa
  "ahi-Catraka" : "ahi-cCatraka",  # ahicCatraka
  "uttara-ayana" : "uttarAyaRa",  # uttarAyaRa
  "uttara-ozWa" : "uttarozWa",  # uttarozWa
  "uttara-diS˚ISa" : "uttara-digISa",  # uttaradigISa
  "uttara-diS˚pAla" : "uttara-dikpAla",  # uttaradikpAla
  "uBaya-tas˚dat" : "uBaya-to-dat",  # uBayatodat
  "uBaya-tas˚daMta" : "uBaya-to-daMta",  # uBayatodaMta
  "om-kAra" : "oM-kAra",  # oMkAra
  "kim-nara˚ISa" : "kiM-nareSa",  # kiMnareSa
  "kim-nara˚ISvara" : "kiM-nareSvara",  # kiMnareSvara
  "kim-puruza˚ISvara" : "kiM-puruzeSvara",  # kiMpuruzeSvara
  "kim-cit˚jYa" : "kiM-cij-jYa",  # kiMcijjYa
  "kim-cit˚mAtra" : "kiM-cin-mAtra",  # kiMcinmAtra
  "kim-tarhi" : "kin-tarhi",  # kintarhi
  "gUQa-Atman" : "gUQotman",  # gUQotman
  "go-maya˚Canna" : "go-maya-cCanna",  # gomayacCanna
  "Gfta-odana" : "Gftodana",  # Gftodana
  "citra-SiKaMqin˚ja" : "citra-SiKaMqi-ja",  # citraSiKaMqija
  "tatas-tva" : "tatas-tya",  # tatastya
  "daSan-kaMWa˚ari" : "daSa-kaMWAri",  # daSakaMWAri
  "daSan-kaMDara˚ari" : "daSa-kaMDarAri",  # daSakaMDarAri
  "nir-aMtaram˚aByAsa" : "nir-aMtarAByAsa",  # niraMtarAByAsa
  "nf-asTimAlin" : "narAsTimAlin",  # narAsTimAlin
  "paMcan-daSan˚aha" : "paMca-daSAha",  # paMcadaSAha
  "para-CaMda˚anuvartana" : "para-cCaMdAnuvartana",  # paracCaMdAnuvartana
  "brahmafzi" : "brahmafzi",  # brahma‌fzi  k1 is wrong here .hidden char 'aXf'
  "BUta-odana" : "BUtodana",  # BUtodana
  "manaApa" : "manastApa",  # manastApa
  "mahA-ozWa" : "mahozWa",  # mahozWa
  "mahA-ozWa" : "mahozWa",  # mahozWa
  "rAjan-aNgana" : "rAjANgaRa",  # rAjANgaRa
  "ruj-pratikriyA" : "ruk-pratikriyA",  # rukpratikriyA
  "vidyuta-unmeza" : "vidyud-unmeza",  # vidyudunmeza
  "sat-asat˚viveka" : "sad-asad˚viveka",  # sadasadviveka
  "sat-asat˚vyaktihetu" : "sad-asad˚vyaktihetu",  # sadasadvyaktihetu
  "svAmin-upakAraka" : "svAmyupakAraka",  # svAmyupakAraka
 }

def revise_extra_helper(rec):
 if rec.k2 in specific_newk2:
  newk2 = specific_newk2[rec.k2]
  flag = check_k1_k2(rec.k1,newk2)
  if flag:
   revise_extra_helper1(rec,newk2)
   return
  
 newk2 = apply_vowel_sandhi(rec.k2)
 flag = check_k1_k2(rec.k1,newk2)
 if flag:
  revise_extra_helper1(rec,newk2)
  return
 # remove ˚ and retry vowel sandhi
 k2a = re.sub(r'([aAiIuUfFeEoO])˚([aAiIuUfFeEoO])', r'\1-\2',rec.k2)
 newk2b = apply_vowel_sandhi(k2a)
 flag = check_k1_k2(rec.k1,newk2b)
 if False and (rec.L == '16171'):
  print('check: k1=%s, k2=%s, k2a=%s, newk2b=%s, flag=%s' %(rec.k1,rec.k2,k2a,newk2b,flag))
  exit(1)
 if flag:
  revise_extra_helper1(rec,newk2b)
  return
 newk2a = apply_cpd_stem(newk2)
 flag = check_k1_k2(rec.k1,newk2a)
 if flag:
  revise_extra_helper1(rec,newk2a)
  return
 
def revise_extras(extras):
 for extra in extras:
  revise_extra_helper(extra)

def write_changes(fileout,extras):
 outrecs = []
 icase = 0
 for rec in extras:
  if not rec.status_rev:
   continue
  outarr = []
  icase = icase + 1
  outarr.append('; Case %04d' % icase)
  outarr.append('; oldk2: %s' % rec.k2)
  outarr.append('; newk2: %s' % rec.newk2)
  lnum = rec.iline + 1
  outarr.append('%d old %s' % (lnum,rec.line))
  outarr.append('%d new %s' % (lnum,rec.newline))
  outarr.append('; ----------------------------------------------------')
  outrecs.append(outarr)
 write_recs(fileout,outrecs,blankflag = False)

def write_problems(fileout,extras):
 outlines = [rec.line for rec in extras if not rec.status]
 write_lines(fileout,outlines)

def write_problems1(fileout,extras):
 recs = [rec for rec in extras if not rec.status]
 outarr = []
 outarr.append(' {')
 for rec in recs:
  k2 = rec.k2
  k1 = rec.k1
  out = '  "%s" : "%s",  # %s'  %(k2,k2,k1)
  outarr.append(out)
 outarr.append(' }')
 write_lines(fileout,outarr)
 
if __name__=="__main__":
 filein = sys.argv[1] #  
 fileout = sys.argv[2]  
 fileout1 = sys.argv[3]
 
 lines = read_lines(filein)
 extras = init_extras(lines)
 revise_extras(extras)

 write_changes(fileout,extras)
 write_problems(fileout1,extras)
 fileout2 = 'temp_k1k2_work.txt'
 # write_problems1(fileout2,extras)
 
