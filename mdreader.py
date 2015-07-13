#
# This file is part of chirpy
# (c) 2015 Felix Braun
# for licensing information see the file LICENSE
#

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

class mdreader:
	def __init__(self):
		GObject.threads_init()
		Gst.init(None)
		self._pipeline = Gst.Pipeline()
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
		metadata={}
		while not end_reached:
			msg = self._pipeline.bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE,\
				Gst.MessageType.ASYNC_DONE |\
				Gst.MessageType.TAG |\
				Gst.MessageType.ERROR )
			if msg.type == Gst.MessageType.TAG:
				taglist = msg.parse_tag()
				taglist.foreach(self.__handle_tag, metadata)
			if msg.type == Gst.MessageType.ERROR: 
				(info, debug) = msg.parse_error()
				print ('info ', info)
				print ('debug ', debug)
				self._pipeline.set_state(Gst.State.NULL)
				end_reached = True
			if msg.type == Gst.MessageType.ASYNC_DONE:
				self._pipeline.set_state(Gst.State.NULL)
				end_reached = True
				return metadata
	def __handle_tag(self, vallist, tag, metadata):
		metadata[tag]=[]
		num = vallist.get_tag_size(tag)
		for i in range(0, num):
			val = vallist.get_value_index(tag, i)
			if isinstance(val, Gst.DateTime):
				val=val.to_iso8601_string()
			metadata[tag].append(val)
