from Updateable import Updateable
from Drawable 	import Drawable
from Moveable 	import Moveable
from Box 		import Box
from Config		import Config

delivery_debug = Config.get_val("delivery_debug")
score = Config.get_val("score")

class Delivery_Block(Drawable, Updateable):
	delivery_blocks = {}

	def __init__(self, pos=[0,0], col=[30,30,30], delivering=1, time=1):
		super(Delivery_Block, self).__init__(pos, col)
		Updateable.__init__(self)

		self.delivering = delivering
		self.time = time
		self.counter = 0

		if tuple(self.position) in Delivery_Block.delivery_blocks:
			del Delivery_Block.delivery_blocks[tuple(self.position)]
			print("Delivery Block Overlap Detected") if delivery_debug else 0

		Delivery_Block.delivery_blocks[tuple(self.position)] = self
		print("Delivery Block created\n  Delivering: " + str(delivering) + "\n  Time: " + str(time)) if delivery_debug else 0

	def update_self(self, dt):

		score = 0
		self.counter += dt

		if self.counter > self.time:
			self.counter = 0
			print("Updating Delivery Block \n  Position: " + str(self.position) + "\n  Delivering: " + str(self.delivering) + "\n  Time: " + str(self.time)) if delivery_debug else 0

			if tuple(self.position) in Moveable.moveables:
				m = Moveable.moveables[tuple(self.position)]
				if (type(m) is Box) and (self.delivering == 0):
					m.delete()
					score += 1
					print("    Taking Box to Deliver") if delivery_debug else 0
				return score

			if self.delivering:
				Box(pos=[self.position[0], self.position[1]])
				print("    Delivering Box") if delivery_debug else 0
			else:
				score -= 1
				print("    Missed a Delivery") if delivery_debug else 0
		return score

	def delete(self):
		Drawable.delete(self)
		Updateable.delete(self)
		del Delivery_Block.delivery_blocks[tuple(self.position)]