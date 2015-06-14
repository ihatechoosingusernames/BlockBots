from Programmable import Programmable
from Drawable import Drawable
from Config import Config

size = Config.get_val("size")
visualiser_debug = Config.get_val("visualiser_debug")

class Program_Visualiser(Programmable, Drawable):

	bit_masks = (7, 11, 13, 14)
	max_recursion = 10
	total_visualisers = 0

	def __init__(self, pos, instruction="(1,,w->2/a->3/s->4/d->5)(2,w,)(3,a,)(4,s,)(5,d,)", current_instruction=0, recursion=0):

		super(Program_Visualiser, self).__init__(instruction)
		Drawable.__init__(self, pos, (120, 10, 120), 1)

		Program_Visualiser.total_visualisers += 1

		self.recursion = recursion + 1
		self.children = []
		self.sensor_val = [0000]
		self.sensor_combination(0)

		if current_instruction:
			self.current_instruction = current_instruction.copy()
		else:
			super(Program_Visualiser, self).set_instruction(instruction)

		print("\nNew Program Visualiser\nPosition: " + str(pos) + "\nInstruction: " + instruction +  "\nCurrent Instruction: " + str(self.current_instruction) + "\nRecursion Level: " + str(recursion) + "\nTotal Visualisers: " + str(Program_Visualiser.total_visualisers)) if visualiser_debug else 0
		
		if recursion < Program_Visualiser.max_recursion:
			self.run()

	def run(self):
		if self.current_instruction[1] < 2: # If this instruction is the last one before transitioning
			old_instruction = self.current_instruction.copy() # Storing the current instruction
			old_position = self.position.copy()
			future_children = {} # Dict of potentially branching future children to be initialised at the end

			print("  Running transitions from current instruction: " + str(old_instruction)) if visualiser_debug else 0

			for i in range(16): #Trying the transitions with every possible combination of sensor inputs
				self.sensor_combination(i)
				self.run_instruction()

				print("    Result of transition " + str(i) + "\ton sensor reading:" + str(self.sensor_val) + " : " + str(self.current_instruction)) if visualiser_debug else 0

				if self.current_instruction[0] not in future_children and (self.position != old_position or self.current_instruction[0] != old_instruction[0]) : # If the new instruction's different, or the only one, make a new branch
					future_children[self.current_instruction[0]] = (self.position.copy(), self.instruction, self.current_instruction.copy(), self.recursion) # Instruction name used as key to avoid double ups
					print("    Added future child: " + self.current_instruction[0] + " = " + str((self.position.copy(), self.instruction, self.current_instruction.copy(), self.recursion))) if visualiser_debug else 0
				
				self.current_instruction = old_instruction.copy() # resetting back to the original instruction
				self.position = old_position.copy()

			for f in future_children: # Initialising future branches
				child = future_children[f]
				self.children.append(Program_Visualiser(child[0], child[1], child[2], child[3]))

		else: # Just running a normal instruction with no transitions
			print("  Running instruction: " + str(self.current_instruction)) if visualiser_debug else 0
			self.run_instruction()
			self.children.append(Program_Visualiser(self.position.copy(), self.instruction, self.current_instruction.copy(), self.recursion))

	def set_instruction(self, inst):
		super(Program_Visualiser, self).set_instruction(inst)
		self.delete()
		self.run()

	def move_up(self): # Defining movement functions called by Programmable to subvert them to our own nefarious purposes
		self.position[1] += size

	def move_down(self):
		self.position[1] -= size

	def move_left(self):
		self.position[0] -= size

	def move_right(self):
		self.position[0] += size

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
		return int(ret_val)

	def sensor_combination(self, num=0): # Sets the four sensor inputs to any possible combination, represented by the binary 0-16
		seq = bin(min(num, 15)).lstrip('-0b') # Binary representation of num
		for i in range(4 - len(seq)):
			seq = '0' + seq # Adding leading 0's
		self.sensor_val = seq # Setting it as the sensor values

	def delete(self):
		print("Program Visualiser deleted at: " + str(self.position) + "  With Children at:") if visualiser_debug else 0
		for c in self.children:
			print("  " + str(c.position)) if visualiser_debug else 0
			c.delete()
		Drawable.delete(self)