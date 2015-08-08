#!/usr/bin/python3

import sys
import os
import mimetypes
import urllib
from mdreader import mdreader
from mediabase import mediabase

def scan_file (path):
	ctime = os.stat(path).st_ctime
	basetime = mbase.getCTime(path)
	if basetime >= ctime:
		return None
	url = 'file://'+urllib.parse.quote(path)
	if path.endswith('.mpc') or path.endswith('.ape'):
		type='audio'
	else:
		(type, enc) = mimetypes.guess_type(url)
	if not type:
		return None
	if not type.startswith('audio'):
		return None
	if type.endswith('x-mpegurl'):
		return None
	data = mreader.read_metadata(url)
	if data:
		data['ctime'] = [ctime]
		data['path'] = [path]
	return data

if __name__ == '__main__':
	mreader = mdreader()
	mbase = mediabase('chirpy.sqlite')
	mimetypes.init()
	for path, dirs, files in os.walk(sys.argv[1]):
		for f in files:
			mobject = scan_file(os.path.join(path,f))
			if mobject:
				mbase.addObj(mobject)			
