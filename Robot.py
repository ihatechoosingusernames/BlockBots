from Moveable 	import Moveable
from Programmable import Programmable
from Config		import Config

size = Config.get_val("size")

class Robot(Moveable, Programmable):
	def __init__(self, pos=[0,0], col=(0,255,0), instruction="(1,,w->2/a->3/s->4/d->5)(2,w,)(3,a,)(4,s,)(5,d,)"):
		super(Robot, self).__init__(pos, col)
		Programmable.__init__(self, instruction)

	def update_self(self, dt):
		super(Robot, self).update_self(0)
		self.run_instruction()
		return 0