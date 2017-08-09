import random

class Deck:
	ranks = [ 'A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K' ]
	suits = [ 'C', 'D', 'H', 'S' ]

	def __init__(self, decks):
		self.decks = decks
		random.seed()
		self.shuffle()
		
	def get(self):
		return self.random_deck

	def get_count(self):
		return len(self.random_deck)

	def shuffle(self):
		self.random_deck = [ rank + suit for deck in range(self.decks) for rank in self.ranks for suit in self.suits ]
		random.shuffle(self.random_deck)
		
	def deal(self):
		if len(self.random_deck) == 0:
			return ""
		else:
			return self.random_deck.pop(0)
