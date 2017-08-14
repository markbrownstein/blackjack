from common_logging import *
from command_line_ui import CommandLineUI
from card_counting import CardCounting
from users import Users
from blackjack_game_framework import BlackjackGameFramework

class BlackjackCommandLineUIGame(BlackjackGameFramework):
	NONE = "None"
	
	def __init__(self, log, rules_section = "Blackjack"):
		# Initialize log
		self.log = log

		# Initialize UI
		self.ui = CommandLineUI(self.log)

		# Load user
		bankroll = 500
		starting_bet = 5
		card_counting_strategy = self.NONE
		self.advise = False
		self.user = ""
		self.users = False
		self.strategy = False
		#self.card_counting_strategy = None
		while True:
			response = self.ui.prompt(["guest", "login", "new user"], "Play as ")
			if response == 'g':
				break
			if response == 'l' or response == 'n':
				self.users = Users(self.log)
				if response == 'l':
					user = self.ui.string_prompt("user name")
					password = self.ui.string_prompt("password", True)
					if self.users.login(user, password):
						self.user = user
						bankroll = self.users.get_bankroll()
						starting_bet = self.users.get_starting_bet()
						self.advise = self.users.get_advise()
						card_counting_strategy = self.users.get_card_counting_strategy()
						break
					else:
						print("Error: Login failed!")
				elif response == 'n':
					while True:
						user = self.ui.string_prompt("new user name")
						password = self.ui.string_prompt("password")
						if self.users.has_user(user):
							print("Error: User " + user + " already exists!")
						else:
							self.user = user
							self.users.save_new_user(user, password, bankroll, starting_bet, self.advise)
							break
					break

		# Initialize framework
		BlackjackGameFramework.__init__(self, self.log, bankroll, starting_bet, rules_section)

		# Load card counting strategy
		if card_counting_strategy != self.NONE:
			self.load_card_counting_strategy(card_counting_strategy)

	def show_hand(self, dealer_hand, show_all_cards = False):
		if dealer_hand == True:
			hand = list(self.get_dealer_hand())
			if show_all_cards == False:
				hand[0] = '??'		
			text = "Dealer";
		else:
			hand = self.get_player_hand()
			text = "Player";
		highest_total = self.calc_highest_total(hand)
		if dealer_hand == False and self.has_splits():
			number = self.get_player_hand_number()
			text = text + " hand #" + str(number) + ": " + str(hand) + " ";
		else:
			text = text + " hand: " + str(hand) + " ";
		if highest_total > 21:
			text = text + "Bust!"
		elif (dealer_hand == False or show_all_cards == True) and self.is_blackjack(hand):
			text = text + "Blackjack!"			
		elif dealer_hand == False and show_all_cards == False and highest_total != self.calc_lowest_total(self.get_player_hand()):
			text = text + str(self.calc_lowest_total(self.get_player_hand())) + " or " + str(highest_total)
		elif dealer_hand == True and show_all_cards == False:
			text = text + str(self.calc_highest_total(hand)) + " + ?"
		else:
			text = text + str(self.calc_highest_total(hand))			
		print(text)

	def decide_insurance(self):
		response = self.ui.noyes_prompt("Insurance: ")
		if response == 'y':
			return self.YES;
		return self.NO

	def decide_insurance_amount(self):
		return self.ui.double_prompt("Enter insurance amount", "Error: bad insurance amount", 0, self.get_current_bet() / 2, '$')

	def decide_hand(self, choices):
		advice = ""
		if self.advise:
			if self.strategy == False:
				self.strategy = self.load_strategy(self.STANDARD_STRATEGY_FILENAME)
			auto = self.advise_hand(self.strategy, choices)
			advice = "Advice: " + auto[0].upper() + auto[1:] + "."
		response = self.ui.prompt(choices, advice)
		if response == 'h':
			return self.HIT;
		if response == 'd':
			return self.DOUBLE;
		if response == 'p':
			return self.SPLIT;
		if response == 'u':
			return self.SURRENDER;
		return self.STAND;

	def end_hand(self, results):
		# Show results
		for result in results:
			print(self.get_result_text(result))
		
		# Save user info
		if len(self.user) > 0:
			card_counting_strategy = self.NONE
			if self.card_counting_strategy != None:
				card_counting_strategy = self.card_counting_strategy.get_card_counting_strategy()
			self.users.save(self.user, self.get_bankroll(), self.get_starting_bet(), self.advise, card_counting_strategy)

	def run(self):
		# Main game loop
		while True:
			# Print stat line with cash and current bet
			stat_line = "\n"
			if len(self.user) > 0:
				stat_line = stat_line + self.user
			else:
				stat_line = stat_line + "Guest"
			stat_line = stat_line + ", Cash: $" + str(self.get_bankroll()) + ", Bet: $" + str(self.get_starting_bet())
			if self.get_bet_multiplier() != 1.0:
				stat_line = stat_line + ", Multiplier: " + str(self.get_bet_multiplier())
			print(stat_line)

			# Print card counting stats if a card counting strategy has been selected
			if self.get_card_counting_strategy() != None and self.get_card_counting_strategy().has_counting_method():
				stat_line = self.get_card_counting_strategy().get_counting_method() + ", Count: " + str(self.get_card_counting_strategy().get_count())
				if self.get_card_counting_strategy().is_using_true_count():
					stat_line = stat_line + ", True count: " + str(self.get_card_counting_strategy().get_true_count())
				print(stat_line)

			# Show main menu
			response = self.ui.prompt(["continue", "bet multiplier", "options", "quit"])
			if response == 'q':
				break
			else:
				deal = False
				if response == 'b':
					min = self.get_rules().get_minimum_bet() / self.get_starting_bet()
					max = self.get_rules().get_maximum_bet() / self.get_starting_bet()
					multiplier = self.ui.double_prompt("Enter bet multiplier (current multiplier = " + str(self.get_bet_multiplier()) + "): ", "Error: Bad multiplier entered!", min, max)
					self.set_bet_multiplier(multiplier)
				elif response == 'c':
					deal = True
				elif response == 'o':
					while True:
						response = self.ui.prompt(["back", "new bet", "advise", "counting strategy"], "Set option:")
						if response == 'b':
							break
						elif response == 'n':
							bet = self.ui.int_prompt("Enter new bet (current bet = $" + str(self.get_starting_bet()) + "): ", "Error: Bad bet entered!", self.get_rules().get_minimum_bet(), self.get_rules().get_maximum_bet(), "$")
							self.set_starting_bet(bet)
							self.set_bet_multiplier(1.0)
						elif response == 'a':
							response = self.ui.yesno_prompt("Advise (current setting = " + str(self.advise) + "): ")
							if response == 'y':
								self.advise = True
							else:
								self.advise = False
						elif response == 'c':
							card_counting_strategy = self.NONE
							if self.card_counting_strategy != None:
								card_counting_strategy = self.card_counting_strategy.get_card_counting_strategy()
							list = CardCounting(self.log, 1).list_card_counting_strategies()
							if not self.NONE in list:
								list.insert(0, self.NONE)
							index = self.ui.list_prompt("Choose strategy from list (current setting = " + card_counting_strategy + ")", "Error: Invalid choice!", list)
							card_counting_strategy = list[index]
							if card_counting_strategy == self.NONE:
								self.card_counting_strategy = None
							else:
								self.load_card_counting_strategy(card_counting_strategy)
				if deal == True:
					self.set_current_bet(self.get_starting_bet() * self.get_bet_multiplier())
					self.play_hand()