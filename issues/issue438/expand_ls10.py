import sys
import re
def edge_cases(text):
	# <ls>Journ. of the Am. Or. S. 6,505, <is>Śl.</is> 18.</ls>
	text = re.sub(r'<ls>([^<]*)<is>Śl\.</is>', r'<ls>\1Śl.', text)
	# <ls>Journ. of the Am. Or. S. 6,502, Śl. 1.</ls>
	text = re.sub(r'<ls>([^<]*) ([0-9,]+)[,] Śl[.] ([0-9]+)[.]</ls>', r'<ls n="\1" id="\2">\1 \2, Śl. \3.</ls>', text)
	# <ls>VP. 175, N. 3.</ls>
	text = re.sub(r'<ls>VP[.] (\d+), N[.] (\d+)', r'<ls n="VP." id="\1">VP. \1, N. \2', text)
	# <ls>SCHIEFNER Lebensb. 243 (13).</ls>
	text = re.sub(r'<ls>SCHIEFNER, Lebensb[.] (\d+)([^<]*)</ls>', r'<ls n="SCHIEFNER Lebensb." id="\1">SCHIEFNER Lebensb. \1\2</ls>', text)
	# <ls>Verz. d. Oxf. H. No. 208.</ls>
	text = re.sub(r'<ls>Verz\. d\. Oxf\. H\. No\. (\d+)\.</ls>', r'<ls n="Verz. d. Oxf. H." id="\1">Verz. d. Oxf. H. No. \1.</ls>', text)
	# <ls>WILSON, SĀṂKHYAK. S. 107.</ls>
	text = re.sub(r'<ls>WILSON, SĀṂKHYAK\. S\. (\d+)\.</ls>', r'<ls n="WILSON, SĀṂKHYAK. S." id="\1">WILSON, SĀṂKHYAK. S. \1.</ls>', text)
	# <ls n="AK." id="1,1,1,48.">AK. 1,1,1,48.</ls>
	text = re.sub(r'<ls n="([^"]+)" id=([^>]+)[.]">', r'<ls n="\1" id=\2">', text)
	# <ls n="M. 6," id="38">38.</ls>
	text = re.sub(r'<ls n="([^,\d]+) ([\d,]+)," id="([\d,.]+)">', r'<ls n="\1" id="\2,\3">', text)
	return text


if __name__ == "__main__":
	filein = sys.argv[1]
	fileout = sys.argv[2]
	with open(filein, 'r') as fin:
		text = fin.read()
	text = edge_cases(text)
	with open(fileout, 'w') as fout:
		fout.write(text)
	print('Edge cases handled')

	
