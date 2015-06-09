from pyglet.gl import *
from Config		import Config

size = Config.get_val("size")
draw_debug = Config.get_val("draw_debug")

class Drawable:
	drawables = []
	top_layer = 0

	def __init__(self, pos=[0,0], col=(255,255,255), layer=0):
		self.position = pos
		self.shape = [self.position[0], self.position[1], self.position[0] + size, self.position[1], self.position[0] + size, self.position[1] + size, self.position[0], self.position[1] + size]
		self.colour = col
		self.layer = layer
		if layer > Drawable.top_layer:
			Drawable.top_layer = layer
		Drawable.drawables.append(self)

	@staticmethod
	def draw():
		for l in range(Drawable.top_layer+1): # Draws all drawables, lowest layers first
			for d in Drawable.drawables:
				d.draw_self() if d.layer == l else 0

	def draw_self(self):
		print("Colour :" + str((self.colour + self.colour + self.colour + self.colour))) if draw_debug else 0
		
		pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2i', self.shape), ('c3B', (self.colour + self.colour + self.colour + self.colour)))

	def delete(self):
		Drawable.drawables.remove(self)