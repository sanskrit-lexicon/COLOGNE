""" details1.py
 
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

def get_chartype(c):
 # compatible with count1.py
 if c in 'fxaiueoFXAIUEO':
  mtype = 'V' # Sanskrit vowel V
 elif c in '0123456789':
  mtype = '#'
 elif re.search(r'[a-zA-Z]',c):
  mtype = 'C'
 else:
  mtype = '?'
 return mtype

def select_details(details,mtype):
 ans = []  # selected details
 for detail in details:
  (lnum,matches,line) = detail
  keep = False
  for match in matches:
   # match is a string
   # classify match based on first character (the char before accent)
   match_type = get_chartype(match[0])
   if match_type == mtype:
    keep = True
    break
  if keep:
   ans.append(detail)
 return ans

def write(fileout,details,dictlo,regex):
 outarr = []
 outarr.append('; ------------------------------------------------------')
 outarr.append('; %s: %s instances of %s' % (dictlo,len(details),regex))
 outarr.append('; ------------------------------------------------------')
 mtypes = ['C','V','#','?']
 mtype_names = ['Consonant','Vowel','Number','Other']
 for imtype,mtype in enumerate(mtypes):
  mtype_details = select_details(details,mtype)
  if mtype_details == []:
   continue
  outarr.append('; ......................................................')
  outarr.append('; %s instances with character before accent of type %s' % (len(mtype_details),mtype_names[imtype]))
  for detail in mtype_details:
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
   fileout = 'details1/details1_%s.txt' % dictlo
   write(fileout,details,dictlo,regex)

