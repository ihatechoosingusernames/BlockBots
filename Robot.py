from Moveable 	import Moveable
from Programmable import Programmable
from Config		import Config

cfg = Config()

size = cfg.size
parser_debug = cfg.parser_debug

class Robot(Moveable, Programmable):
	def __init__(self, pos=[0,0], col=(0,255,0)):
		super(Robot, self).__init__(pos, col)
		Programmable.__init__(self)

	def update_self(self, dt):
		super(Robot, self).update_self(0)
		self.run_instruction()
		return 0

	# The sensor returns true if there is something occupying the specified adjacent space, default argument is any space, diagonals not included
	def sensor(self, side=""):
		print("    Sensor called on side: " + side) if parser_debug else 0

		if side == "w":
			vector = [self.position[0], self.position[1] + size]
		elif side == "a":
			vector = [self.position[0] - size, self.position[1]]
		elif side == "s":
			vector = [self.position[0], self.position[1] - size]
		elif side == "d":
			vector = [self.position[0] + size, self.position[1]]

		return (self.collides(vector)[0] == 1)