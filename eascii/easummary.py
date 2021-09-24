#-*- coding:utf-8 -*-
"""easummary.py
 
"""
import sys,re,codecs
import unicodedata
## https:##stackoverflow.com/questions/27092833/unicodeencodeerror-charmap-codec-cant-encode-characters
## This required by git bash to avoid error
## UnicodeEncodeError: 'charmap' codec cannot encode characters 
## when run in a git bash script.

sys.stdout.reconfigure(encoding='utf-8')
dictlos =re.split(r' +',"acc ae ap90 ben   bhs bop bor bur cae \
 ccs gra gst ieg inm  krm mci md mw mw72 \
 mwe pe pgn pui    pw pwg sch shs skd \
 snp stc vcp vei wil  yat lan armh")
print(len(dictlos),'dictionary codes')

def check_ea(lines):
 asdict = {}
 metaline = None
 page = None
 #regex_split = re.compile(r'<ls>(.*?)</ls>')
 #nls = 0
 for iline,line in enumerate(lines):
  if iline == 0: # %***This File is E:\\APTE.ALL, Last update 11.09.06 
   continue  # 
  line = line.rstrip('\r\n')
  if line == '':
   continue
  if line.startswith('<L>'):
   metaline = line
   #imetaline1 = iline+1
   #continue
  elif line == '<LEND>':
   metaline = None
   imetaline = None
   continue
  elif line.startswith('[Page'):
   page = line
   continue
  if metaline == None:
   # only examines lines within entries, including metaline
   continue
  for c in line:
   if ord(c) > 127:
    if c not in asdict:
     asdict[c] = 0
    asdict[c] = asdict[c] + 1
 
 return asdict

def write_ea_helper_version0(eacodes):
 chars = eacodes.keys()
 chars = sorted(chars)
 outarr = []
 for c in chars:
  eacode = eacodes[c]
  c_dictlos = sorted(eacode.counts.keys())
  ntot = sum(eacode.counts[dictlo] for dictlo in c_dictlos)
  a = []  # tab separated values
  a.append("%s" %c)
  a.append("\\u%04x" %ord(c))
  a.append('%d'% ntot)
  a.append(unicodedata.name(c))
  b = []
  for dictlo in c_dictlos:
   b.append('%s=%s' %(dictlo,eacode.counts[dictlo]))
  a.append(', '.join(b))
  out = '\t'.join(a)
  outarr.append(out)
 return outarr
  
def partition_idea(n,k):
 """
  n the length of some array
  return a list of lists,
  Example:  n=5, k=2
  [[0,1],[2,3],[4]]
Ref https://www.techiedelight.com/partition-list-python
 """
 def gen():
  for i in range(0, n, k):
        yield list(range(i,i+k))
 return list(gen())

def partition_list(l, n):
 # ref: https://www.techiedelight.com/partition-list-python
    for i in range(0, len(l), n):
        yield l[i:i + n]
 
def write_ea_helper(eacodes,chunksize):
 # For characters in many dictionaries, generate output over multiple lines.
 chars = eacodes.keys()
 chars = sorted(chars)
 outarr = []
 # header (first line of tsv)
 a = ['char','hex','count','char name']
 for i in range(chunksize):
  a.append('dict #')
 outarr.append('\t'.join(a))
 for c in chars:
  eacode = eacodes[c]
  c_dictlos = sorted(eacode.counts.keys())
  # n_dictlos = len(c_dictlos)
  ntot = sum(eacode.counts[dictlo] for dictlo in c_dictlos)
  carr = []
  a = []  # tab separated values
  a.append("%s" %c)
  a.append("\\u%04x" %ord(c))
  a.append('%d'% ntot)
  a.append(unicodedata.name(c))
  aheader = a
  a = [] # for subsequent lines
  a.append('')
  a.append('')
  a.append('')
  a.append('')
  arest = a
  iline = 0
  for ichunk,chunk in enumerate(partition_list(c_dictlos,chunksize)):
   # 5 dictionaries at a time
   if ichunk == 0:
    a = aheader[:]  # clone
   else:
    a = arest[:]  # clone
   b = []
   nchunk = len(chunk)
   for i in range(chunksize):
    #for dictlo in chunk:
    if i < nchunk:
     dictlo = chunk[i]
     b.append('%s %s' %(dictlo.ljust(5),eacode.counts[dictlo]))
    else:
     b.append('')
   #bstring = ' '.join(b)
   #a.append(bstring)
   #out = '\t'.join(a)
   c = a + b 
   out = '\t'.join(c)
   assert type(c) == list
   assert type(out) == str
   #print(out)
   outarr.append(out)
 nrecs = len(chars)
 return nrecs,outarr
 
def write_ea(fileout,eacodes):
 chunksize = 5
 nrec,outarr = write_ea_helper(eacodes,chunksize)
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   try:
    f.write(out+'\n')
   except:
    print('write_ea error:out=',out)
    exit(1)
 print(nrec,"records written to",fileout)

def eaone(filein):
 with codecs.open(filein,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f]
 eacounts = check_ea(lines) # dictionary [ASCII] -> count
 return eacounts

class EA(object):
 def __init__(self,c):
  # c is character
  self.c = c
  self.counts = {}  # counts[dictlo] = N

def filter_greek_version0(eacodes):
 # not as desired, since some combining characters are 0300-0332
 eacodes1 = {}
 chars = eacodes.keys()
 for c in chars:
  hex = "%04x" % ord(c)
  if hex.startswith(('03','1f')):
   # Greek and Coptic, Greek extended
   eacodes1[c] = eacodes[c]
 return eacodes1

def filter_greek(eacodes):
 # not as desired, since some combining characters are 0300-0332
 eacodes1 = {}
 chars = eacodes.keys()
 for c in chars:
  name = unicodedata.name(c)
  if name.startswith('GREEK'):
   # Greek and Coptic, Greek extended
   eacodes1[c] = eacodes[c]
 return eacodes1

def filter_arabic(eacodes):
 eacodes1 = {}
 chars = eacodes.keys()  
 for c in chars:
  name = unicodedata.name(c)
  if name.startswith('ARABIC'):
   eacodes1[c] = eacodes[c]
 return eacodes1

def filter_rest(eacodes):
 eacodes1 = {}
 chars = eacodes.keys()  
 for c in chars:
  name = unicodedata.name(c)
  if not name.startswith(('GREEK','ARABIC')):
   eacodes1[c] = eacodes[c]
 return eacodes1

def summary(eadicts):
 eacodes = {}  # key  utf-8 ascii character
 for dictlo,eacounts in eadicts:
  chars = eacounts.keys()  # ascii characters in dictlo
  for c in chars:
   if c not in eacodes:
    eacodes[c] = EA(c)
   eacodes[c].counts[dictlo] =  eacounts[c]
 return eacodes


#print( list(partition_list(list(range(0,12)),5)))
#exit(1)
if __name__=="__main__":
 csl_orig = sys.argv[1] #  relative path to dictionary digitizations
 fileout = sys.argv[2] # extended ascii
 eadicts = []
 #dictlos = dictlos[:3]
 for dictlo in dictlos:
  filein = '%s/v02/%s/%s.txt' %(csl_orig,dictlo,dictlo)
  eacounts = eaone(filein)
  print(len(eacounts),"extended ascii characters for",dictlo)
  eadicts.append((dictlo,eacounts))
 agg = summary(eadicts)
 # Greek
 agg_greek = filter_greek(agg)
 fileout_greek = "%s_greek.tsv" %fileout
 write_ea(fileout_greek,agg_greek)
 # Arabic
 agg_arabic = filter_arabic(agg)
 fileout_arabic = "%s_arabic.tsv" %fileout
 write_ea(fileout_arabic,agg_arabic)
 # The rest
 agg_rest = filter_rest(agg)
 fileout_rest = "%s.tsv" % fileout
 write_ea(fileout_rest,agg_rest)
