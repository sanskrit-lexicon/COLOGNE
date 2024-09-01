#-*- coding:utf-8 -*-
""" convert_hwextra_lbody.py
"""
from __future__ import print_function
import sys,re,codecs,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import digentry

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
 write_recs(fileout,outrecs,blankflag=False) # no blank line

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
  self.seqflag = None  # Are group entries sequential
  self.seqflag1 = None # Are bodylines same in groups?
  self.seqflag5 = None # <h>[a-z]
  self.seqflag6 = None # Are metaline-<e> the same in group?
  self.ientrydiffs = []  # updated in check_groups_3
  
def init_groups(entries):
 regexes_raw = []
 regexes = []
 for option in ('or','and'):
  regex_raw = r'<info %s="(.*?)"/>' % option
  regex = re.compile(regex_raw)
  regexes_raw.append(regex_raw)
  regexes.append(regex)
  
 groupd = {}
 groups = []
 n = 0
 for ientry,entry in enumerate(entries):
  text = ' '.join(entry.datalines)
  for regex in regexes:
   for m in re.finditer(regex,text):
    n = n + 1
    data = m.group(1)  # L1,X1;L2,X2; ...
    if data not in groupd:
     group = Group(data)
     groupd[data] = group
     groups.append(group)
    else:
     group = groupd[data]
    group.ientries.append(ientry)

 print('%s entries matching %s' %(n,regexes_raw))
 keys = groupd.keys()
 print('%s groups' % len(keys))
 #check_groups_1(groupd,entries)
 #check_groups_2(groupd,entries)
 return groups

def write_entries1_helper(entry):
 outarr = []
 g = entry.group
 if g.startswith('; BEGIN'):
  outarr.append('') # blank line
  outarr.append(g)
 outarr.append(entry.metaline)
 for line in entry.datalines:
  outarr.append(line)
 outarr.append(entry.lend)
 if g.startswith('; END'):
  outarr.append(g)
  outarr.append('') # blank line
 return outarr

def write_entries(fileout,entries):
 outrecs = []
 for entry in entries:
  outrec = write_entries_helper(entry)
  outrecs.append(outrec)
 write_recs(fileout,outrecs,blankflag=False)
 
def extra_entries(extras):
 for group in groups:
  ientries = group.ientries
  # begin group 
  ientry0 = ientries[0]
  entry0 = entries[ientry0]
  L0 = entry0.metad['L']
  for ientry in ientries[1:]:
   entry = entries[ientry]
   # change entry.datalines
   newdataline = '{{Lbody=%s}}' % L0
   entry.datalines = [newdataline]

class Extra(object):
 def __init__(self,line):
  self.line = line
  # sample:
  # 
  # remove <pc>
  self.line = re.sub(r'<pc>(.*?)<','<',self.line)
  # remove <ln1> to end
  self.line = re.sub(r'<ln1>.*$','',self.line)
  m = re.search(r'<L>([^<]+)<k1>([^<]+)<k2>([^<]+)<type>([^<]+)<LP>([^<]+)<k1P>([^<]+)$',self.line)
  if m == None:
   print('Extra could not parse:')
   print(line)
   print(self.line)
   exit(1)
  (self.L,self.k1,self.k2,self.type,self.LP,self.k1P) = m.groups()

def init_extras(filein):
 lines = read_lines(filein) 
 recs = [Extra(line) for line in lines if line.startswith('<L>')]
 return recs

def make_extra_entry(extra,Ldict):
 # make an Entry object from an Extra object
 # get pc from parent
 lines = []
 LP = extra.LP
 entryP = Ldict[LP]
 pc = entryP.metad['pc']
 metaline = '<L>%s<pc>%s<k1>%s<k2>%s' %(extra.L,pc,extra.k1,extra.k2)
 lines.append(metaline)
 lines.append('{{Lbody=%s}}' % LP)
 lines.append('<LEND>')
 # get linenum1,2 from parent
 linenum1 = entryP.linenum1
 linenum2 = entryP.linenum2
 entry = digentry.Entry(lines,linenum1,linenum2)
 return entry
              
if __name__=="__main__":
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx)
 filein1 = sys.argv[2] # multik2a.txt
 fileout = sys.argv[3] # output with errors marked.
 entries = digentry.init(filein)
 Ldict = digentry.Entry.Ldict

 extras = init_extras(filein1)
 entriesx = [make_extra_entry(extra,Ldict) for extra in extras]
 entries1 = entries + entriesx
 # sort entries1
 entries2 = sorted(entries1,key=lambda e:float(e.metad['L']))
 write_entries(fileout,entries2)
 
