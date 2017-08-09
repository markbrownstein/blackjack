import random

class Shoe:
	RANKS = [ 'A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K' ]
	SUITS = [ 'C', 'D', 'H', 'S' ]

	def __init__(self, decks):
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
		
	def deal(self):
		if len(self.random_deck) == self.red_card:
			self.red_card = 0
			return ""
		else:
			return self.random_deck.pop(0)
