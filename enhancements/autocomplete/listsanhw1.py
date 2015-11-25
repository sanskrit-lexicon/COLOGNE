# -*- coding: utf-8 -*-
""" afem.py

To generate words ending with 'a' and having feminine gender.
  
"""
import sys, re
import codecs
import string
import datetime

# Function to return timestamp
def timestamp():
	return datetime.datetime.now()

def listsanhw1():
	fin = codecs.open('../../../CORRECTIONS/sanhw1/sanhw1.txt','r','utf-8')
	data = fin.readlines()
	fin.close()
	fout = codecs.open('hw11.txt','w','utf-8')
	hw1 = []
	for line in data:
		line = line.strip()
		hw = line.split(':')[0]
		hw1.append(hw)
	fout.write('"')
	fout.write('\n'.join(hw1))
	fout.write('"')
	fout.close()
listsanhw1()
	