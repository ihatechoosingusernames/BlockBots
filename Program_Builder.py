from Program_Visualiser import Program_Visualiser
from Drawable import Drawable
from pyglet.window import key
from Config import Config

builder_debug = Config.get_val("builder_debug")
size = Config.get_val("size")

class Program_Builder(Program_Visualiser):

	tool_mode = "action" # The current tool that the user will interact with

	def __init__(self, pos):
		super(Program_Builder, self).__init__(pos, instruction="(0,,->1)(1,,->1)")
		self.selected_cell = self # The currently selected cell (Each square filled in by the program visualiser is a cell)
		self.real_program = self.instruction # The actual resulting program of this program builder
		self.sense_cells = [] # A list of all the sense_cells for easy deletion

	def on_mouse_press(self, x, y, button, modifiers): # Event handlers
		pos = [int(x - x%size), int(y - y%size)]

		cell = self.cell_at_pos(pos)

		if cell:
			self.select_cell(cell)
			print("Cell clicked at position: " + str(pos) + " with tool: " + Program_Builder.tool_mode) if builder_debug else 0

			if Program_Builder.tool_mode == "sensing":
				self.sense_at_cell(self.selected_cell)

	def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
		pos = [int(x - x%size), int(y - y%size)]
		dist = [int((pos[0] - self.selected_cell.position[0])/size), int((pos[1] - self.selected_cell.position[1])/size)] # Finding the distance from the selected cell

		if Program_Builder.tool_mode == "action":

			inst_pos = self.real_program.find("(" + self.selected_cell.current_instruction[0]) + 1 # Finding the position of the current real_program
			inst_pos = self.real_program.find(",", inst_pos) + 1 + (self.selected_cell.current_instruction[1] if self.selected_cell.current_instruction[1] > -1 else 0)

			new_action_string = ("a" * abs(dist[0]) if dist[0] < 0 else "d" * dist[0]) + ("s" * abs(dist[1]) if dist[1] < 0 else "w" * dist[1]) # Working out the instructions needed to get to the dragged position

			i = 0
			for a in new_action_string: # Making sure that there aren't any double ups
				if self.real_program[inst_pos + i] == a:
					new_action_string = new_action_string[1:]
					i += 1

			self.instruction = self.real_program[0:inst_pos] + new_action_string + self.real_program[inst_pos:len(self.real_program)] # Plugging that shit in!

			super(Program_Builder, self).delete() # Get rid of the old visuals
			super(Program_Builder, self).__init__(pos=self.position, instruction=self.instruction) # Let's see what it looks like!
			print("Action: " + new_action_string + " added to instruction: " + self.selected_cell.current_instruction[0] + " with tool: " + Program_Builder.tool_mode + 
				"\nTotal program now: " + self.instruction) if builder_debug else 0


	def on_mouse_release(self, x, y, button, modifiers):
		pos = [int(x - x%size), int(y - y%size)]

		if Program_Builder.tool_mode == "action":
			self.real_program = self.instruction # Only change the real instruction on the final mouse release

		#elif Program_Builder.tool_mode == "sensing":
			# Finds whether it's over something it can chain together into a transition statement

	def on_key_press(self, symbol, modifiers):
		if symbol == key.Z:
			Program_Builder.tool_mode = "action"

		elif symbol == key.X:
			Program_Builder.tool_mode = "sensing"

		elif symbol == key.C:
			Program_Builder.tool_mode = "recursion"

	def cell_at_pos(self, pos): # Iterates through all cells to find any at a given position
		cells = [self]
		while len(cells) > 0:
			if cells[0].position == pos:
				return cells[0]
			else:
				cells.extend(cells[0].children)
				cells.pop(0)
		else:
			return 0

	def select_cell(self, cell):
		self.selected_cell.colour = (120, 10, 120)
		self.selected_cell = cell
		self.selected_cell.colour = (10,200,150)

	def sense_at_cell(self, cell):
		if not isinstance(self.selected_cell, Program_Builder.sense_cell):
			cell.children.extend([Program_Builder.sense_cell(cell, "w"), Program_Builder.sense_cell(cell, "a"), Program_Builder.sense_cell(cell, "s"), Program_Builder.sense_cell(cell, "d")])
			self.sense_cells.extend(cell.children)

	def delete(self):
		super(Program_Builder, self).delete()


	class sense_cell(Drawable): # A type of cell just for showing the sensor positions
		def __init__(self, parent, side):
			relative_pos = [0,0]
			if side == "w":
				relative_pos[1] = size
			elif side == "a":
				relative_pos[0] = -size
			elif side == "s":
				relative_pos[1] = -size
			elif side == "d":
				relative_pos[0] = size

			self.parent = parent

			if isinstance(parent, Program_Builder.sense_cell):
				super(Program_Builder.sense_cell, self).__init__(pos=[parent.position[0] + relative_pos[0], parent.position[1] + relative_pos[1]], col=(200,50,50))
				self.children = []
				self.sense_type = "!" + side
				print("New sense_cell at position: " + str(self.position) + " with sense type: " + self.sense_type) if builder_debug else 0

			else:
				super(Program_Builder.sense_cell, self).__init__(pos=[parent.position[0] + relative_pos[0], parent.position[1] + relative_pos[1]], col=(50,50,200))
				self.sense_type = side
				self.children = [Program_Builder.sense_cell(self, side)]
				print("New sense_cell at position: " + str(self.position) + " with sense type: " + self.sense_type) if builder_debug else 0

		def parent_program(self): # Returns the actual program visualiser cell it refers to
			if isinstance(self.parent, Program_Builder.sense_cell):
				return self.parent.parent
			return self.parent

		def delete(self):
			if len(self.children):
				self.children[0].delete()
			super(Program_Builder.sense_cell, self).delete()
			self.parent.children.remove(self)