from Updateable import Updateable
from Drawable 	import Drawable
from Config		import Config

class Programmer(Drawable, Updateable):
	programmers = {}

	def __init__(self, pos=[0,0], col=(210,210,210), program=""):
		super(Programmer, self).__init__(pos, col)
		Updateable.__init__(self)

		self.program = program

		if tuple(self.position) in Programmer.programmers: # A new programmer placecd on an old one will replace it
			del Programmer.programmers[tuple(self.position)]

		Programmer.programmers[tuple(self.position)] = self
		print("Programmer succesfully added") if programmer_debug else 0

	def update_self(self, dt):
		print("Programmer updating self") if programmer_debug else 0

		if tuple(self.position) in Moveable.moveables:
			m = Moveable.moveables[tuple(self.position)]
			print("  Something in the same position") if programmer_debug else 0
			if type(m) is Robot:
				m.set_instruction(self.program)
				print("  Programmed a robot") if programmer_debug else 0

	def delete(self):
		Drawable.delete(self)
		Updateable.delete(self)
		del Programmer.programmers[tuple(self.position)]

	def set_instruction(self, instruction):
		self.program = instruction
		print("Programmer programmed") if programmer_debug else 0