# Interprets the Config file

class Config:

	@staticmethod
	def get_val(val):
		with open("Config.txt") as cfg:
			for line in cfg:
				if line.startswith(val):
					return int(line.split("= ")[1])