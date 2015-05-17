# Interprets the Config file

class Config:

	def __init__(self):
		with open("Config.txt") as cfg:
			for line in cfg:
				if line.startswith("size"):
					Config.size = int(line.split("= ")[1])
				elif line.startswith("window_width"):
					Config.window_width = int(line.split("= ")[1])
				elif line.startswith("window_height"):
					Config.window_height = int(line.split("= ")[1])
				elif line.startswith("score"):
					Config.score = int(line.split("= ")[1])
				elif line.startswith("update_count"):
					Config.update_count = int(line.split("= ")[1])
				elif line.startswith("time_count"):
					Config.time_count = int(line.split("= ")[1])
				elif line.startswith("parser_debug"):
					Config.parser_debug = int(line.split("= ")[1])
				elif line.startswith("conveyor_debug"):
					Config.conveyor_debug = int(line.split("= ")[1])
				elif line.startswith("programmer_debug"):
					Config.programmer_debug = int(line.split("= ")[1])
				elif line.startswith("delivery_debug"):
					Config.delivery_debug = int(line.split("= ")[1])
				elif line.startswith("collision_debug"):
					Config.collision_debug = int(line.split("= ")[1])
				elif line.startswith("update_debug"):
					Config.update_debug = int(line.split("= ")[1])
