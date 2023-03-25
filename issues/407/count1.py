""" count1.py
 
"""
import sys,re
import codecs
import os.path,time

def count_one(dictlo,regex):
 csl_orig = 'c:/xampp/htdocs/cologne/csl-orig/v02'
 dictfile = '%s/%s/%s.txt' % (csl_orig,dictlo,dictlo)
 #print(dictfile)
 with codecs.open(dictfile,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f]
 # print(len(lines),'lines in',dictfile)
 count = 0
 all_matches = []
 for iline,line in enumerate(lines):
  matches = re.findall(regex,line)
  count = count + len(matches)
  for match in matches:
   all_matches.append(match)
 print('%s instances of %s in %s' % (count,regex,dictlo))
 return count,all_matches
 
def get_dictlos_all():
 x =  'acc ae ap90 ben bhs bop bor bur cae ' +\
 'ccs gra gst ieg inm  krm mci md mw mw72 ' +\
 'mwe pe pgn pui  pwkvn  pw pwg sch shs skd ' +\
 'snp stc vcp vei wil  yat lan armh'
 dictlos = re.split(r' +',x)
 print(len(dictlos),"dictionary codes known")
 print(', '.join(dictlos))
 return dictlos

dictlos_all = get_dictlos_all()

def get_chartype(c):
 if c in 'fxaiueoFXAIUEO':
  mtype = 'V' # Sanskrit vowel V
 elif c in '0123456789':
  mtype = '#'
 elif re.search(r'[a-zA-Z]',c):
  mtype = 'C'
 else:
  mtype = '?'
 return mtype

def get_matchstr(matches):
 keys = []
 d = {}
 mtypes = ['C','V','#','?']
 for match in matches:
  # match is a string
  # classify match based on first character (the char before accent)
  mtype = get_chartype(match[0])
  if mtype not in keys:   
   keys.append(mtype)
   d[mtype] = 0
  d[mtype] = d[mtype] + 1
 keys1 = sorted(keys, key = lambda x: mtypes.index(x))
 arr = []
 for k in keys1:
  n = d[k]
  # a = '%s (%s)' %(k,n)
  a = '%s-%s' %(k,n)
  arr.append(a)
 ans = ', '.join(arr)
 return ans
 
def write(fileout,counts):
 outarr = []
 outarr.append('; Number of instances of %s' % regex)
 for dictlo,countmatches in counts:
  count,all_matches = countmatches
  matchstr = get_matchstr(all_matches)
  
  outarr.append('%s %s %s' %(dictlo.ljust(5),count,matchstr))
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out+'\n')
 print(len(dictlos),'counts written to',fileout)
 
if __name__=="__main__":
 option = sys.argv[1] # ALL  or a specific dictionary code
 # Problematic entering this regex on the command line
 #print(regex)
 #regex = sys.argv[2]
 #print(regex)
 # In Python, two ways to enter
 regex = "[^<][/\\\^][fxaiueoFXAIUEO]"  # this same as Emacs
 print(regex)
 #regex = r"[^<][/\\^][fxaiueoFXAIUEO]"
 fileout = sys.argv[2] # output path
 if option == 'ALL':
  dictlos = dictlos_all
 elif option in dictlos_all:
  dictlos = [option]
 else:
  print('ERROR unknown option:',option)
  exit(1)
 #dictlos = dictlos[:5]
 counts = [(dictlo,count_one(dictlo,regex)) for dictlo in dictlos]
 write(fileout,counts)

