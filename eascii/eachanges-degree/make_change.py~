#-*- coding:utf-8 -*-
"""change_hyphen_ls.py for Benfey abbreviations
 
"""
import sys,re,codecs
## https:##stackoverflow.com/questions/27092833/unicodeencodeerror-charmap-codec-cant-encode-characters
## This required by git bash to avoid error
## UnicodeEncodeError: 'charmap' codec cannot encode characters 
## when run in a git bash script.

sys.stdout.reconfigure(encoding='utf-8') 
class Change(object):
 def __init__(self,metaline,page,iline,old,new,reason,iline1,line1,new1):
  self.metaline = metaline
  self.page = page
  self.iline = iline
  self.old = old
  self.new = new
  self.reason = reason
  self.iline1 = iline1
  self.line1 = line1
  self.new1 = new1
def change1(line):
 reason = 'marked'
 if '</ls>' not in line:
  return reason,line
 newline = re.sub(r'</ls>(-[0-9]+)',r'\1</ls>',line)
 newline = re.sub(r'</ls>-(-[0-9]+)',r'\1</ls>',newline)
 return reason,newline

def old_init_changes(lines,tooltips0):
 known_abbrevs = ['P.']
 tooltips1 = [tip for tip in tooltips0 if tip.abbrev in known_abbrevs]
 tooltips = sorted(tooltips1,key = lambda tip: len(tip.abbrev),reverse=True)
 for tip in tooltips[0:10]:print(tip.abbrev)
 
 changes = [] # array of Change objects
 metaline = None
 imetaline1 = None
 page = None
 regex_split = re.compile(r'({#.*?#})|(<ls>.*?</ls>)')
 regex_replacenew = r'<ls>\1</ls>' # re.compile(r'<ls>\1<ls>')
 # regex for Panini (P.)
 regex_replaceold_P = re.compile(r'(P[.] +[IV]+[.] +[0-9]+[.] +[0-9]+[.]?)')
 #regex_replaceold_P = re.compile(r'(P[.] +[IV]+[.] +[0-9]+[.] +[0-9]+[.]? [0-9VI .;?]+)')
 for iline,line in enumerate(lines):
  #if iline == 260: print('dbgstart:',line)
  if iline == 0: # %***This File is E:\\APTE.ALL, Last update 11.09.06 
   continue  # 
  line = line.rstrip('\r\n')
  if line == '':
   continue
  if line.startswith('<L>'):
   metaline = line
   imetaline1 = iline+1
   continue
  if line == '<LEND>':
   metaline = None
   imetaline = None
   continue
  if line.startswith('[Page'):
   page = line
   continue
  #if imetaline1 == iline:
  #assert '¦' in line  # check
  #continue
  if line.startswith('[Page'):
   continue
  if '.' not in line:
   # all tooltip abbreviations contain a period.
   continue
  #newline = line.rstrip()  # remove trailing spaces
  #if iline == 260: print('dbg:oldline:',line)
  newline = line
  found = False
  for tip in tooltips:
   ab = tip.abbrev
   parts = re.split(regex_split,newline)
   newparts = []
   if ab != 'P.':
    continue
   else:
    regex_replaceold = regex_replaceold_P
   for part in parts:
    newpart = part
    if part == None:
     newpart = ''
    elif part.startswith('{#'):
     pass
    elif part.startswith('<ls>'):
     pass
    elif ab not in part:
     pass
    else:  
     newpart = re.sub(regex_replaceold,regex_replacenew,part)
    newparts.append(newpart)
   newline = ''.join(newparts) # end of tooltips loop
  #if iline == 260: print('dbg:newline=',line)
  if newline == line:
   continue
  # generate a change
  iline1 = None
  line1 = None
  newline1 = None
  reason = ''
  change = Change(metaline,page,iline,line,newline,reason,iline1,line1,newline1)

  changes.append(change)
 print(len(changes),'potential changes found')
 return changes

def change_out(change,ichange):
 outarr = []
 case = ichange + 1
 #outarr.append('; TODO Case %s: (reason = %s)' % (case,change.reason))
 try:
  ident = '%s  (reason = %s)' %(change.metaline,change.reason)
 except:
  print('ERROR:',change.iline,change.old)
  exit(1)
 if ident == None:
  ident = change.page
 outarr.append('; ' + ident)
 # change for iline
 lnum = change.iline + 1
 line = change.old
 new = change.new
 outarr.append('%s old %s' % (lnum,line))
 outarr.append('%s new %s' % (lnum,new))
 outarr.append(';')
 #change for iline1
 if True:
  lnum = change.iline1 + 1
  line = change.line1
  new = change.new1
  outarr.append('%s old %s' % (lnum,line))
  outarr.append('%s new %s' % (lnum,new))
  outarr.append(';')

 # dummy next line
 return outarr

def write_changes(fileout,changes):
 with codecs.open(fileout,"w","utf-8") as f:
   for ichange,change in enumerate(changes):
    outarr = change_out(change,ichange)
    for out in outarr:
     f.write(out+'\n')
 print(len(changes),"possible changes written to",fileout)

def write_changes_hyphen(fileout,changes):
 # aggregate via reason
 aggs = {}
 for change in changes:
  reason = change.reason
  if reason not in aggs:
   aggs[reason] = []
  aggs[reason].append(change)
 
 with codecs.open(fileout,"w","utf-8") as f:
  reasons = aggs.keys()
  nchanges = 0
  for reason in reasons:
   changes1 = aggs[reason]
   f.write('; --------------------------------------------------------------\n')
   f.write(';  hyphen = %s, %s instances\n' %(reason,len(changes1)))
   f.write('; --------------------------------------------------------------\n')
   for ichange,change in enumerate(changes1):
    outarr = change_out(change,ichange)
    for out in outarr:
     f.write(out+'\n')
   nchanges = nchanges + len(changes1)
 print(nchanges,"possible changes written to",fileout)

class Tooltip(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  parts = re.split(r' += ',line)
  if len(parts) != 2:
   print('problem parsing tooltip')
   print(line)
   print(parts)
   exit(1)
  self.abbrev,self.tip = parts
  self.nabbrev = 0
  
def init_tooltip(filein):
 with codecs.open(filein,"r","utf-8") as f:
  ans = [Tooltip(x) for x in f]
 print(len(ans),'tooltips from',filein)
 return ans

def init_changes(lines,hyphens):
 changes = [] # array of Change objects
 metaline = None
 nabbrev = 0  # number of abbreviations marked
 for iline,line in enumerate(lines):
  if line.startswith('<L>'):
   metaline = line
   continue
  if line.startswith('<LEND>'):
   metaline = None
   continue
  if line.startswith('<H>ADDENDA'):
   # ADDENDA AND CORRIGENDA
   metaline = 'ADDENDA'
   continue
  if line.startswith('[Page'):
   page = line
   continue
  if metaline == None:
   continue
  found = False
  for hyphen in hyphens:
   if line.endswith(hyphen):
    found = True
    break
  if not found:
   continue
  # generate a Change instance
  # remove hyphen phrase in line
  newline = re.sub(r' *%s$'%hyphen,'',line)  
  # insert the hyphen in next line
  iline1 = iline + 1
  line1 = lines[iline1]
  #print('hyphen=',hyphen)
  h = hyphen[0:-1]
  old = '<div n="lb">'
  new = '%s%s' %(old,h)
  #print(old,new)
  newline1 = line1.replace(old,new)
  if newline1 == line1:
   # unexpected next line
   # add note to metaline
   metaline = metaline + '  PROBLEM'
  reason = hyphen
  change = Change(metaline,page,iline,line,newline,reason,iline1,line1,newline1)  
  changes.append(change)
 return changes

def init_hyphens():
 text = """Bhā- Rā- Śṛṅ- Mā- Mṛ- Kumā- Bṛ- Kā- Mahā-"""
 return text.split(' ')
  
if __name__=="__main__":
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx)
 fileout = sys.argv[2] # possible change transactions
 hyphens = init_hyphens()
 with codecs.open(filein,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f]
 # lines = lines  # for later comparison
 changes = init_changes(lines,hyphens)
 write_changes_hyphen(fileout,changes)
