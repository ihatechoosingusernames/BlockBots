from Programmable import Programmable
from Drawable import Drawable
from Config import Config

size = Config.size
visualiser_debug = Config.visualiser_debug

class Program_Visualiser(Programmable, Drawable):

	max_recursion = 2
	combinations = [(0,0,0,0), (0,0,0,1), (0,0,1,0), (0,0,1,1), (0,1,0,0), (0,1,0,1), (0,1,1,0), (0,1,1,1), (1,0,0,0), (1,0,0,1), (1,0,1,0), (1,0,1,1), (1,1,0,0), (1,1,0,1), (1,1,1,0), (1,1,1,1)]

	def __init__(self, pos, instruction="(1,wwddss,w->2/!w->3)(2,aa,->3)(3,,)", current_instruction=0, recursion=0):
		if recursion > Program_Visualiser.max_recursion:
			return
		super(Program_Visualiser, self).__init__(instruction)
		Drawable.__init__(self, pos, (120, 10, 120), 1)

		self.current_position = pos
		self.recursion = recursion + 1
		self.squares = []
		self.children = []
		self.sensor_val = Program_Visualiser.combinations[0]

		if current_instruction:
			self.current_instruction = current_instruction
		else:
			super(Program_Visualiser, self).set_instruction(instruction)

		print("\nNew Program Visualiser\nPosition: " + str(pos) + "\nInstruction: " + instruction +  "\nCurrent Instruction: " + str(self.current_instruction) + "\nRecursion Level: " + str(recursion)) if visualiser_debug else 0
		self.run()
		print("New Program Visualiser finished\n") if visualiser_debug else 0

	def run(self):
		if self.current_instruction[1] == -1: #Runs the first iteration if necessary
			self.run_instruction()

		while self.current_instruction[1] > 1: # Running action code until the penultimate action
			self.run_instruction()
			print("  Running instruction: " + str(self.current_instruction)) if visualiser_debug else 0

		else: # When the transitions are going to be evaluated
			old_instruction = self.current_instruction.copy()
			old_position = self.current_position

			print("  Running transitions from current instruction: " + str(old_instruction)) if visualiser_debug else 0

			for i in range(len(Program_Visualiser.combinations)): #Trying the transitions with every possible combination of sensor inputs
				self.sensor_val = Program_Visualiser.combinations[i]
				self.run_instruction()
				future_children = {} # Dict of potentially branching future children, to be initialised at the end

				print("    Result of transition " + str(i) + " on sensor reading:" + str(self.sensor_val) + " : " + str(self.current_instruction)) if visualiser_debug else 0

				if self.current_instruction[0] != old_instruction[0]: # If the new instruction's different, make a new branch
					future_children[self.current_instruction[0]] = (self.current_position, self.instruction, self.current_instruction.copy(), self.recursion) # Instruction name used as key to avoid double ups
				
				self.current_instruction = old_instruction.copy()
				self.current_position = old_position

			for f in future_children: # Initialising future branches
				child = future_children[f]
				self.children.append(Program_Visualiser(child[0], child[1], child[2], child[3]))

	def set_instruction(self, inst):
		super(Program_Visualiser, self).set_instruction(inst)
		self.delete()
		self.run()

	def new_square(self):
		self.squares.append(Drawable(self.current_position, (120, 10, 10), 0))

	def move_up(self):
		self.current_position[1] += size
		self.new_square()

	def move_down(self):
		self.current_position[1] -= size
		self.new_square()

	def move_left(self):
		self.current_position[0] -= size
		self.new_square()

	def move_right(self):
		self.current_position[0] += size
		self.new_square()

	def sensor(self, side=""):
		ret_val = 0
		if side == "w":
			ret_val = self.sensor_val[0]
		elif side == "a":
			ret_val = self.sensor_val[1]
		elif side == "s":
			ret_val = self.sensor_val[2]
		elif side == "d":
			ret_val = self.sensor_val[3]

		print("      Sensor Called on: " + side + " Returning: " + str(ret_val)) if visualiser_debug else 0
		return ret_val

	def delete(self):
		for c in self.children:
			c.delete
		for s in self.squares:
			s.delete
		Drawable.delete(self)