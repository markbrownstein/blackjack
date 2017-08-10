from logging import *
from blackjack_auto import BlackjackAuto
from blackjack_auto_game import BlackjackAutoGame

if __name__=="__main__":
	new = False
	log = Logging(LogSource.PRINT, LogLevel.WARNING)
	if new:
		game = BlackjackAutoGame(log)
		game.run()
	else:
		auto = BlackjackAuto(log)
		auto.run()