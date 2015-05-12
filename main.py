import pyglet
import math
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse

size = 20
window_width = 800
window_height = 600

score = 0

parser_debug = 0 	# Change these to 1 for various debugging printouts
conveyor_debug = 0
draw_debug = 0
programmer_debug = 0
delivery_debug = 0

class Main_Window(pyglet.window.Window):
	def __init__(self):
		super(Main_Window, self).__init__(width=window_width, height=window_height)
		self.set_caption("BlockBots!")

		self.selected = 0
		self.instruction = ""
		self.console = pyglet.text.Label(text=self.instruction, y=5, x=5)
		self.score = pyglet.text.Label(text=str(score), x=int(window_width/2), y=int(window_height-15), bold=1)

		pyglet.clock.schedule(self.update)

		self.map_init()

	def map_init(self): {}

	def update(self, dt):
		if(dt != 0):
			Updateable.update(dt)
			Moveable.update(dt)
			self.score = pyglet.text.Label(text=str(score), x=int(window_width/2), y=int(window_height-15), bold=1)

	def on_draw(self):
		self.clear()
		Drawable.draw()
		self.console.draw()
		self.score.draw()

	def on_key_press(self, symbol, modifiers):
		if symbol == key.ENTER:
			self.selected.set_instruction(self.instruction)

		if symbol == key.BACKSPACE:
			if modifiers & key.MOD_SHIFT:
				self.instruction = "" # Deletes whole line
			else:
				self.instruction = self.instruction[0:len(self.instruction)-1] # Removes last character

			self.console = pyglet.text.Label(self.instruction)

	def on_text(self, text):
		self.instruction += text
		self.console = pyglet.text.Label(self.instruction, y=5, x=5)

	def on_mouse_release(self, x, y, button, modifiers):
		if button == pyglet.window.mouse.LEFT:
			position = [int(x - x%size), int(y - y%size)]

			if self.instruction == "box":
				Box(position)
			elif self.instruction.startswith("programmer"):
				self.selected = Programmer(position, program=self.instruction.split("programmer")[1])
			elif self.instruction.startswith("conveyor"):
				Conveyor(pos=position, dir=self.instruction.split(" ")[1])
			elif self.instruction == "robot":
				self.selected = Robot(pos=position)
			elif self.instruction.startswith("delivery"):
				self.selected = Delivery_Block(pos=position, delivering=int(self.instruction.split(" ")[1]), time=int(self.instruction.split(" ")[2]))
			elif self.instruction == "delete":
				for d in Drawable.drawables:
					if d.position == position:
						d.delete()

class Updateable:
	updateables = []

	update_counter = 0
	update_time = 1

	def __init__(self):
		Updateable.updateables.append(self)

	def update_self(self): {}

	@staticmethod
	def update(dt):
		Updateable.update_counter += dt

		if Updateable.update_counter > Updateable.update_time:
			Updateable.update_counter = 0
			for u in Updateable.updateables:
				u.update_self(Updateable.update_time)

	def delete(self):
		Updateable.updateables.remove(self)

class Drawable:
	drawables = []

	def __init__(self, pos=[0,0], col=(255,255,255)):
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

	def delete(self):
		Drawable.drawables.remove(self)

class Moveable(Drawable):
	moveables = []

	update_time = 1
	update_counter = 0

	@staticmethod
	def update(dt):
		Moveable.update_counter += dt

		if Moveable.update_counter > Moveable.update_time:
			Moveable.update_counter = 0

			for m in Moveable.moveables:
				m.update_self(dt)
				m.update_pos(dt)

	def __init__(self, pos=[0,0], col=(0,0,0)):
		super(Moveable, self).__init__(pos, col)
		if(self.collides()):
			raise Exception("Don't stack the boxes, this is a 2D game!")
		else:
			self.moveables.append(self)
			self.speed = 2

	def delete(self):
		Drawable.drawables.remove(self)
		Moveable.moveables.remove(self)

	def update_pos(self, dt):
		diff = [int(self.position[0] - self.shape[0]), int(self.position[1] - self.shape[1])]

		for i in range(0, len(self.shape), 2):
			self.shape[i] += diff[0]
			self.shape[i+1] += diff[1]

	def update_self(self, dt): {}

	def move_up(self):
		self.move([0, 1])

	def move_down(self):
		self.move([0, -1])

	def move_left(self):
		self.move([-1, 0])

	def move_right(self):
		self.move([1, 0])

	def move(self, move_vec): # Moves the Moveable when given a vector [squares_x, squares_y]
		distance_vec = [size * move_vec[0], size * move_vec[1]]

		self.position[0] += distance_vec[0]
		self.position[1] += distance_vec[1]

		if(self.collides()):
			collision_type, collider = self.collides()
			if(collision_type == 1):
				collider.move(move_vec)
				collider.update_pos(0)
				self.position[0] = collider.position[0] - distance_vec[0]
				self.position[1] = collider.position[1] - distance_vec[1]
			else:
				self.position[0] -= distance_vec[0]
				self.position[1] -= distance_vec[1]

	def collides(self):
		for x in Moveable.moveables:
			if (x.position == self.position) and (x != self):
				return 1, x

		if (self.position[0] > window_width-size) or (self.position[0] < 0) or (self.position[1] > window_height-size) or (self.position[1] < 0):
			return 2, 0

class Robot(Moveable):
	def __init__(self, pos=[0,0], col=(0,255,0)):
		super(Robot, self).__init__(pos, col)
		self.instruction = "(1,,w->2/a->3/s->4/d->5)(2,w,)(3,a,)(4,s,)(5,d,)"
		self.current_instruction = ["", -1] # The name of the current instruction and the number of actions still to go within that instruction

	def update_self(self, dt):
		self.run_instruction()

	def set_instruction(self, inst):
		self.instruction = inst
		self.current_instruction = [inst.split("(")[0].split(",")[0], -1] # Sets current instruction to first instruction name

	# Runs robot instructions of format: (Instruction Name,Actions,Transitions)
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
				evaluation = 1 if (not len(condition)) and len(t) else 0 # The result of the transition rule
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

		f = lambda d: 1 if ((d.position[0] - self.position[0] == size or -size) and (d.position[size] - self.position[size] == size or -size)) else 0

		if side == "w":
			f = lambda d: 1 if (d.position[0] == self.position[0]) and (d.position[1] - self.position[1] == size) else 0
		elif side == "a":
			f = lambda d: 1 if (d.position[1] == self.position[1]) and (d.position[0] - self.position[0] == -size) else 0
		elif side == "s":
			f = lambda d: 1 if (d.position[0] == self.position[0]) and (d.position[1] - self.position[1] == -size) else 0
		elif side == "d":
			f = lambda d: 1 if (d.position[1] == self.position[1]) and (d.position[0] - self.position[0] == size) else 0

		for m in Moveable.moveables:
			if f(m):
				return 1

		return 0

class Box(Moveable):
	def __init__(self, pos=[0,0], col=(0,0,255)):
		super(Box, self).__init__(pos, col)

class Conveyor(Drawable, Updateable):
	conveyors = []

	def __init__(self, pos=[0,0], col=(255,255,0), dir="w"):
		super(Conveyor, self).__init__(pos, col)
		Updateable.__init__(self)
		self.dir = dir

		for c in Conveyor.conveyors: #Avoids double ups, as there is no inbuilt collision detection
			if (c.position == self.position) and (c.dir == self.dir):
				return

		Conveyor.conveyors.append(self)

	def update_self(self, dt):
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

	def delete(self):
		Drawable.delete(self)
		Conveyor.conveyors.remove(self)

class Programmer(Drawable, Updateable):
	programmers = []

	def __init__(self, pos=[0,0], col=(210,210,210), program=""):
		super(Programmer, self).__init__(pos, col)
		Updateable.__init__(self)

		self.program = program

		for p in Programmer.programmers: # A new programmer placecd on an old one will replace it
			if(p.position == self.position):
				Programmer.programmers.remove(p)

		Programmer.programmers.append(self)
		print("Programmer succesfully added") if programmer_debug else 0

	def update_self(self, dt):
		print("Programmer updating self") if programmer_debug else 0

		for m in Moveable.moveables:
			if m.position == self.position:
				print("Something in the same position") if programmer_debug else 0
				if type(m) is Robot:
					m.set_instruction(self.program)
					print("Programmed a robot") if programmer_debug else 0

	def delete(self):
		Drawable.delete(self)
		Updateable.delete(self)
		Programmer.programmers.remove(self)

	def set_instruction(self, instruction):
		self.program = instruction
		print("Programmer programmed") if programmer_debug else 0

class Delivery_Block(Drawable, Updateable):
	delivery_blocks = []

	def __init__(self, pos=[0,0], col=[30,30,30], delivering=1, time=1):
		super(Delivery_Block, self).__init__(pos, col)
		Updateable.__init__(self)

		self.delivering = delivering
		self.time = time
		self.counter = 0

		for d in Delivery_Block.delivery_blocks:
			if self.position == d.position:
				d.delete()
				print("Delivery Block Overlap Detected") if delivery_debug else 0
				continue

		Delivery_Block.delivery_blocks.append(self)
		print("Delivery Block created\n  Delivering: " + str(delivering) + "\n  Time: " + str(time)) if delivery_debug else 0

	def update_self(self, dt):

		global score
		self.counter += dt

		if self.counter > self.time:
			self.counter = 0
			print("Updating Delivery Block \n  Position: " + str(self.position) + "\n  Delivering: " + str(self.delivering) + "\n  Time: " + str(self.time)) if delivery_debug else 0

			for m in Moveable.moveables:
				if m.position == self.position:
					if (type(m) is Box) and (self.delivering == 0):
						m.delete()
						score += 1
						print("    Taking Box to Deliver") if delivery_debug else 0
					return

			if self.delivering:
				Box(pos=[self.position[0], self.position[1]])
				print("    Delivering Box") if delivery_debug else 0
			else:
				score -= 1
				print("    Missed a Delivery") if delivery_debug else 0

	def delete(self):
		Drawable.delete(self)
		Updateable.delete(self)
		Delivery_Block.delivery_blocks.remove(self)

window = Main_Window()
pyglet.app.run()