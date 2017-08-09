from log_level import LogLevel

class Logging:
	def __init__(self, log_level):
		self.log_level = log_level

	def log(self, log_level, text):
		if log_level != LogLevel.NONE and log_level <= self.log_level:
			if log_level == LogLevel.SEVERE:
				log_level_text = "Severe: "
			elif log_level == LogLevel.WARNING:
				log_level_text = "Warning: "
			elif log_level == LogLevel.INFO:
				log_level_text = "Info: "
			elif log_level == LogLevel.FINE:
				log_level_text = "Fine: "
			elif log_level == LogLevel.FINER:
				log_level_text = "Finer: "
			else:
				log_level_text = "Finest: "
			
			print(log_level_text + text)