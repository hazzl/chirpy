#
# This file is part of chirpy
# (c) 2015 Felix Braun
# for licensing information see the file LICENSE
#

import sys
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

class mdreader:
	def __init__(self):
		GObject.threads_init()
		Gst.init(None)
		self._pipeline = Gst.Pipeline()
		self._metadata = {}
		self._dec = Gst.ElementFactory.make('uridecodebin', 'mdread_decoder')
		self._pipeline.add (self._dec)
		self._sink = Gst.ElementFactory.make('fakesink', 'mdread_sink')
		self._pipeline.add (self._sink)
		self._dec.connect('pad-added', self.__on_pad_added, self._sink)
	def __on_pad_added(self, dec, pad, sink):
		sinkpad = sink.get_static_pad('sink')
		if not sinkpad.is_linked():
			pad.link(sinkpad)
	def read_metadata(self, uri):
		self._dec.set_property('uri', uri)
		self._pipeline.set_state(Gst.State.PAUSED)
		end_reached = False
		self._metadata = {}
		while not end_reached:
			msg = self._pipeline.bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE,\
				Gst.MessageType.ASYNC_DONE |\
				Gst.MessageType.TAG |\
				Gst.MessageType.ERROR )
			if msg.type == Gst.MessageType.TAG:
				taglist = msg.parse_tag()
				taglist.foreach(self.__handle_tag, None)
			if msg.type == Gst.MessageType.ERROR: 
				(info, debug) = msg.parse_error()
				print ('info ', info)
				print ('debug ', debug)
				self._pipeline.set_state(Gst.State.NULL)
				end_reached = True
			if msg.type == Gst.MessageType.ASYNC_DONE:
				self._pipeline.set_state(Gst.State.NULL)
				end_reached = True
				return self._metadata
	def __store_or_append(self,tag,val):
		if tag not in self._metadata.keys():
			self._metadata[tag]=list()
		self._metadata[tag].append(val)
	def __handle_tag(self, vallist, tag, user):
		num = vallist.get_tag_size(tag)
		for i in range(num):
			val = vallist.get_value_index(tag, i)
			if tag == "extended-comment":
				etag, sep, val = val.partition('=')
				self.__store_or_append(etag,val)
			elif tag == "private-id3v2-frame":
				etag, val = self.__handle_id3v2(val)
				self.__store_or_append(etag,val)
			else:
				if isinstance(val, Gst.DateTime):
					val=val.to_iso8601_string()
				self.__store_or_append(tag,val)
	def __handle_id3v2(self, val):
		id3= {	"TIT1": "grouping",
			"TEXT":	"lyricist",
			"TDOR": "originalyear",
			"TORY": "recordingdates",
			"TLAN": "language",
			"TRSO": "radioowner",
			"TRSN": "radiostationname",
			"TOWN": "fileowner",
			"WCOP": "wwwcopyright",
			"WOAS": "wwwsource",
			"WOAF": "wwwaudiofile",
			"WOAR": "wwwartist",
			"WORS": "wwwradio",
			"WPUB": "wwwpublisher",
			"WXXX": "wwwuser",
			"TPE3": "conductor"}
		#print ("cap",val.get_caps())
		#print ("info", val.get_info())
		buf = val.get_buffer()
		#buf.foreach_meta(_handle_bufmeta, None)
		#for i in range(buf.n_memory()):
		res,info = buf.get_memory(0).map(0)
		data = info.data
		buf.get_memory(0).unmap(info)
		tag = data[:4].decode("latin_1")
		val = data[11:-1].decode("latin_1")
		return (id3[tag], val)
