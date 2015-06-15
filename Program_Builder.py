from Program_Visualiser import Program_Visualiser
from pyglet.window import key
from Config import Config

builder_debug = Config.get_val("builder_debug")
size = Config.get_val("size")

class Program_Builder(Program_Visualiser):

	tool_mode = "action" # The current tool that the user will interact with

	def __init__(self, pos):
		super(Program_Builder, self).__init__(pos, instruction="(0,,->0)")
		self.selected_cell = self

	def on_mouse_press(self, x, y, button, modifiers): # Event handlers 
		pos = [int(x - x%size), int(y - y%size)]

		cell = self.cell_at_pos(pos)

		if cell:
			self.select_cell(cell)
			print("Cell clicked at position: " + str(pos) + " with tool: " + Program_Builder.tool_mode) if builder_debug else 0

	def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
		pos = [int(x - x%size), int(y - y%size)]
		dist = [int(dx - dx%size), int(dy - dy%size)]

		if Program_Builder.tool_mode == "action":

			inst_pos = self.instruction.find("(" + self.selected_cell.current_instruction[0]) + 1 # Finding the position of the current instruction
			inst_pos = self.instruction.find(",", inst_pos) + 1 + (self.selected_cell.current_instruction[1] if self.selected_cell.current_instruction[1] > -1 else 0)

			new_action_string = ("a" * abs(dist[0]) if dist[0] < 0 else "d" * dist[0]) + ("s" * abs(dist[1]) if dist[1] < 0 else "w" * dist[1]) # Working out the instructions needed to get to the dragged position

			self.instruction = self.instruction[0:inst_pos] + new_action_string + self.instruction[inst_pos:len(self.instruction)] # Plugging that shit in!

			super(Program_Builder, self).__init__(pos=self.position, instruction=self.instruction) # Lets see what it looks like!

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