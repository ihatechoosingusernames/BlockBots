import pyglet
import math
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse

size = 20
window_width = 640
window_height = 480

parser_debug = 0 	# Change to 1 for parser debugging printouts
conveyor_debug = 0 	# Change to 1 for conveyor debugging printouts
draw_debug = 0 		# Change to 1 for draw debugging printouts

class Main_Window(pyglet.window.Window):
	def __init__(self):
		super(Main_Window, self).__init__(width=window_width, height=window_height)
		self.set_caption("BlockBots!")

		self.robot = Robot()
		self.instruction = self.robot.instruction
		self.label = pyglet.text.Label(self.instruction)

		pyglet.clock.schedule(self.update)

		self.map_init()

	def map_init(self):
		Conveyor(pos=[0,int(window_height/2)], dir="d")

		Box(pos=[0,int(window_height/2)])

	def update(self, dt):
		if(dt != 0):
			Moveable.update(dt)
			Conveyor.update(dt)
			self.robot.update(dt)

	def on_draw(self):
		self.clear()
		Drawable.draw()
		self.label.draw()

	def on_key_press(self, symbol, modifiers):
		if symbol == key.ENTER:
			self.robot.set_instruction(self.instruction)
			self.label = pyglet.text.Label(self.instruction, color=(0,255,0,0))

		if symbol == key.BACKSPACE:
			if modifiers & key.MOD_SHIFT:
				self.instruction = "" # Deletes whole line
			else:
				self.instruction = self.instruction[0:len(self.instruction)-1] # Removes last character

			self.label = pyglet.text.Label(self.instruction)

	def on_text(self, text):
		self.instruction += text
		self.label = pyglet.text.Label(self.instruction)

	def on_mouse_release(self, x, y, button, modifiers):
		if button == pyglet.window.mouse.LEFT:
			Box([int(x - x%size), int(y - y%size)])

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		if buttons == pyglet.window.mouse.RIGHT:
			input_dir = ""
			if math.fabs(dx) > math.fabs(dy): # Finding the main direction of the dragging
				if dx > 0:
					input_dir = "d"
				else:
					input_dir = "a"
			else:
				if dy > 0:
					input_dir = "w"
				else:
					input_dir = "s"

			Conveyor(pos=[int(x - x%size), int(y - y%size)], dir=input_dir) # New Conveyor!

class Drawable:
	drawables = []

	def __init__(self, pos=[1,1], col=(255,255,255)):
		self.position = pos
		self.shape = [self.position[0], self.position[1], self.position[0] + size, self.position[1], self.position[0] + size, self.position[1] + size, self.position[0], self.position[1] + size]
		self.colour = col
		Drawable.drawables.append(self)

	@staticmethod
	def draw():
		for d in Drawable.drawables:
			d.draw_self()

	def draw_self(self):
		print("Colour :" + str((self.colour + self.colour + self.colour + self.colour))) if draw_debug else 0
		
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

		for i in range(0, len(self.shape), 2):
			self.shape[i] += diff[0]
			self.shape[i+1] += diff[1]

	def move_up(self):
		self.position[1] += size

		if(self.collides()): # Collision testing
			collision_type, collider = self.collides()
			if(collision_type == 1): # If it collides with another moveable
				collider.move_up()
				self.position[1] = collider.position[1] - size # Stay behind the other moveable if it hits a wall
			else: # If it hits a wall
				self.position[1] -= size

	def move_down(self):
		self.position[1] -= size

		if(self.collides()):
			collision_type, collider = self.collides()
			if(collision_type == 1):
				collider.move_down()
				self.position[1] = collider.position[1] + size
			else:
				self.position[1] += size

	def move_left(self):
		self.position[0] -= size

		if(self.collides()):
			collision_type, collider = self.collides()
			if(collision_type == 1):
				collider.move_left()
				self.position[0] = collider.position[0] + size
			else:
				self.position[0] += size

	def move_right(self):
		self.position[0] += size

		if(self.collides()):
			collision_type, collider = self.collides()
			if(collision_type == 1):
				collider.move_right()
				self.position[0] = collider.position[0] - size
			else:
				self.position[0] -= size

	def collides(self):
		for x in self.moveables:
			if(x.position == self.position):
				if(x != self):
					return 1, x

		if (self.position[0] > window_width) or (self.position[0] < 0) or (self.position[1] > window_height) or (self.position[1] < 0):
			return 2, 0

class Robot(Moveable):
	def __init__(self):
		super(Robot, self).__init__(pos=[1,1], col=(0,255,0))
		self.update_time = 1
		self.update_counter = 0
		self.instruction = "(0,wwdd,!d->1)(1,,w->2/a->3/s->4/d->5)(2,w,)(3,a,)(4,s,)(5,d,)"
		self.current_instruction = ["", -1] # The name of the current instruction and the number of actions still to go within that instruction 

	def update(self, dt):
		self.update_counter += dt

		if(self.update_counter > self.update_time):
			self.update_counter = 0
			self.run_instruction()

	def set_instruction(self, inst):
		self.instruction = inst
		self.current_instruction = [inst.split("(")[0].split(",")[0], -1] # Sets current instruction to first instruction name

	# Runs robot instructions of format: (Instruction Name, Actions, Transitions)
	def run_instruction(self):
		if len(self.instruction) < 1: # Checks that there are instructions to use 
			return

		inst_pos = self.instruction.find("(" + self.current_instruction[0]) + 1
		inst = self.instruction[inst_pos : self.instruction.index(")", inst_pos)] # Finds the definition of the current instruction

		inst_parts = inst.split(",") # Splits instruction into its parts

		print("Instruction Parts:\n  Name: " + inst_parts[0] + "\n  Actions: " + inst_parts[1] + "\n  Transitions: " + inst_parts[2]) if parser_debug else 0

		actions = inst_parts[1] # Should be the Actions part of the instruction

		if len(actions) > 0: # Only runs the action code if there are actions

			if self.current_instruction[1] < 0: # Checks if this is a new instruction and sets the action count if so
				self.current_instruction[1] = len(actions)

			action_index = len(actions) - self.current_instruction[1]
			print("  Action Number: " + str(action_index)) if parser_debug else 0
			self.current_instruction[1] -= 1

			if  actions[action_index] == 'w':
				self.move_up()
			elif actions[action_index] == 's':
				self.move_down()
			elif actions[action_index] == 'a':
				self.move_left()
			elif actions[action_index] == 'd':
				self.move_right()

		if self.current_instruction[1] < 1: # Checks if that was the last instruction
			self.current_instruction[1] = -1 # Sets to new instruction special value

			transitions = inst_parts[2].split("/") # Delimiting the transitions, format is: Transition_Rule_1->Destination/Transition_Rule_2->Destination etc.
			print("\nTransitions:") if parser_debug else 0

			for t in transitions: # Finding the transition that passes first
				print("  Transition Rule: " + t) if parser_debug else 0

				condition = t.split("->")[0] # Splitting it into rule and destination
				operator_stack = ["|"] # This ensures the first value is considered if there is no operator before it
				evaluation = 0 # The result of the transition rule
				for c in condition: # Parsing is very basic at the moment
					print("    Parsing Character: " + c + "    Operator Stack: " + str(len(operator_stack))) if parser_debug else 0

					if (c == 'w') or (c == 'a') or (c == 's') or (c == 'd'):
						c_result = self.sensor(c) # Find the initial value of that sensor reading
						print("    Sensor Result: " + str(c_result)) if parser_debug else 0
						p = operator_stack.pop(len(operator_stack)-1) # Find the most recent operator for it

						if p == "!": # The "not" operator is used in conjunction with other operators, so the next is popped
							c_result = not c_result
							p = operator_stack.pop(len(operator_stack)-1)

						if p == "&":
							evaluation = evaluation and c_result
						elif p == "|":
							evaluation = evaluation or c_result

						print("    Parsed  Character: " + c + "    Operator Stack: " + str(len(operator_stack)) + "    Result So Far: " + str(evaluation)) if parser_debug else 0

					else: # Add all operators to operator stack
						operator_stack.append(c)
						print("    Parsed   Operator: " + c + "    Operator Stack: " + str(len(operator_stack))) if parser_debug else 0

				if evaluation: # The first transition that evaluates true is used, if none do, the current rule loops forever
					self.current_instruction[0] = t.split("->")[1]
					print("  Transition Accepted, New Instruction: " + self.current_instruction[0]) if parser_debug else 0
					return

	# The sensor returns true if there is something occupying the specified adjacent space, default argument is any space, diagonals not included
	def sensor(self, side=""):
		print("    Sensor called on side: " + side) if parser_debug else 0

		f = lambda d: 1 if ((d.position[0] - self.position[0] == 1 or -1) or (m.position[1] - self.position[1] == 1 or -1)) else 0

		if side == "w":
			f = lambda d: 1 if (d.position[1] - self.position[1] == size) else 0
		elif side == "a":
			f = lambda d: 1 if (d.position[0] - self.position[0] == -size) else 0
		elif side == "s":
			f = lambda d: 1 if (d.position[1] - self.position[1] == -size) else 0
		elif side == "d":
			f = lambda d: 1 if (d.position[0] - self.position[0] == size) else 0

		for m in Moveable.moveables:
			if f(m):
				return 1

		return 0

class Box(Moveable):
	def __init__(self, pos=[1,1], col=(0,0,255)):
		super(Box, self).__init__(pos, col)

class Conveyor(Drawable):
	conveyors = []

	update_counter = 0
	update_time = 1

	def __init__(self, pos=[1,1], col=(255,255,0), dir="w"):
		super(Conveyor, self).__init__(pos, col)
		self.dir = dir

		for c in Conveyor.conveyors: #Avoids double ups, as there is no inbuilt collision detection
			if (c.position == self.position) and (c.dir == self.dir):
				return

		Conveyor.conveyors.append(self)

	@staticmethod
	def update(dt):
		Conveyor.update_counter += dt

		if Conveyor.update_counter > Conveyor.update_time:
			Conveyor.update_counter = 0

			for c in Conveyor.conveyors:
				c.update_self()

	def update_self(self):
		print("Conveyor Direction: " + self.dir) if conveyor_debug else 0
		for m in Moveable.moveables:
			if m.position == self.position:
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

window = Main_Window()
pyglet.app.run()