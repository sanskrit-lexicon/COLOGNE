""" count.py
 
"""
import sys,re
import codecs
import os.path,time

def unused_gather(filein):
 d = {}
 regex = re.compile(r'<(.*?)>')
 with codecs.open(filein,"r","utf-8") as f:
  metaline = None
  for line in f:
   line = line.rstrip('\r\n')
   if line.startswith('<L>'):
    metaline = True
    continue
   if line.startswith('<LEND>'):
    metaline = False
    continue
   if not metaline:
    continue
   for m in re.finditer(regex,line):
    e = m.group(1)
    tag = re.sub(r' .*$','',e)  # remove attributes, if any
    # exclude closing tags
    if tag.startswith('/'):
     continue
    if tag not in d:
     d[tag] = 0
    d[tag] = d[tag] + 1
 return d
 print("%s lines written to %s" %(n,fileout))

def count_one(dictlo,regex):
 csl_orig = 'c:/xampp/htdocs/cologne/csl-orig/v02'
 dictfile = '%s/%s/%s.txt' % (csl_orig,dictlo,dictlo)
 #print(dictfile)
 with codecs.open(dictfile,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f]
 print(len(lines),'lines in',dictfile)
 count = 0
 for iline,line in enumerate(lines):
  matches = re.findall(regex,line)
  count = count + len(matches)
 print('%s instances of %s in %s' % (count,regex,dictlo))
 return count
 
def get_dictlos_all():
 x =  'acc ae ap90 ben bhs bop bor bur cae ' +\
 'ccs gra gst ieg inm  krm mci md mw mw72 ' +\
 'mwe pe pgn pui    pw pwg sch shs skd ' +\
 'snp stc vcp vei wil  yat lan armh'
 dictlos = re.split(r' +',x)
 print(len(dictlos),"dictionary codes known")
 print(', '.join(dictlos))
 return dictlos

dictlos_all = get_dictlos_all()


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
 outarr = []
 outarr.append('; Number of instances of %s' % regex)
 for dictlo,count in counts:
  outarr.append('%s %s' %(dictlo.ljust(5),count))
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out+'\n')
 print(len(dictlos),'counts written to',fileout)

