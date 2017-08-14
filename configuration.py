from configparser import ConfigParser
from sys import exit

from common_logging import *

class Configuration:
	def __init__(self, log, filename, section = "DEFAULT"):
		# Initialize and read INI file
		self.log = log

		# Load and read config file
		self.config = ConfigParser()
		self.config.read(filename)
		
		# Load section
		self.load_section(section)

	def load_section(self, section):
		self.section = section
		#self.log.finest("INI file sections " + str(self.config.sections()))
		if not section in self.config:
			self.log.severe("Error: Can't find configuration file: " + filename + " and/or section: " + section)
			exit()

	def get_section(self):
		return self.section

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

