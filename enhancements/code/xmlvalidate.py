"""xmlvalidate.py
   Use additional lxml module to validate an xml file against an
   external DTD file.
   Usage:
   python xmlvalidate.py <xmlfilename> <dtdfilename>
"""
from lxml import etree
import sys

def validate(xmlfile,dtdfile):
 dtd = etree.DTD(dtdfile)
 tree = etree.parse(xmlfile)
 root = tree.getroot()
 status = dtd.validate(root)  # status is a Boolean
 if status:
  print("ok")
 else:
  errmsg=dtd.error_log.filter_from_errors()[0]
  print("Problem validating")
  print(errmsg)

if __name__ == "__main__":
 if len(sys.argv) != 3:
  print("Usage: python3 xmlvalidate.py <xmlfilename> <dtdfilename>")
  exit(1)
 xmlfile = sys.argv[1]
 dtdfile = sys.argv[2]
 validate(xmlfile,dtdfile)
