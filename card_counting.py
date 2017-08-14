from common_logging import *
from configuration import Configuration
from event_listener import EventListener

class CardCounting(Configuration, EventListener):
	# Methods
	COUNTING_METHOD = "counting_method"
	BETTING_METHOD = "betting_method"
	PLAYING_METHOD = "playing_method"
	
	# Counting method
	TRUE_COUNT = "true_count"
	COUNT_THRESHOLD = "count_threshold"
	RANK_DICTIONARY = { "A": "ace", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine", "T": "ten", "J": "jack", "Q": "queen", "K": "king" }
	
	# Betting method
	HIGH = "high"
	STEP = "step"

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
		counting_method = Configuration.read_string(self, self.COUNTING_METHOD, "")
		if counting_method in self.config:
			self.counting_method = counting_method
		elif len(counting_method) > 0:
			self.log.warning("Error: Couldn't load counting method: " + counting_method)

		# Read betting method
		self.betting_method = None
		betting_method = Configuration.read_string(self, self.BETTING_METHOD, "")
		if betting_method in self.config:
			self.betting_method = betting_method
		elif len(betting_method) > 0:
			self.log.warning("Error: Couldn't load betting method: " + betting_method)
		
		# Read playing method
		self.playing_method = None
		playing_method = Configuration.read_string(self, self.PLAYING_METHOD, "")
		if playing_method in self.config:
			self.playing_method = playing_method
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
		
	def is_using_true_count(self):
		if self.counting_method != None:
			return self.read_boolean(self.TRUE_COUNT, False, self.counting_method)
		return False
		
	def get_count_threshold(self):
		if self.betting_method != None:
			return self.read_double(self.COUNT_THRESHOLD, 0.0, self.counting_method)
		return 0.0
	
	def get_betting_high(self):
		if self.betting_method != None:
			return self.read_double(self.HIGH, 1.0, self.betting_method)
		return 1.0
	
	def get_betting_step(self):
		if self.betting_method != None:
			return self.read_double(self.HIGH, 1.0, self.betting_method)
		return 0.0
		
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
			self.count = self.count + self.read_double(key, 0.0, self.counting_method)
			self.log.finer("Current count=" + str(self.count))
	
	def event(self, type, data):
		EventListener.event(self, type, data)
		
		if self.counting_method != None:
			if type == "shuffle":
				self.reset_count()
			elif type == "card":
				self.do_count(data)
