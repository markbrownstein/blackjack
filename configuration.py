from configparser import ConfigParser
from logging import *
from sys import exit

class Configuration:
	def __init__(self, log, filename, section = "DEFAULT"):
		# Initialize and read INI file
		self.log = log
		self.section = section
		self.config = ConfigParser()
		self.config.read(filename)
		self.log.finest(self.config.sections())
		if section != "DEFAULT" and not section in self.config.sections():
			self.log.severe("Can't find configuration file: " + filename + " and/or section: " + section)
			exit()

	def readString(self, key, default):
		value = default
		if key in self.config[self.section]:
			value = self.config[self.section][key]
		return value

	def readInt(self, key, default):
		value = default
		if key in self.config[self.section]:
			str_value = self.config[self.section][key]
			if str_value.isdigit():
				value = int(str_value)
		return value

	def readDouble(self, key, default):
		value = default
		if key in self.config[self.section]:
			str_value = self.config[self.section][key]
			try:
 				value = float(str_value)
			except ValueError:
				pass
		return value

	def readBoolean(self, key, default):
		value = default
		if key in self.config[self.section]:
			str_value = self.config[self.section][key].lower()
			if str_value == "yes" or str_value == "true":
				value = True
			elif str_value == "no" or str_value == "false":
				value = False
		return value

