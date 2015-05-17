from Moveable import Moveable
from Config		import Config

class Box(Moveable):
	def __init__(self, pos=[0,0], col=(0,0,255)):
		super(Box, self).__init__(pos, col)