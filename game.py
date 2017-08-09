from deck import Deck

class Game:
	def __init__(self, decks, bankroll):
		self.deck = Deck(decks)
		self.bankroll = bankroll
		self.dealer_hand = []
		self.player_hand = []
		
	def deal_card(self):
		card = self.deck.deal()
		while card == "":
			self.deck.shuffle()
			card = self.deck.deal()
		return card
			
	def deal_hand(self, bet):
		self.player_bet = bet
		self.player_bust = False
		self.dealer_hand = []
		self.player_hand = []
		self.player_hand.append(self.deal_card())
		self.dealer_hand.append(self.deal_card())
		self.player_hand.append(self.deal_card())
		self.dealer_hand.append(self.deal_card())
	
	def finish_hand(self):
		if self.player_bust == True:
			 self.bankroll = self.bankroll - self.bet

	def get_dealer_hand(self):
		return self.dealer_hand

	def get_player_hand(self):
		return self.player_hand
