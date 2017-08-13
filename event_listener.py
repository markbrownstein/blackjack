from logging import *

class EventListener:
	def __init__(self, log):
		self.log = log

	def event(self, type, data):
		self.log.finest("Event type: " + type + ", data: " + str(data))
