from logging import *
from command_line_ui import CommandLineUI
from blackjack_game_framework import BlackjackGameFramework

class BlackjackCommandLineUIGame(BlackjackGameFramework):
	def __init__(self, log, bankroll, starting_bet):
		# Initialize log
		self.log = log
		
		# Initialize framework
		BlackjackGameFramework.__init__(self, self.log, bankroll, starting_bet)
		
		# Initialize UI
		self.ui = CommandLineUI(self.log)

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
		text = text + " hand: " + str(hand) + " ";
		if highest_total > 21:
			text = text + "Bust!"
		elif dealer_hand == False and show_all_cards == False and highest_total != self.calc_lowest_total(self.get_player_hand()):
			text = text + str(self.calc_lowest_total(self.get_player_hand())) + " or " + str(highest_total)
		elif dealer_hand == True and show_all_cards == False:
			text = text + str(self.calc_highest_total(hand)) + " + ?"
		else:
			text = text + str(self.calc_highest_total(hand))			
		print(text)

	def decide_hand(self, choices):
		response = self.ui.prompt(choices)
		if response == 'h':
			return self.HIT;
		if response == 'd':
			return self.DOUBLE;
		return self.STAND;
		
	def end_hand(self, result):
		result_text = ""
		if result == 2:
			result_text = "Blackjack! Player WINS!"
		elif result == 1:
			result_text = "Player WINS!"
		elif result == 0:
			result_text = "PUSH!"
		elif result == -1:
			result_text = "Player LOSES!"
		print(result_text)

	def run(self):
		while True:
			print("Cash: $" + str(self.get_bankroll()) + ", Bet: $" + str(self.get_starting_bet()))
			response = self.ui.prompt(["continue", "new bet", "quit"])
			if response == 'q':
				break
			else:
				deal = False
				if response == 'n':
					while True:
						prompt = "[ Enter new bet between $" + str(self.get_rules().get_minimum_bet()) + " and $" + str(self.get_rules().get_maximum_bet()) + " ] "
						response = input(prompt)
						if response.isdigit():
							num = int(response)
							if num >= self.get_rules().get_minimum_bet() and num <= self.get_rules().get_maximum_bet():
								self.set_starting_bet(num)
								break
						print("Error: Bad bet entered!")
					deal = True
				elif response == 'c':
					deal = True
				if deal == True:
					self.set_current_bet(self.get_starting_bet())
					self.play_hand()