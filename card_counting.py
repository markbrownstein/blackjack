from common_logging import *
from configuration import Configuration
from event_listener import EventListener

class CardCounting(Configuration, EventListener):
	# Methods
	COUNTING_METHOD = "counting_method"
	BETTING_METHOD = "betting_method"
	PLAYING_METHOD = "playing_method"
	
	# Counting method
	RANK_DICTIONARY = { "A": "ace", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine", "T": "ten", "J": "jack", "Q": "queen", "K": "king" }
	
	def __init__(self, log, decks, card_counting_strategy_section = "Blackjack"):
		# Initialize variables
		self.decks = decks
		
		# Initialize and read INI file
		Configuration.__init__(self, log, "card_counting.ini", card_counting_strategy_section)

		# Initialize event listener
		EventListener.__init__(self, log)

		# Load card counting strategy
		self.load_card_counting_strategy(card_counting_strategy_section)
		
		# Reset count
		self.reset_count()
		
	def load_card_counting_strategy(self, card_counting_strategy_section):
		# Load card counting strategy section
		self.load_section(card_counting_strategy_section)
		
		# Read counting method
		self.counting_method = None
		counting_method = Configuration.readString(self, self.COUNTING_METHOD, "")
		if counting_method in self.config:
			self.counting_method = self.config[counting_method]
		elif len(counting_method) > 0:
			self.log.warning("Error: Couldn't load counting method: " + counting_method)

		# Read betting method
		self.betting_method = None
		betting_method = Configuration.readString(self, self.BETTING_METHOD, "")
		if betting_method in self.config:
			self.betting_method = self.config[betting_method]
		elif len(betting_method) > 0:
			self.log.warning("Error: Couldn't load betting method: " + betting_method)
		
		# Read playing method
		self.playing_method = None
		playing_method = Configuration.readString(self, self.PLAYING_METHOD, "")
		if playing_method in self.config:
			self.playing_method = self.config[playing_method]
		elif len(playing_method) > 0:
			self.log.warning("Error: Couldn't load playing method: " + playing_method)
		
	def has_counting_method(self):
		if self.counting_method == None:
			return False
		return True
		
	def has_betting_method(self):
		if self.betting_method == None:
			return False
		return True
		
	def has_playing_method(self):
		if self.playing_method == None:
			return False
		return True
		
	def get_card_counting_strategy(self):
		return self.section
		
	def get_count(self):
		return self.count
		
	def get_true_count(self):
		return self.count / self.decks
		
	def get_counting_method(self):
		return self.counting_method
		
	def get_betting_method(self):
		return self.betting_method
		
	def get_playing_method(self):
		return self.playing_method
		
	def list_card_counting_strategies(self):
		list = []
		for section in self.config.sections():
			if section != "Blackjack" and self.config.has_option(section, self.COUNTING_METHOD):
				list.append(section)
		return list
		
	def reset_count(self):
		self.count = 0.0
		#self.aces_count = 0
		self.log.info("Reset count")
		
	def do_count(self, card):
		if self.counting_method != None:
			key = self.RANK_DICTIONARY[card[0]]
			if key in self.counting_method:
				try:
					self.count = self.count + float(self.counting_method[key])
				except ValueError:
					pass
			self.log.finer("Current count=" + str(self.count))
	
	def event(self, type, data):
		EventListener.event(self, type, data)
		
		if self.counting_method != None:
			if type == "shuffle":
				self.reset_count()
			elif type == "card":
				self.do_count(data)
