#!/usr/bin/python3

import sys
import os
from mdreader import mdreader
from mediabase import mediabase

def scan_file (path):
	data = mreader.read_metadata('file://'+path)
	if data:
		data['mtime'] = os.stat(path).st_mtime
		data['path'] = path
	return data

if __name__ == '__main__':
	mreader = mdreader()
	mbase = mediabase('chirpy.sqlite')
	for path, dirs, files in os.walk(sys.argv[1]):
		for f in files:
			mobject = scan_file(path+'/'+f)
			if mobject:
#				for key in mobject.keys():
#					print (key, '=>', mobject[key])
				mbase.addObj(mobject)
			
