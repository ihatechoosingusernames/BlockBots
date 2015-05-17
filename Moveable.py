from Updateable import Updateable
from Drawable 	import Drawable
from Config		import Config

class Moveable(Drawable, Updateable):
	moveables = {}

	def __init__(self, pos=[0,0], col=(0,0,0)):
		super(Moveable, self).__init__(pos, col, layer=1)
		Updateable.__init__(self)
		self.move_limit = 1 # Total distance moveable can travel in a single update.
		self.move_count = 0 # Total distance moveable has moved in this update

		if(self.collides()[0]):
			raise Exception("Don't stack the boxes, this is a 2D game! Collision at: " + str(self.position))
			Drawable.delete(self)
		else:
			Moveable.moveables[tuple(pos)] = self

	def delete(self):
		Drawable.delete(self)
		del Moveable.moveables[tuple(self.position)]

	def update_pos(self):
		diff = [int(self.position[0] - self.shape[0]), int(self.position[1] - self.shape[1])]

		for i in range(0, len(self.shape), 2):
			self.shape[i] += diff[0]
			self.shape[i+1] += diff[1]

	def update_self(self, dt):
		self.move_count = 0

	def move_up(self):
		self.move([0, 1])

	def move_down(self):
		self.move([0, -1])

	def move_left(self):
		self.move([-1, 0])

	def move_right(self):
		self.move([1, 0])

	def move(self, move_vec): # Moves the Moveable when given a vector [squares_x, squares_y]
		if self.move_count >= self.move_limit:
			return 0

		self.move_count += abs(move_vec[0]) + abs(move_vec[1])

		return_val = 1 # 1 If succesful, 0 if not

		distance_vec = [size * move_vec[0], size * move_vec[1]] # The distance it will move
		new_pos = [self.position[0] + distance_vec[0], self.position[1] + distance_vec[1]] # The new position it will occupy

		collision_type, collider = self.collides(new_pos)

		if collision_type == 1:
			print("  Attempting to push collider at " + str(self.position)) if collision_debug else 0
			return_val = collider.move(move_vec)

			if return_val:
				print("  Moving from " + str(self.position) + " to " + str(new_pos)) if collision_debug else 0
				self.change_pos(new_pos)
			else:
				print("  Move failed") if collision_debug else 0

		elif collision_type == 2:
			print("  Ran into a wall at " + str(self.position)) if collision_debug else 0
			return_val = 0

		else:
			print("  Moving from " + str(self.position) + " to " + str(new_pos)) if collision_debug else 0
			self.change_pos(new_pos)

		self.update_pos()
		return return_val

	def change_pos(self, new_pos): # Changes position in both the moveables dict and the position variable
		del Moveable.moveables[tuple(self.position)]
		Moveable.moveables[tuple(new_pos)] = self
		self.position = new_pos

	def collides(self, pos=[-1,-1]): # Tells if that position collides with anything, returns the type of collision and colliders if any

		pos = self.position if pos == [-1,-1] else pos
		print("\nTesting collisions at " + str(pos)) if collision_debug else 0

		x = Moveable.moveables.get(tuple(pos), 0)
		if x:
			print("  Collision with Moveable") if collision_debug else 0
			return 1, x

		if (pos[0] > window_width-size) or (pos[0] < 0) or (pos[1] > window_height-size) or (pos[1] < 0):
			print("  Collision with Wall") if collision_debug else 0
			return 2, 0

		return 0, 0