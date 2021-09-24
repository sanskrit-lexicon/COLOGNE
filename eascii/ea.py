#-*- coding:utf-8 -*-
"""check_ea.py for ap57,ap90
 
"""
import sys,re,codecs
import unicodedata
## https:##stackoverflow.com/questions/27092833/unicodeencodeerror-charmap-codec-cant-encode-characters
## This required by git bash to avoid error
## UnicodeEncodeError: 'charmap' codec cannot encode characters 
## when run in a git bash script.

sys.stdout.reconfigure(encoding='utf-8') 
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

def write_ea(fileout,eadict):
 keys = eadict.keys()
 keys = sorted(keys)
 
 with codecs.open(fileout,"w","utf-8") as f:
   for key in keys:
    out = "%s  (\\u%04x) %5d := %s" %(key,ord(key),eadict[key],unicodedata.name(key))
    f.write(out+'\n')
 print(len(keys),"extended ascii counts written to",fileout)

if __name__=="__main__":
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx)
 fileout = sys.argv[2] # extended ascii
 
 with codecs.open(filein,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f]
 eacounts = check_ea(lines) # 
 write_ea(fileout,eacounts)
 
