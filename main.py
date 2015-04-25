import pyglet
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse

size = 20

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

	def on_key_press(self, symbol, modifiers): {}

	def on_text(self, text):
		self.instruction += text
		self.label = pyglet.text.Label(self.instruction)
		self.robot.set_instruction(self.instruction)

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
#			self.speed = 5

	def update_pos(self, dt):
		diff = [int((self.position[0] - self.shape[0]) * (dt)), int((self.position[1] - self.shape[1]) * (dt))] #Not sure what's going on with dt here, but fun things are happening!
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
		self.instruction = ""
		self.current_instruction = ("" , -1)

	def update(self, dt):
		self.update_counter += dt

		if(self.update_counter > self.update_time):

			self.update_counter = 0

			if self.current_instruction[0] == 'w' or 'a' or 's' or 'd':
				self.move_instruction()
			elif self.current_instruction[0] == '*':
				self.current_instruction = (self.instruction[self.current_instruction[1]-1], self.current_instruction[1]-1)
				self.move_instruction()

			if len(self.instruction)-1 != self.current_instruction[1]:
				self.current_instruction = (self.instruction[self.current_instruction[1]+1], self.current_instruction[1]+1)
			elif len(self.instruction) > 0:
				self.current_instruction = (self.instruction[0], 0)

	def set_instruction(self, inst):
		self.instruction = inst
		self.current_instruction = (inst[0], 0)

	def move_instruction(self):
		if self.current_instruction[0] == 'w':
			self.move_up()
		elif self.current_instruction[0] == 's':
			self.move_down()
		elif self.current_instruction[0] == 'a':
			self.move_left()
		elif self.current_instruction[0] == 'd':
			self.move_right()

class Box(Moveable): {}

window = Main_Window()
pyglet.app.run()