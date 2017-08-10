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


	def run(self):
		while True:
			bet = self.get_starting_bet()
			print("Cash: $" + str(self.get_bankroll()) + ", Bet: $" + str(bet))
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
					self.start_hand()