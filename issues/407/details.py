""" details.py
 
"""
import sys,re
import codecs
import os.path,time

def get_details(dictlo,regex):
 csl_orig = 'c:/xampp/htdocs/cologne/csl-orig/v02'
 dictfile = '%s/%s/%s.txt' % (csl_orig,dictlo,dictlo)
 
 with codecs.open(dictfile,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f]
 print(len(lines),'lines in',dictfile)
 count = 0
 details = []
 for iline,line in enumerate(lines):
  matches = re.findall(regex,line)
  if len(matches) == 0:
   continue
  detail = (iline+1,matches,line)
  details.append(detail)
 return details
 
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

def write(fileout,details,dictlo,regex):
 outarr = []
 outarr.append('; ------------------------------------------------------')
 outarr.append('; %s: %s instances of %s' % (dictlo,len(details),regex))
 outarr.append('; ------------------------------------------------------')
 for detail in details:
  (lnum,matches,line) = detail
  outarr.append('; ----------------')
  matchstr = ' :: '.join(matches)
  outarr.append('; %s ' % matchstr)
  lnumstr = '%s' % lnum
  lnumstr = lnumstr.ljust(7)
  outarr.append('%s: %s' %(lnumstr,line))

 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out+'\n')
 print(len(details),'instance lines written to',fileout)
 
if __name__=="__main__":
 option = sys.argv[1] # a specific dictionary code
 regex = "[^<][/\\\^][fxaiueoFXAIUEO]"  # this same as Emacs
 if option == 'ALL':
  dictlos = dictlos_all
 elif option in dictlos_all:
  dictlos = [option]
 else:
  print('details.py ERROR unknown option:',option)
  exit(1)
 for dictlo in dictlos: 
  details = get_details(dictlo,regex)
  if len(details) == 0:
   print('%s no instances' % dictlo)
  else:
   fileout = 'details/details_%s.txt' % dictlo
   write(fileout,details,dictlo,regex)

