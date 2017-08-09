from blackjack_game import BlackjackGame

if __name__=="__main__":
	game = BlackjackGame(1, 500)
	game.deal_hand(5)
	print("Dealer hand: ")
	print(game.get_dealer_hand())
	print("Player hand: ")
	print(game.get_player_hand())
