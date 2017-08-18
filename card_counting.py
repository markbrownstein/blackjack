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
	TYPE = "type"
	HIGH = "high"
	STEP = "step"
	INCREMENTAL = "incremental"
	MULTIPLIER = "multiplier"

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
		
	def parse_range(self, s):
		n_array = []
		
		try:
			index = s.find('-')
			if index >= 0:
				first = int(s[:index])
				second = int(s[index + 1:])
				if first >= second:
					raise Exception("Range backwards")
				while first <= second:
					n_array.append(str(first))
					first = first + 1
			else:
				n_array.append(s)
		except Exception as e:
			self.log.warning("Exception caught reading card counting playing method:" + str(e))
			
		return n_array
		
	def load_card_counting_strategy(self, card_counting_strategy_section):
		# Load card counting strategy section
		self.load_section(card_counting_strategy_section)
		
		# Read counting method
		self.counting_method = None
		counting_method = Configuration.read_string(self, self.COUNTING_METHOD, "")
		self.log.info("Counting method: " + counting_method)
		if counting_method in self.config:
			self.counting_method = counting_method
		elif len(counting_method) > 0:
			self.log.warning("Error: Couldn't load counting method: " + counting_method)

		# Read betting method
		self.betting_method = None
		betting_method = Configuration.read_string(self, self.BETTING_METHOD, "")
		self.log.info("Betting method: " + betting_method)
		if betting_method in self.config:
			self.betting_method = betting_method
		elif len(betting_method) > 0:
			self.log.warning("Error: Couldn't load betting method: " + betting_method)
		
		# Read playing method
		self.playing_method = None
		self.playing_method_map = {}
		playing_method = Configuration.read_string(self, self.PLAYING_METHOD, "")
		self.log.info("Playing method: " + playing_method)
		if playing_method in self.config:
			self.playing_method = playing_method

			# Read playing method list
			for playing_method in self.config[self.playing_method]:
				try:
					s = self.config[self.playing_method][playing_method]
					s_array = s.split('_')
					
					# We need at least 3 (can be insurance_+5_yes => "insurance": ["+5", "yes"] or soft13-16_2-6+5_double => "soft13-16": [ "2-6", "+5", "double" ]
					if len(s_array) >= 3:
						# Parse the players hand (could be soft or hard)
						prefix = ""
						if s_array[0][0:4].lower() == "soft" or s_array[0][0:4].lower() == "hard":
							prefix = s_array[0][0:4].lower()
						left_over = s_array[0][len(prefix):]
						comma = False
						index = left_over.find(',')
						if index >= 0:
							first = left_over[:index]
							left_over = left_over[index + 1:]
							if first != left_over:
								raise Exception("Pairs don't match")
							comma = True
						n_array = self.parse_range(left_over)
						for n in n_array:
							if comma:
								self.playing_method_map[prefix + n + ',' + prefix + n] = s_array[1:]
							else:
								self.playing_method_map[prefix + n] = s_array[1:]
				except Exception as e:
					self.log.warning("Exception caught reading card counting playing method:" + str(e))
			#print(self.playing_method_map)
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
		if self.playing_method == None or self.playing_method_map == None or len(self.playing_method_map) == 0:
			return False
		return True
		
	def get_card_counting_strategy(self):
		return self.section
		
	def get_count(self):
		return self.count
		
	def get_true_count(self):
		return self.count / self.decks
		
	def get_used_count(self):
		count = 0.0
		if self.has_counting_method():
			if self.is_using_true_count():
				count = self.get_true_count()
			else:
				count = self.get_count()
		return count
		
	def get_counting_method(self):
		return self.counting_method
		
	def get_betting_method(self):
		return self.betting_method
		
	def get_playing_method(self):
		return self.playing_method
		
	def get_decision(self, key):
		if self.playing_method_map != None and key in self.playing_method_map:
			return self.playing_method_map[key]
		return None
		
	def is_using_true_count(self):
		if self.counting_method != None:
			return self.read_boolean(self.TRUE_COUNT, False, self.counting_method)
		return False
		
	def get_count_threshold(self):
		if self.counting_method != None:
			return self.read_double(self.COUNT_THRESHOLD, 0.0, self.counting_method)
		return 0.0
	
	def get_betting_type(self):
		if self.betting_method != None:
			return self.read_string(self.TYPE, "", self.betting_method)
		return ""
	
	def get_betting_high(self):
		if self.betting_method != None:
			return self.read_double(self.HIGH, 1.0, self.betting_method)
		return 1.0
	
	def get_betting_step(self):
		if self.betting_method != None:
			return self.read_double(self.STEP, 1.0, self.betting_method)
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
			self.log.finer("Current count=" + str(self.count) + ", current true count=" + str(self.get_true_count()))
	
	def event(self, type, data):
		EventListener.event(self, type, data)
		
		if self.counting_method != None:
			if type == "shuffle":
				self.reset_count()
			elif type == "card":
				self.do_count(data)
