from blackjack_game import BlackjackGame

def print_dealer_hand(game):
	dealer_hand = game.get_dealer_hand()
	dealer_hand[0] = '??'
	print("Dealer hand: " + str(dealer_hand) + " " + str(game.calc_highest_total(dealer_hand)) + "+??")

def print_player_hand(game):
	highest_total = game.calc_highest_total(game.get_player_hand())
	lowest_total = game.calc_lowest_total(game.get_player_hand())
	if highest_total == lowest_total:
		print("Player hand: " + str(game.get_player_hand()) + " " + str(highest_total))
	else:
		print("Player hand: " + str(game.get_player_hand()) + " " + str(lowest_total) + " or " + str(highest_total))

if __name__=="__main__":
	minimum_bet = 1
	maximum_bet = 100
	game = BlackjackGame(1, 500)
	bet = 5
	while True:
		prompt = "Cash: $" + str(game.get_bankroll()) + " => (C)continue - bet $" + str(bet) + ", (N)ew bet or (Q)uit? "
		response = input(prompt)
		if response == 'q' or response == 'Q':
			break
		else:
			deal = False
			if response == 'n' or response == 'N':
				while True:
					prompt = "Enter new bet (between $" + str(minimum_bet) + " and $" + str(maximum_bet) + "): $"
					response = input(prompt)
					if response.isdigit():
						num = int(response)
						if num >= minimum_bet and num <= maximum_bet:
							bet = num
							break
					print("Bad bet entered")
				deal = True
			elif response == 'c' or response == 'c':
				deal = True
			if deal == True:
				game.deal_hand(bet)
				print_dealer_hand(game)
				print_player_hand(game)
				
