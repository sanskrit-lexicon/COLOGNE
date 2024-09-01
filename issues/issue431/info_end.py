#-*- coding:utf-8 -*-
""" info_end
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
  
 if False: # dbg
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

def revise_k2_ab_cdsl(lgroups):
 #for entry in entries:
 # newmetaline = ab_cdsl_metaline_hom(entry)
 # entry.metaline = newmetaline
 for lgroup in lgroups:
  Ls = lgroup.Ls
  k2s = lgroup.k2s
  nLs = len(Ls)
  nk2s = len(k2s)
  entries = lgroup.entries
  nentries = len(entries)
  if (nLs != nk2s) or (nLs != nentries):
   print('revise_hom_ab_cdsl: ERROR 1. nLs = %s, nk2s = %s, nentries = %s' %
         (nLs, nk2s, nentries))
   exit(1)
  # Expect that all k2s are same
  oldk2 = k2s[0]
  for k2 in k2s:
   assert k2 == oldk2
  newk2s = oldk2.split(', ')
  assert len(newk2s) == nLs
  for i,L in enumerate(Ls):
   newk2 = newk2s[i]
   entry = entries[i]
   oldmetaline = entry.metaline
   newmetaline = oldmetaline.replace('<k2>'+oldk2, '<k2>'+newk2)
   entry.metaline = newmetaline
   # also need to recompute entry.metad
   entry.metad = digentry.parseheadline(entry.metaline)

def revise_h_ab_cdsl(entries):
 print('enter revise_h_ab_cdsl')
 n = 0
 print('process %s entries' % len(entries))
 for entry in entries:
  metaline = entry.metaline
  oldk2 = entry.metad['k2']
  # example oldk2: '1. arva/'
  m = re.search(r'^([^ ]+)\. (.*)$',oldk2)
  if False and (entry.metad['L'] == '1078'): #debug
   print('chk1\nmetaline=\n%s\noldk2 = %s' % (metaline,oldk2))
  if m == None:
   # no homonym. so no change to metaline
   continue
  h = m.group(1)
  newk2 = m.group(2)
  newk2h = '%s<h>%s' %(newk2,h)
  newmetaline = metaline.replace('<k2>' + oldk2, '<k2>' + newk2h)
  entry.metaline = newmetaline
  entry.metad = digentry.parseheadline(entry.metaline)
  n = n + 1
  if False:
   if entry.metad['L'] == '1078':
    print('revise_h_ab_cdsl check')
    print('metaline = %s\noldk2 = %s' %(metaline,oldk2))
    print('newk2 = %s\nnewk2h = %s\n newmeta = %s' %(newk2,newk2h,newmetaline))
    #exit(1)
 print('revise_h_ab_cdsl: %s metalines changed' % n)
 
def write_lgroups(fileout,lgroups):
 outarr = []
 for igroup,lgroup in enumerate(lgroups):
  entries = lgroup.entries
  Ls = lgroup.Ls
  outarr.append('%04d group has %s entries' %(igroup+1,len(entries)))
  for i,L in enumerate(Ls):
   entry = entries[i]
   metaline = entry.metaline
   outarr.append('  %s' % metaline)
  outarr.append('')
 write_lines(fileout,outarr)
 
if __name__=="__main__":
 option = sys.argv[1]
 assert option in ('cdsl,ab','ab,cdsl')
 filein = sys.argv[2] #  xxx.txt (path to digitization of xxx)
 fileout = sys.argv[3] #
 fileout1 = sys.argv[4]  # misc. helpful output
 
 entries = digentry.init(filein)
 Ldict = digentry.Entry.Ldict;

 if option == 'cdsl,ab':
  revise_hom_cdsl_ab(entries)
  write_entries(fileout,entries)
  print(len(entries),'new entries written to',fileout)
 else:
  lgroups = init_Lgroups_cdsl(entries)
  #print('debug write lgroups to',fileout)
  write_lgroups(fileout1,lgroups)
  # change k2 metalines for groups (from multiple to single)
  # group-entry metalines are revised
  revise_k2_ab_cdsl(lgroups)
  # revise metaline for entries with hom in k2
  revise_h_ab_cdsl(entries)
  write_entries(fileout,entries)
  print(len(entries),'new entries written to',fileout)
  
