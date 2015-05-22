import pyglet
import math
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse

from Updateable import Updateable
from Drawable 	import Drawable
from Robot 		import Robot
from Box 		import Box
from Conveyor 	import Conveyor
from Programmer import Programmer
from Delivery_Block import Delivery_Block
from Config		import Config
from Program_Visualiser import Program_Visualiser

cfg = Config()

window_width 	= cfg.window_width
window_height 	= cfg.window_height
time_count 		= cfg.time_count
score 			= cfg.score
size 			= cfg.size

class Main_Window(pyglet.window.Window):
	def __init__(self):
		super(Main_Window, self).__init__(width=window_width, height=window_height)
		self.set_caption("BlockBots!")

		self.selected = 0
		self.instruction = "program visualiser"
		self.console = pyglet.text.Label(text=self.instruction, y=5, x=5)
		self.score = pyglet.text.Label(text=str(score), x=int(window_width/2), y=int(window_height-15), bold=1)

		pyglet.clock.schedule(self.update)

		self.map_init()

	def map_init(self):
		Robot(pos=[20,0])
		Box(pos=[20,20])
		Delivery_Block(pos=[20,60], delivering=1, time=2)
		Programmer([20,40], program="(0,w,->1)(1,s,->2)(2,,)")
		Conveyor(pos=[20,80], dir="d")
		Box(pos=[20,80])
		Conveyor(pos=[40,80], dir="d")
		Delivery_Block(pos=[60,80], delivering=0, time=2)

		Robot(pos=[100,100])
		Box(pos=[120,100])

	def update(self, dt):
		global time_count, score
		time_count += dt
		if(dt != 0):
			score += Updateable.update(dt, time_count)
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
		position = [int(x - x%size), int(y - y%size)]

		if button == pyglet.window.mouse.LEFT:

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
						if d is self.selected:
							self.selected = 0
						d.delete()
			elif self.instruction.startswith("program visualiser"):
				self.selected = Program_Visualiser(pos=position)

window = Main_Window()
pyglet.app.run()