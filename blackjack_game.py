from shoe import Shoe

class BlackjackGame:
	def __init__(self, decks, bankroll):
		self.shoe = Shoe(decks)
		self.bankroll = bankroll
		self.dealer_hand = []
		self.player_hand = []
		self.dealer_bust = False
		self.player_bust = False
		self.need_to_shuffle = False
		
	def get_bankroll(self):
		return self.bankroll
	
	def get_dealer_hand(self):
		return self.dealer_hand

	def get_player_hand(self):
		return self.player_hand

	def calc_rank(self, card):
		rank = 0
		char = card[0]
		if char.isdigit():
			rank = int(char)
		elif char == 'A':
			rank = 1
		elif char == 'T' or char == 'J' or char == 'Q' or char == 'K':
			rank = 10
		return rank
	
	def calc_highest_total(self, hand):
		total = 0
		aces = 0
		for card in hand:
			rank = self.calc_rank(card)
			#print("card: " + card + ", rank: " + str(rank))
			if rank == 1:
				aces = aces + 1
			total = total + rank
		while total < 12 and aces > 0:
			total = total + 10
			aces = aces - 1
		return total

	def deal_card(self):
		card = self.shoe.deal()
		if card == "":
			self.need_to_shuffle = True
			card = self.shoe.deal()
		return card
			
	def deal_hand(self, bet):
		if self.need_to_shuffle:
			self.need_to_shuffle = False
			self.shoe.shuffle()
		self.player_bet = bet
		self.dealer_hand = []
		self.player_hand = []
		self.dealer_bust = False
		self.player_bust = False
		self.player_hand.append(self.deal_card())
		self.dealer_hand.append(self.deal_card())
		self.player_hand.append(self.deal_card())
		self.dealer_hand.append(self.deal_card())
	
	def finish_hand(self):
		if self.player_bust == True:
			 self.bankroll = self.bankroll - self.bet
		elif self.dealer_bust == True:
			 self.bankroll = self.bankroll + self.bet
