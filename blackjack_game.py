from game import Game

if __name__=="__main__":
	game = Game(1, 500)
	game.deal_hand(5)
	print("Dealer hand: ")
	print(game.get_dealer_hand())
	print("Player hand: ")
	print(game.get_player_hand())
