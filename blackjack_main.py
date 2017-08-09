from logging import *
from blackjack_auto import BlackjackAutoGame

if __name__=="__main__":
	log = Logging(LogSource.PRINT, LogLevel.INFO)
	auto = BlackjackAutoGame(log)
	auto.run()