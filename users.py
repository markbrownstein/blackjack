from common_logging import *
from configuration import Configuration

class Users(Configuration):
	FILENAME = "users.ini"
	
	PASSWORD = "password"
	BANKROLL = "bankroll"
	STARTING_BET = "starting_bet"
	ADVISE = "advise"
	ADJUSTMENT = "adjustment"
	CARD_COUNTING_STRATEGY = "card_counting_strategy"
	
	def __init__(self, log):
		# Initialize and read INI file
		Configuration.__init__(self, log, self.FILENAME)

	def get_bankroll(self):
		return self.read_double(self.BANKROLL, 500)

	def get_starting_bet(self):
		return self.read_int(self.STARTING_BET, 1)

	def get_advise(self):
		return self.read_boolean(self.ADVISE, False)

	def get_adjustment(self):
		return self.read_string(self.ADJUSTMENT, "Multiplier")

	def get_card_counting_strategy(self):
		return self.read_string(self.CARD_COUNTING_STRATEGY, False)

	def login(self, user, password):
		success = False
		if user in self.config and self.config[user][self.PASSWORD] == password:
			success = True
			self.load_section(user)
		return success

	def has_user(self, user):
		has = False
		if user in self.config:
			has = True
		return has

	def save(self, user, bankroll, starting_bet, advise, adjustment, card_counting_strategy):
		if not user in self.config:
			self.config[user] = {}

		# Save data to memory
		self.config[user][self.BANKROLL] = str(bankroll)
		self.config[user][self.STARTING_BET] = str(starting_bet)
		self.config[user][self.ADVISE] = str(advise)
		self.config[user][self.ADJUSTMENT] = str(adjustment)
		self.config[user][self.CARD_COUNTING_STRATEGY] = str(card_counting_strategy)

		# Save data to file
		with open(self.FILENAME, 'w') as configfile:
			self.config.write(configfile)

	def save_new_user(self, user, password, bankroll, starting_bet, advise, adjustment, card_counting_strategy):
		if not user in self.config:
			self.config[user] = {}
		self.config[user][self.PASSWORD] = password
		self.save(user, bankroll, starting_bet, advise, adjustment, card_counting_strategy)
	