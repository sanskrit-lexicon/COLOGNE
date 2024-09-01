#-*- coding:utf-8 -*-
""" convert_metaline_pw.py
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

class Group:
 def __init__(self,key):
  self.key = key  # L1,X1;L2,X2; ...
  self.ientries = []
  self.Lk1s = key.split(';')
  self.Ls = []
  self.k1s = []
  for Lk1 in self.Lk1s:
   try:
    (L,k1) = Lk1.split(',')
    self.Ls.append(L)
    self.k1s.append(k1)
   except:
    print('Group error:',key)
    exit(1)

class LGROUP:
 def __init__(self,Lbody):
  self.Ls = [Lbody]
  self.entries = []
  self.k2s = []
  self.homs = []
  self.k2homs = []
  self.k2ab = None
  self.newmeta = None
  
def get_k2homs(k2s,homs):
 arr = []
 for i,k2 in enumerate(k2s):
  hom = homs[i]
  if hom == None:
   x = k2
   arr.append(x)
   continue
  x = '%s. %s' %(hom,k2)
  arr.append(x)
 return arr

def init_Lgroups_cdsl(entries):
 ientries_lbody = []
 n = 0
 for ientry,entry in enumerate(entries):
  text = ' '.join(entry.datalines)
  m = re.search(r'{{Lbody=(.*?)}}',text)
  if m != None:
   Lbody = m.group(1)
   ientries_lbody.append((ientry,Lbody))
 print('init_groups_cdsl finds %s Lbody entries' % len(ientries_lbody))
 #
 groupsd = {}
 groups = []
 for i,temp in enumerate(ientries_lbody):
  ientry,Lbody = temp
  if Lbody not in groupsd:
   group = LGROUP(Lbody)
   groups.append(group)
   groupsd[Lbody] = group
  group = groupsd[Lbody]
  entry = entries[ientry]
  L = entry.metad['L']
  group.Ls.append(L)
 #
 # compute additional attributes of Lgroup objects
 for group in groups:
  for L in group.Ls:
   entry = digentry.Entry.Ldict[L]
   group.entries.append(entry)
   k2 = entry.metad['k2']
   group.k2s.append(k2)
   if 'h' in entry.metad:
    hom = entry.metad['h']
    m = re.search(r'^[0-9]+$',hom)
    if not m:  # non-numeric hom!
     print('WARNING: non-numeric hom: metaline=\n%s' % entry.metaline)
   else:
    hom = None
   group.homs.append(hom)
  # generate revised k2
  group.k2homs = get_k2homs(group.k2s,group.homs)
  group.k2ab = ','.join(group.k2homs)
  # new metaline
  entry0 = group.entries[0]
  meta = entry0.metaline
  metad = entry0.metad
  if 'e' in metad: # mw
   eval = metad['e']
   newe = '<e>%s' % eval
  else:
   newe = ''
  meta1 = re.sub(r'<k2>.*$','',meta)  # so L,pc,k1 remain in meta1
  newk2 = group.k2ab
  meta2 = '%s<k2>%s%s' %(meta1,newk2,newe)  #
  group.newmeta = meta2
  
 if True: # dbg
  for igroup,group in enumerate(groups):
   if igroup > 5:
    break
   print('groupLs %04d: %s' % (igroup+1,group.Ls))
   print('  newmeta=',group.newmeta)
 return groups

def write_entries(fileout,entries):
 outrecs = []
 for entry in entries:
  outrec = write_entries_helper(entry)
  outrecs.append(outrec)
 write_recs(fileout,outrecs,blankflag=False)

def cdsl_ab_metaline(entry):
 metad = entry.metad
 L = metad['L']
 pc = metad['pc']
 k1 = metad['k1']
 k2 = metad['k2']
 if 'e' in metad: # mw
  eval = metad['e']
  newe = '<e>%s' % eval
 else:
  newe = ''
 if 'h' in metad:
  hval = metad['h']
  newh = '%s. ' % hval
 else:
  newh = ''
 oldmeta = entry.metaline
 meta1 = re.sub(r'<k2>.*$','',oldmeta)  # so L,pc,k1 remain in meta1
 newk2val = '%s%s' %(newh,k2)
 meta2 = '%s<k2>%s' %(meta1,newk2val)
 newmeta = '%s%s' %(meta2,newe)

 if False and (newh != ''): # dbg
  print('old metaline: %s' % oldmeta)
  print('new metaline: %s' % newmeta)
  exit(1)
 return newmeta

def revise_hom_cdsl_ab(entries):
 newentries = []
 for entry in entries:
  newmetaline = cdsl_ab_metaline(entry)
  entry.metaline = newmetaline

def ab_cdsl_metaline_hom(entry):
 metad = entry.metad
 L = metad['L']
 pc = metad['pc']
 k1 = metad['k1']
 k2 = metad['k2']
 if ',' in k2:
  print('ab_cdsl_metaline_hom unexpected k2',k2)
  print(entry.metaline)
  exit(1)
 if 'e' in metad: # mw
  eval = metad['e']
  newe = '<e>%s' % eval
 else:
  newe = ''
 oldmeta = entry.metaline
 meta1 = re.sub(r'<k2>.*$','',oldmeta)  # so L,pc,k1 remain in meta1
 m = re.search(r'^([^ ]+)\. (.*)$',k2)
 if m == None:
  # no homonym
  newmeta = '%s<k2>%s%s' % (meta1,k2,newe)
 else:
  h = m.group(1)
  newk2 = m.group(2)
  newmeta ='%s<k2>%s<h>%s%s' %(meta1,newk2,h,newe)

 if False and (m != None): # dbg
  print('ab_cdsl_metaline_hom')
  print('old metaline: %s' % oldmeta)
  print('new metaline: %s' % newmeta)
  exit(1)
 return newmeta

def revise_hom_ab_cdsl(entries):
 newentries = []
 for entry in entries:
  newmetaline = ab_cdsl_metaline_hom(entry)
  entry.metaline = newmetaline

def unused_ab_cdsl_metaline_k2(entry):
 metad = entry.metad
 L = metad['L']
 pc = metad['pc']
 k1 = metad['k1']
 k2 = metad['k2']
 if 'e' in metad: # mw
  eval = metad['e']
  newe = '<e>%s' % eval
 else:
  newe = ''
 oldmeta = entry.metaline
 meta1 = re.sub(r'<k2>.*$','',oldmeta)  # so L,pc,k1 remain in meta1
 m = re.search(r'^([^ ]+)\. (.*)$',k2)
 if m == None:
  # no homonym
  newmeta = '%s<k2>%s%s' % (meta1,k2,newe)
 else:
  h = m.group(1)
  newk2 = m.group(2)
  newmeta ='%s<k2>%s<h>%s%s' %(meta1,newk2,h,newe)

 if False and (m != None): # dbg
  print('ab_cdsl_metaline_hom')
  print('old metaline: %s' % oldmeta)
  print('new metaline: %s' % newmeta)
  exit(1)
 return newmeta

def revise_k2_ab_cdsl(entries):
 groups = []
 ientry = 0
 nentries = len(entries)
 while ientry < nentries:
  entry = entries[ientry]
  k2 = entry.metad['k2']
  if ',' not in k2:
   ientry = ientry + 1
   continue
  group = []
  parts = k2.split(', ')
  n = len(parts)
  for i in range(n):
   if i == 0:
    group.append(ientry)
    continue
   ientry1 = ientry + i
   entry1 = entries[ientry1]
   text = ' '.join(entry1.datalines)
   m = re.search(r'{{Lbody=(.*?)}}',text)
   if m == None:
    print('revise_k2_ab_cdsl error 1')
    print(entry.metaline)
    exit(1)
   # check that entry1
   group.append(ientry1)
   k2_1 = entry1.metad['k2']
   assert k2_1 == k2
  groups.append(group)
  ientry = ientry + n
 print('revise_k2_ab_cdsl found %s groups, with identical k2' % len(groups))
 # --------
 nchg = 0
 # change metaline for all groups
 for group in groups:
  ientry0 = group[0]
  entry0  = entries[ientry0]
  k2 = entry0.metad['k2']
  k2s = k2.split(', ')
  if len(k2s) != len(group):
   print('revise_k2_ab_cdsl: error 2')
   exit(1)
  for i,ientry in enumerate(group):
   k2 = k2s[i]
   entry = entries[ientry]
   metaline = entry.metaline
   meta1 = re.sub(r'<k2>.*$', '<k2>',metaline)
   newmeta = meta1 + k2
   entry.metaline = newmeta  # revise this
   entry.metad = digentry.parseheadline(newmeta)
   nchg = nchg + 1
 print('revise_k2_ab_cdsl changes %s metalines' % nchg)
if __name__=="__main__":
 option = sys.argv[1]
 assert option in ('cdsl,ab','ab,cdsl')
 filein = sys.argv[2] #  xxx.txt (path to digitization of xxx)
 fileout = sys.argv[3] # 
 entries = digentry.init(filein)
 Ldict = digentry.Entry.Ldict;

 if option == 'cdsl,ab':
  revise_hom_cdsl_ab(entries)
  write_entries(fileout,entries)
  print(len(entries),'new entries written to',fileout)
 else:
  revise_k2_ab_cdsl(entries)
  revise_hom_ab_cdsl(entries)
  write_entries(fileout,entries)
  print(len(entries),'new entries written to',fileout)
  
