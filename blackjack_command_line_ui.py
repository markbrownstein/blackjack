from logging import *
from command_line_ui import CommandLineUI
from blackjack_rules import BlackjackRules
from blackjack_game import BlackjackGame
from blackjack_command_line_ui_game import BlackjackCommandLineUIGame

def print_dealer_hand(game, hidden):
	dealer_hand = list(game.get_dealer_hand())
	if hidden == True:
		dealer_hand[0] = '??'
		print("Dealer hand: " + str(dealer_hand) + " " + str(game.calc_highest_total(dealer_hand)) + "+??")
	else:
		highest_total = game.calc_highest_total(game.get_dealer_hand())
		if highest_total > 21:
			print("Dealer hand: " + str(game.get_dealer_hand()) + " Bust!")
		else:
			print("Dealer hand: " + str(game.get_dealer_hand()) + " " + str(highest_total))

def print_player_hand(game):
	highest_total = game.calc_highest_total(game.get_player_hand())
	if highest_total > 21:
			print("Player hand: " + str(game.get_player_hand()) + " Bust!")
	else:
		lowest_total = game.calc_lowest_total(game.get_player_hand())
		if highest_total == lowest_total:
			print("Player hand: " + str(game.get_player_hand()) + " " + str(highest_total))
		else:
			print("Player hand: " + str(game.get_player_hand()) + " " + str(lowest_total) + " or " + str(highest_total))

if __name__=="__main__":
	new = False
	log = Logging(LogSource.PRINT, LogLevel.WARNING)
	if new:
		game = BlackjackCommandLineUIGame(log, 500, 5)
		game.run()
	else:
		ui = CommandLineUI(log)
		game = BlackjackGame(log, 500)
		start_bet = 5
		while True:
			bet = start_bet
			print("Cash: $" + str(game.get_bankroll()) + ", Bet: $" + str(bet))
			response = ui.prompt(["continue", "new bet", "quit"])
			if response == 'q':
				break
			else:
				deal = False
				if response == 'n':
					while True:
						prompt = "[ Enter new bet between $" + str(game.get_rules().get_minimum_bet()) + " and $" + str(game.get_rules().get_maximum_bet()) + " ] "
						response = input(prompt)
						if response.isdigit():
							num = int(response)
							if num >= game.get_rules().get_minimum_bet() and num <= game.get_rules().get_maximum_bet():
								start_bet = num
								break
						print("Error: Bad bet entered!")
					deal = True
				elif response == 'c':
					deal = True
				if deal == True:
					game.deal_hand(bet)
					print_player_hand(game)
					print_dealer_hand(game, True)
					# TODO: This is where insurance would go
					if game.is_hand_over() == False:
						while True:
							commands = ["hit", "stand"]
							if game.can_double_down(game.get_player_hand(), bet):
								commands.append("double down")
							response = ui.prompt(commands)
							if response == 's':
								break
							if response == 'h':
								game.deal_card_to_player()
								print_player_hand(game)
								print_dealer_hand(game, True)
								if game.is_hand_over() == True:
									break
							if response == 'd':
								bet = bet * 2
								game.deal_card_to_player()
								print_player_hand(game)
								print_dealer_hand(game, True)
								break
					print_player_hand(game)
					while True:
						print_dealer_hand(game, False)
						if game.is_hand_over(True):
							break
						game.deal_card_to_dealer()
					result = game.finish_hand(bet)
					if result == 2:
						print("Blackjack! Player WINS!")
					elif result == 1:
						print("Player WINS!")
					elif result == 0:
						print("PUSH!")
					elif result == -1:
						print("Player LOSES!")
