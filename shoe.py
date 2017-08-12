import random
from logging import *

class Shoe:
	RANKS = [ 'A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K' ]
	SUITS = [ 'C', 'D', 'H', 'S' ]

	def __init__(self, log, decks):
		self.log = log
		self.decks = decks
		self.random_deck = []
		self.red_card = 0
		random.seed()
		self.shuffle()
		
	def get(self):
		return self.random_deck

	def get_count(self):
		return len(self.random_deck)

	def shuffle(self):
		self.random_deck = [ rank + suit for deck in range(self.decks) for rank in self.RANKS for suit in self.SUITS ]
		random.shuffle(self.random_deck)
		if self.decks <= 2:
			self.red_card = self.decks * 13 + random.randint(-6, 6)
		else:
			self.red_card = self.decks * 13 + random.randint(-13, 13)
		#self.random_deck = [ 'A1', '91', 'A1', 'A1', 'T1', '41', 'T1', 'J1', 'T2', '92', 'T2', 'K2', '43', 'Q3', '43', 'Q3', 'K3', '44', 'T4', '44', '64', 'K4', '74', 'K4', 'K4', '95', '55', '75', 'A5', '55' ]
		#self.red_card = 0
		
	def deal(self):
		card = ""
		if len(self.random_deck) <= self.red_card:
			self.red_card = 0
		else:
			card = self.random_deck.pop(0)
		self.log.finest("Dealt card: " + card)
		return card
