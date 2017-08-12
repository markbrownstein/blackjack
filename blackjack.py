import sys

from logging import *

from blackjack_command_line_ui_game import BlackjackCommandLineUIGame
from blackjack_auto_game import BlackjackAutoGame

UI = "ui"
AUTO = "auto"

NONE = "none" # 0
SEVERE = "severe" # 1
WARNING = "warning" # 2
INFO = "info" # 3
FINE = "fine" # 4
FINER = "finer" # 5
FINEST = "finest" # 6

if __name__=="__main__":
	print_intructions = True
	if len(sys.argv) > 1:
		# Read log level from command line
		log_level = 0
		if len(sys.argv) > 2:
			if SEVERE == sys.argv[2].lower():
				log_level = 1
			elif WARNING == sys.argv[2].lower():
				log_level = 2
			elif INFO == sys.argv[2].lower():
				log_level = 3
			elif FINE == sys.argv[2].lower():
				log_level = 4
			elif FINER == sys.argv[2].lower():
				log_level = 5
			elif FINEST == sys.argv[2].lower():
				log_level = 6
		log = Logging(LogSource.PRINT, log_level)

		# Read INI section from command line
		section = "DEFAULT"
		if len(sys.argv) > 3:
			section = sys.argv[3]
		
		# Run game
		if UI == sys.argv[1].lower():
			print_intructions = False
			game = BlackjackCommandLineUIGame(log, section)
			game.run()
		elif AUTO == sys.argv[1].lower():
			print_intructions = False
			game = BlackjackAutoGame(log, section)
			game.run()
	if print_intructions == True:
		print("Usage: blackjack.py [ ui|auto ] { none|severe|warning|info|fine|finer|finest } { DEFAULT }")