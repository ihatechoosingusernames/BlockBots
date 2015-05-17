import pyglet
import math
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse

from Updateable import Updateable
from Drawable 	import Drawable
from Moveable 	import Moveable
from Robot 		import Robot
from Box 		import Box
from Conveyor 	import Conveyor
from Programmer import Programmer
from Delivery_Block import Delivery_Block
import Config

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
		global time_count
		time_count += dt
		if(dt != 0):
			Updateable.update(dt, time_count)
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
				self.instruction = self.instruction[0:len(self.instruction)-1] # Removes last characterobot

			self.console = pyglet.text.Label(text=self.instruction, y=5, x=5)

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

window = Main_Window()
pyglet.app.run()