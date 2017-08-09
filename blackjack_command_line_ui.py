from logging import *
from blackjack_game import BlackjackGame

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
	log = Logging(LogSource.PRINT, LogLevel.WARNING)
	minimum_bet = 1
	maximum_bet = 100
	game = BlackjackGame(log, 1, 500)
	bet = 5
	while True:
		print("Cash: $" + str(game.get_bankroll()) + ", Bet: $" + str(bet))
		prompt = "[ C)ontinue, N)ew bet or Q)uit ] "
		response = input(prompt)
		if response == 'q' or response == 'Q':
			break
		else:
			deal = False
			if response == 'n' or response == 'N':
				while True:
					prompt = "[ Enter new bet between $" + str(minimum_bet) + " and $" + str(maximum_bet) + "] "
					response = input(prompt)
					if response.isdigit():
						num = int(response)
						if num >= minimum_bet and num <= maximum_bet:
							bet = num
							break
					print("Error: Bad bet entered!")
				deal = True
			elif response == 'c' or response == 'c':
				deal = True
			if deal == True:
				game.deal_hand(bet)
				print_dealer_hand(game, True)
				print_player_hand(game)
				if game.is_hand_over() == False:
					while True:
						prompt = "[ S)tand or H)it ] "
						response = input(prompt)
						if response == 's' or response == 'S':
							break
						if response == 'h' or response == 'H':
							game.deal_card_to_player()
							print_dealer_hand(game, True)
							print_player_hand(game)
							if game.is_hand_over() == True:
								break
				print_dealer_hand(game, False)
				print_player_hand(game)
				game.finish_hand(bet)
