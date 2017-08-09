class LogLevel:
	NONE = 0
	SEVERE = 1
	WARNING = 2
	INFO = 3
	FINE = 4
	FINER = 5
	FINEST = 6
	
class LogSource:
	NONE = 0
	PRINT = 1

class Logging:
	def __init__(self, log_source, log_level):
		self.log_source = log_source
		self.log_level = log_level

	def log(self, log_level, text):
		if self.log_source != LogSource.NONE:
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
	
	def severe(self, text):
		self.log(LogLevel.SEVERE, text)

	def warning(self, text):
		self.log(LogLevel.WARNING, text)

	def info(self, text):
		self.log(LogLevel.INFO, text)

	def fine(self, text):
		self.log(LogLevel.FINE, text)

	def finer(self, text):
		self.log(LogLevel.FINER, text)

	def finest(self, text):
		self.log(LogLevel.FINEST, text)
