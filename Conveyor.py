from Updateable import Updateable
from Drawable 	import Drawable
from Moveable 	import Moveable
from Config		import Config

cfg = Config()

conveyor_debug = cfg.conveyor_debug

class Conveyor(Drawable, Updateable):
	conveyors = {}

	def __init__(self, pos=[0,0], col=(255,255,0), dir="w"):
		super(Conveyor, self).__init__(pos, col)
		Updateable.__init__(self)
		self.dir = dir

		if tuple(self.position) in Conveyor.conveyors: # Avoids double ups
			del Conveyor.conveyors[tuple(self.position)]

		Conveyor.conveyors[tuple(self.position)] = self

	def update_self(self, dt):
		print("Conveyor Direction: " + self.dir) if conveyor_debug else 0
		if tuple(self.position) in Moveable.moveables:
			m = Moveable.moveables[tuple(self.position)]

			if self.dir == "w":
				m.move_up()
			elif self.dir == "a":
				m.move_left()
			elif self.dir == "s":
				m.move_down()
			elif self.dir == "d":
				m.move_right()
			print("Found Moveable and moved it") if conveyor_debug else 0
			return

	def delete(self):
		Drawable.delete(self)
		Updateable.delete(self)
		del Conveyor.conveyors[tuple(self.position)]