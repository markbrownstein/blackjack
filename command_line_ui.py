from logging import *

class CommandLineUI:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'	
    
	def __init__(self, log):
		self.log = log

	def printBlue(self, text):
		print(self.OKBLUE + text + self.ENDC)
		
	def prompt(self, option_list, text = ""):
		# Construct prompt
		prompt_text = "[ "
		if len(text) > 0:
			prompt_text = prompt_text + text + " "
		commands = []
		for i in range(len(option_list)):
			option = option_list[i]
			if len(commands) > 0:
				if i == len(option_list) - 1:
					prompt_text = prompt_text + " or "					
				else:
					prompt_text = prompt_text + ", "
			command = option[0].lower()
			if command in commands:
				i = 1				
				while True:
					command = option[i].lower()
					if not command in commands:
						break
					i = i + 1
					if i >= len(option):
						self.log.warning("No option letter available!")
						break
				if i < len(option):
					commands.append(command)
					prompt_text = prompt_text + option[0:i] + option[i].upper() + ")" + option[i + 1:]
			else:
				commands.append(command)
				prompt_text = prompt_text + option[0].upper() + ")" + option[1:]
		prompt_text = prompt_text + " ] "
		
		# Get answer
		while True:
			response = input(prompt_text).lower()
			if not response:
				response = commands[0]
				break
			if response in commands:
				break
		return response 

	def yesno_prompt(self, text = ""):
			return self.prompt(["yes", "no"], text)

	def noyes_prompt(self, text = ""):
			return self.prompt(["no", "yes"], text)
