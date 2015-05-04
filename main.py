import pyglet
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse

size = 20
smoothness = 5;

class Main_Window(pyglet.window.Window):
	def __init__(self):
		super(Main_Window, self).__init__()
		self.set_caption("BlockBots!")

		self.robot = Robot()
		self.boxes = []
		self.instruction = ""
		self.label = pyglet.text.Label(self.instruction)

		pyglet.clock.schedule(self.update)

	def update(self, dt):
		if(dt != 0):
			Moveable.update(dt)
			self.robot.update(dt)

	def on_draw(self):
		self.clear()
		self.robot.draw()
		for b in self.boxes:
			b.draw()
		self.label.draw()

	def on_key_release(self, symbol, modifiers):
		if symbol == key.ENTER or key.RETURN:
			self.robot.set_instruction(self.instruction)

	def on_text(self, text):
		self.instruction += text
		self.label = pyglet.text.Label(self.instruction)

	def on_mouse_release(self, x, y, button, modifiers):
		if button == pyglet.window.mouse.LEFT:
			self.boxes.append(Box([int(x - x%size), int(y - y%size)], (255, 0, 255)))

class Drawable:
	def __init__(self, pos=[1,1], col=(0,0,0)):
		self.position = pos
		self.shape = [self.position[0], self.position[1], self.position[0] + size, self.position[1], self.position[0] + size, self.position[1] + size, self.position[0], self.position[1] + size]
		self.colour = col

	def draw(self):
		pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2i', self.shape), ('c3B', (self.colour + self.colour + self.colour + self.colour)))

class Moveable(Drawable):
	moveables = []

	@staticmethod
	def update(dt):
		for m in Moveable.moveables:
			m.update_pos(dt)

	def __init__(self, pos=[0,0], col=(0,0,0)):
		super(Moveable, self).__init__(pos, col)
		if(self.collides()):
			raise Exception("Don't stack the boxes, this is a 2D game!")
		else:
			self.moveables.append(self)
			self.speed = 2

	def update_pos(self, dt):
		diff = [int(self.position[0] - self.shape[0]), int(self.position[1] - self.shape[1])]
		if(self.collides()):
			if(diff[0] < 0):
				self.collides()[1].move_left()
			elif(diff[0] > 0):
				self.collides()[1].move_right()
			if(diff[1] < 0):
				self.collides()[1].move_down()
			elif(diff[1] > 0):
				self.collides()[1].move_up()

		for i in range(0, len(self.shape), 2):
			self.shape[i] += diff[0]
			self.shape[i+1] += diff[1]

	def move_up(self):
		self.position[1] += size

	def move_down(self):
		self.position[1] -= size

	def move_left(self):
		self.position[0] -= size

	def move_right(self):
		self.position[0] += size

	def collides(self):
		for x in self.moveables:
			if(x.position == self.position):
				if(x != self):
					return 1, x

class Robot(Moveable):
	def __init__(self):
		super(Robot, self).__init__(col=(0,255,0))
		self.update_time = 1
		self.update_counter = 0
		self.instruction = "(FIRST,wd,w->FIRST)"
		self.current_instruction = ["", -1] # The name of the current instruction and the number of actions still to go within that instruction 

	def update(self, dt):
		self.update_counter += dt

		if(self.update_counter > self.update_time):
			self.update_counter = 0
			self.run_instruction()

	def set_instruction(self, inst):
		self.instruction = inst
		self.current_instruction = (self.instruction[0], 0)

	# Runs robot instructions of format: (Instruction Name, Actions, Transitions)
	def run_instruction(self):
		if len(self.instruction) < 1: # Checks that there are instructions to use 
			return

		inst_pos = self.instruction.find("(" + self.current_instruction[0])
		inst = self.instruction[inst_pos : self.instruction.index(")", inst_pos)] # Finds the definition of the current instruction

		inst_parts = inst.split(",") # Splits instruction into its parts

		actions = inst_parts[1] # Should be the Actions part of the instruction

		if self.current_instruction[1] < 0: # Checks if this is a new instruction and sets the action count if so
			self.current_instruction[1] = len(actions)

		action_index = len(actions) - self.current_instruction[1]
		self.current_instruction[1] -= 1

		if  actions[action_index] == 'w':
			self.move_up()
		elif actions[action_index] == 's':
			self.move_down()
		elif actions[action_index] == 'a':
			self.move_left()
		elif actions[action_index] == 'd':
			self.move_right()

		if self.current_instruction[1] == 0: # Checks if that was the last instruction
			self.current_instruction[1] -= 1 # Sets to new instruction special value

			transitions = inst_parts[2].split("/") # Delimiting the transitions, format is: Transition_Rule_1->Destination/Transition_Rule_2->Destination etc.

			for t in transitions: # Finding the transition that passes first
				condition = t.split("->")[0] # Splitting it into rule and destination
				parse_stack = ["|"] # This ensures the first value is considered
				evaluation = 0
				for c in condition: # Parsing is very basic at the moment
					if c == 'w' or 'a' or 's' or 'd':
						c_result = self.sensor(c)
						p = parse_stack.pop(0)

						if p == "!":
							c_result = not c_result
							p = parse_stack.pop(0)

						if p == "&":
							evaluation = evaluation and c_result
						elif p == "|":
							evaluation = evaluation or c_result

					else:
						parse_stack.insert(0, c)

				if evaluation: # The first transition that evaluates true is used
					self.current_instruction[0] = t.split("->")[1]
					return

	# The sensor returns true if there is something occupying the specified adjacent space, default argument is any space, diagonals not included
	def sensor(self, side=""):
		f = lambda d: 1 if ((d.position[0] - self.position[0] == 1 or -1) or (m.position[1] - self.position[1] == 1 or -1)) else 0

		if side == "w":
			f = lambda d: 1 if (d.position[1] - self.position[1] == 1) else 0
		elif side == "a":
			f = lambda d: 1 if (d.position[0] - self.position[0] == -1) else 0
		elif side == "s":
			f = lambda d: 1 if (d.position[1] - self.position[1] == -1) else 0
		elif side == "d":
			f = lambda d: 1 if (d.position[0] - self.position[0] == 1) else 0

		for m in Moveable.moveables:
			if f(m):
				return 1

		return 0

class Box(Moveable): {}

window = Main_Window()
pyglet.app.run()