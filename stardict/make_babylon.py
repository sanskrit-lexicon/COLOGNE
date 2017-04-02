# This Python file uses the following encoding: utf-8
"""
Usage:
python make_babylon.py pathToDicts dictId
e.g.
python make_babylon.py ../../Cologne_localcopy md
"""
import re,codecs,sys
from lxml import etree
import transcoder
import datetime
	
# Function to return timestamp
def timestamp():
	return datetime.datetime.now()

def add_tags1(x):
	global prevsutra
	m = re.search(u'^(.*)॥([१२३४५६७८९०। /-]*)॥',x)
	sutra = m.group(1).strip()
	num = m.group(2).strip()
	current_sutra = num.split(u'।')
	print current_sutra
	if len(current_sutra) != 3:
		print current_sutra
		prevsutra = current_sutra
		exit(0)
	result = '\n\n'+num+'|'+sutra+'|'+sutra+' '+num+'|'+num+' '+sutra+'\n'+sutra+' '+num+' <BR> '
	result = result.replace(u'।','.')
	return result

	

if __name__=="__main__":
	pathToDicts = sys.argv[1]
	dictId = sys.argv[2]
	#dictList = ['acc','ae','ap','ap90','ben','bhs','bop','bor','bur','cae','ccs','gra','gst','ieg','inm','krm','mci','md','mw','mw72','mwe','pd','pe','pgn','pui','pw','pwg','sch','shs','skd','snp','stc','vcp','vei','wil','yat']

	meaningseparator = {'acc':('([ .])--','\g<1>BREAK --'), 'md':(';','BREAK'), 'ap90':('<b>[-]{2}([0-9]+)</b>','BREAK<b>\g<1></b>')}
	if dictId in meaningseparator:
		instr = meaningseparator[dictId][0]
		outstr = meaningseparator[dictId][1]
	inputfile = pathToDicts+'/'+dictId+'/'+dictId+'xml/xml/'+dictId+'.xml'
	tree = etree.parse(inputfile)
	hw = tree.xpath("/"+dictId+"/H1/h/key1")
	entry =  tree.xpath("/"+dictId+"/H1/body")
	outputfile = codecs.open('output/'+dictId+'.babylon','w','utf-8')
	counter = 0
	for x in xrange(len(hw)):
		heading1 = etree.tostring(hw[x], method='text', encoding='utf-8')
		if counter % 1000 == 0:
			print counter
		counter += 1
		#print heading1
		if dictId not in ['ae','mwe']:
			heading = transcoder.transcoder_processString(heading1,'slp1','deva')
		#text = etree.tostring(entry[x], method='text', encoding='utf-8')
		html = etree.tostring(entry[x], method='html', encoding='utf-8')
		html = re.sub('\[Page[0-9+ abc-]+\]','',html)
		html = html.replace('<lb></lb>','')
		if dictId in meaningseparator and re.search(instr,html):
			html = re.sub(instr,outstr,html)
		html = html.decode('utf-8')
		sanskrittext = re.findall('<s>([^<]*)</s>',html)
		for sans in sanskrittext:
			html = html.replace('<s>'+sans+'</s>','<s>'+transcoder.transcoder_processString(sans,'slp1','deva')+'</s>')
		if dictId in ['acc','ap90']:
			html = transcoder.transcoder_processString(html,'as','roman')
			html = html.replace(u'ç',u'ś')
			html = html.replace(u'Ç',u'Ś')
			html = html.replace(u'[Pagē-',u'[Page 1-')
			html = html.replace(u'[Pagė',u'[Page 1-')
			html = html.replace(u'C¤:',u'Comm.')
			html = html.replace(u'n1',u'ṅ')
		html = html.replace('- ','')
		html = re.sub('[<][^>]*[>]','',html)
		html = html.replace('BREAK','<BR>')
		outputfile.write(heading+'\n')
		outputfile.write(html+'\n\n')
	outputfile.close()
		