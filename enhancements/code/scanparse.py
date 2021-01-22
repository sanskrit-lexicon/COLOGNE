import sys,re,codecs

class Item(object):
 def __init__(self,lines):
  self.lines = lines
  try:
   self.L,self.key,self.wordin,self.wordout = lines[0].split(':')
  except:
   print('Item Error:')
   for line in lines:
    print(line)
   exit(1)

 def get_type(self):
  for x in self.lines[1:]:
   if 'scan ' in x:
    return 'scan'
  # otherwise
  return 'other'

def generate_items(lines):
 """ assumes lines is a list of two kinds:  A and B
   A,B,B,A,BABBBAAAB etc
   We want to generate ABB,AB,ABBB,A,A,AB
   We require the first line to be an A
 """
 def linetypeF(line):
  if re.search(r'^[0-9]',line):
   return True
  else:
   return False
 items = []
 for iline,line in enumerate(lines):
  if iline == 0:
   if not linetypeF(line):
    print('generate_items ERROR 1',line)
    exit(1)
   items = [line]
  elif linetypeF(line):
   yield items
   items=[line]
  else:
   items.append(line)
 # last time
 return items

def init_items(lines):
 # assume a line followed by comments
 items = [Item(x) for x in generate_items(lines)]
 print(len(items),'items')
 return items

def write_items_scan(items,fileout):
 a = [item for item in items if item.get_type() == 'scan']
 with codecs.open(fileout,"w","utf-8") as f:
  for item in a:
   out = '%s : %s : %s : %s :' %(item.L,item.key,item.wordin,item.wordout)
   f.write(out+'\n')
 print(len(a),"records written to",fileout)

def write_items_other(items,fileout):
 a = [item for item in items if item.get_type() == 'other']
 with codecs.open(fileout,"w","utf-8") as f:
  for item in a:
   for line in item.lines:
    f.write(line+'\n')
 print(len(a),"records written to",fileout)

if __name__ == "__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 fileout1 = sys.argv[3]
 with codecs.open(filein,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f]
 items = init_items(lines)
 write_items_scan(items,fileout)
 write_items_other(items,fileout1)

