import csv
from logging import *
from blackjack_rules import BlackjackRules
from blackjack_game import BlackjackGame

class BlackjackAutoGame:
	STANDARD = "standard"
	
	def __init__(self, log):
		self.log = log
		self.number_of_runs = 1
		self.number_of_hands = 10
		self.strategy_filenames = { }
		self.strategy_filenames[self.STANDARD] = "standard_strategy.csv"
		self_strategies = { }
		
	def load_strategy(self, filename):
		strategy = {}
		with open(filename, newline='') as file:
			reader = csv.reader(file, delimiter='\t')
			for row in reader:
				if row[0].isdigit() and len(row) == 11:
					key = int(row[0])
					value = []
					for i in range(10):
						if row[i + 1] == '1':
							value.append(True)
						else:
							value.append(False)
					strategy[key] = value
		return strategy
	
	def run(self):
		# Load strategies
		for strategy_name in self.strategy_filenames.keys():
			filename = self.strategy_filenames[strategy_name]
			strategy = self.load_strategy(filename)
					
		# Start games
		self.game = BlackjackGame(self.log, 1, 500)
		self.bet = 5
