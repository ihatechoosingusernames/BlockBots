from Config import Config

cfg = Config()

class Box:
	def __init__(self, pos=[0,0]):
		self.position = pos
		self.size = cfg.size

	def describe(self):
		print("I am Box at: " + str(self.position) + " of size: " + str(self.size))

position = [0, 10]
box = Box(position)
pos_map = {tuple(position) : box, (0,0) : Box()}

this = pos_map[tuple(position)]
box.describe()
print(str(type(this) is Box))