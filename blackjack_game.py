from common_logging import *
from blackjack_constants import *
from shoe import Shoe
from blackjack_rules import BlackjackRules
from event_listener import EventListener

class BlackjackGame:
	HAND_KEY = "hand"
	BUST_KEY = "bust"
	DONE_KEY = "done"
	NUMBER_KEY = "number"
	BET_KEY = "bet"
	SURRENDER_KEY = "surrender"

	def __init__(self, log, bankroll, rules_section = "Blackjack"):
		# Logger
		self.log = log
		
		# Required objects
		self.rules = BlackjackRules(log, rules_section)
		self.shoe = Shoe(log, self.rules.get_decks())
		self.event_listener = EventListener(log)

		# Variables
		self.bankroll = bankroll
		self.original_bet = 0
		self.need_to_shuffle = False
		self.split_hand_number = 1
		self.insurance = 0

		# Dealer hand related variables
		self.dealer_hand = []
		self.dealer_bust = False

		# Player hand related variables
		self.player_hand = self.new_player_hand()
		self.split_hands = []

	def get_rules(self):
		return self.rules

	def get_bankroll(self):
		return self.bankroll

	def get_dealer_hand(self):
		return self.dealer_hand

	def get_player_hand(self):
		return self.player_hand[self.HAND_KEY]

	def get_player_hand_number(self):
		return self.player_hand[self.NUMBER_KEY]

	def set_event_listener(self, event_listener):
		self.event_listener = event_listener

	def can_double_down(self, hand, bet):
		can = False
		if len(hand) == 2 and self.calc_total_bets() + bet <= self.bankroll:
			if self.rules.can_double_down_on_all() == True:
				can = True
			else:
				total = self.calc_highest_total(hand)
				if total >= 9 and total <= 11:
					can = True
		return can

	def can_split(self, hand, bet):
		can = False
		if len(hand) == 2 and hand[0][0] == hand[1][0] and self.calc_total_bets() + bet <= self.bankroll:
			can = True
		return can

	def can_surrender(self):
		can = False
		if self.rules.is_surrender_allowed() and len(self.player_hand[self.HAND_KEY]) == 2 and len(self.split_hands) == 0:
			can = True
		return can

	def can_buy_insurance(self):
		can = False
		if self.rules.is_insurance_allowed() and self.calc_rank(self.dealer_hand[1]) == 1 and self.calc_total_bets() < self.bankroll:
			can = True
		return can

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
			#self.log.finest("card: " + card + ", rank: " + str(rank))
			if rank == 1:
				aces = aces + 1
			total = total + rank
		while total <= 11 and aces > 0:
			total = total + 10
			aces = aces - 1
		return total

	def calc_lowest_total(self, hand):
		total = 0
		for card in hand:
			rank = self.calc_rank(card)
			total = total + rank
		return total

	def calc_total_bets(self):
		total = self.player_hand[self.BET_KEY]
		for hand in self.split_hands:
			total = total + hand[self.BET_KEY]
		return total

	def is_blackjack(self, hand):
		blackjack = False
		if self.calc_highest_total(hand) == 21 and len(hand) == 2:
			blackjack = True
		return blackjack

	def has_splits(self):
		if len(self.split_hands) > 0:
			return True
		return False

	def new_player_hand(self):
		new_hand = { self.HAND_KEY: [], self.BUST_KEY: False, self.DONE_KEY: False, self.BET_KEY: self.original_bet, self.NUMBER_KEY: self.split_hand_number, self.SURRENDER_KEY: False }
		self.split_hand_number = self.split_hand_number + 1
		return new_hand
		
	def double_bet(self):
		self.player_hand[self.BET_KEY] = self.player_hand[self.BET_KEY] * 2
		self.player_hand[self.DONE_KEY] = True
		
	def surrender_hand(self):
		self.player_hand[self.SURRENDER_KEY] = True
		self.player_hand[self.DONE_KEY] = True
	
	def buy_insurance(self, insurance):
		if insurance >= 0 and insurance <= self.original_bet / 2 and self.calc_total_bets() + insurance <= self.bankroll:
			self.insurance = insurance
			return True
		return False
		
	def make_dealer_hole_card_visible(self):
		self.event_listener.event("card", self.dealer_hand[0])

	def deal_card(self, visible = True):
		card = self.shoe.deal()
		if card == "":
			self.need_to_shuffle = True
			card = self.shoe.deal()
			if card == "":
				self.log.warning("Shoe empty! Shuffling when not supposed to!")
				self.shoe.shuffle()
				self.event_listener.event("shuffle", "")
				card = self.shoe.deal()
		if visible == True:
			self.event_listener.event("card", card)
		return card

	def deal_card_to_dealer(self):
		self.dealer_hand.append(self.deal_card())
		if self.calc_highest_total(self.dealer_hand) > 21:
			self.dealer_bust = True

	def deal_card_to_player(self):
		self.player_hand[self.HAND_KEY].append(self.deal_card())
		if self.calc_highest_total(self.player_hand[self.HAND_KEY]) > 21:
			self.player_hand[self.BUST_KEY] = True

	def deal_hand(self, bet):
		# Save original bet
		self.original_bet = bet
		
		# Shuffle if need be
		if self.need_to_shuffle:
			self.need_to_shuffle = False
			self.shoe.shuffle()
			self.event_listener.event("shuffle", "")
			
		# Setup hands
		self.dealer_hand = []
		self.dealer_bust = False
		self.split_hands = []
		self.split_hand_number = 1
		self.player_hand = self.new_player_hand()
		self.insurance = 0
		
		# Deal hands
		self.player_hand[self.HAND_KEY].append(self.deal_card())
		self.dealer_hand.append(self.deal_card(False))
		self.player_hand[self.HAND_KEY].append(self.deal_card())
		self.dealer_hand.append(self.deal_card())
	
	def split_hand(self):
		self.log.finer("Before split: " + str(self.player_hand[self.HAND_KEY]))
		new_hand = self.new_player_hand()
		card = self.player_hand[self.HAND_KEY].pop()
		new_hand[self.HAND_KEY].append(card)
		self.player_hand[self.HAND_KEY].append(self.deal_card())
		new_hand[self.HAND_KEY].append(self.deal_card())
		self.split_hands.append(new_hand)
		self.log.finer("After split: " + str(self.player_hand[self.HAND_KEY]) + str(new_hand[self.HAND_KEY]))

	def next_hand(self):
		next = False;
		self.player_hand[self.DONE_KEY] = True
		for i in range(len(self.split_hands)):
			#print(self.split_hands[i])
			if self.split_hands[i][self.DONE_KEY] == False:
				next = True
				
				# Append current hand at the end of the split list
				self.split_hands.append(self.player_hand)
				
				# Pop the next not done hand and make it the current hand
				self.player_hand = self.split_hands.pop(i)
				
				break;
		return next

	def is_player_hand_over(self):
		done = self.player_hand[self.DONE_KEY]
		if done == False:
			if self.player_hand[self.BUST_KEY] == True:
				done = True
			elif self.is_blackjack(self.player_hand[self.HAND_KEY]) == True:
				done = True
			self.player_hand[self.DONE_KEY] = done
		return done

	def is_dealer_hand_over(self):
		if self.is_blackjack(self.dealer_hand) == True:
			return True
		dealer_total = self.calc_highest_total(self.dealer_hand)
		if dealer_total > 17:
			return True
		if dealer_total == 17 and self.rules.does_dealer_hits_on_soft_17() == False:
			return True
		return False

	def finish_hand(self):
		result = []
		
		# Handle insurance bet
		dealer_blackjack = self.is_blackjack(self.dealer_hand)
		if self.insurance > 0:
			if dealer_blackjack:
				self.bankroll = self.bankroll + self.insurance * 2
			else:
				self.bankroll = self.bankroll - self.insurance

		# Go through hands
		while True:
			if self.player_hand[self.SURRENDER_KEY] == True:
				# Surrender, bet should be halved
				player_won = SURRENDER_RESULT
				self.bankroll = self.bankroll - self.player_hand[self.BET_KEY] / 2
			else:
				player_won = PUSH_RESULT
				dealer_total = self.calc_highest_total(self.dealer_hand)
				player_total = self.calc_highest_total(self.player_hand[self.HAND_KEY])

				# First, test for blackjacks
				player_blackjack = self.is_blackjack(self.player_hand[self.HAND_KEY])
				if player_blackjack == True:
					# Player blackjack! If dealer has blackjack too, push
					if dealer_blackjack == False:
						# No dealer black jack, pay out for blackjack
						self.bankroll = self.bankroll + self.player_hand[self.BET_KEY] * self.rules.get_blackjack_payout()
						player_won = BLACKJACK_RESULT
				else:
					# Next, test for dealer blackjack
					if dealer_blackjack == True:
						player_won = LOSS_RESULT
					# Now, test for busts
					elif self.player_hand[self.BUST_KEY] == True:
						player_won = LOSS_RESULT
					elif self.dealer_bust == True:
						player_won = WIN_RESULT
					else:
						# Now, compare hands
						if dealer_total == player_total:
							if self.rules.does_push_goes_to_dealer() == True:
					 			player_won = LOSS_RESULT
						elif dealer_total > player_total:
				 			player_won = LOSS_RESULT
						else:
				 			player_won = WIN_RESULT

					# Payout
					if player_won == WIN_RESULT:
						self.bankroll = self.bankroll + self.player_hand[self.BET_KEY]
					elif player_won == LOSS_RESULT:
						self.bankroll = self.bankroll - self.player_hand[self.BET_KEY]
			result.append(player_won)
			
			if len(self.split_hands) > 0:
				# Pop the next hand and make it the current hand
				self.player_hand = self.split_hands.pop(0)
			else:
				break;
		return result
