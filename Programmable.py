from Config import Config

cfg = Config()
parser_debug = cfg.parser_debug
size = cfg.size

class Programmable:
	def __init__(self, instruction=""):
		self.instruction = instruction # Not using set_instruction due to it being overridden by subclasses
		self.current_instruction = [instruction.split("(")[1].split(",")[0], -1]

	def set_instruction(self, inst):
		self.instruction = inst
		self.current_instruction = [inst.split("(")[1].split(",")[0], -1] # Sets current instruction to first instruction name

	def sensor(self, side=""):
		print("    Sensor called on side: " + side) if parser_debug else 0

		if side == "w":
			vector = [self.position[0], self.position[1] + size]
		elif side == "a":
			vector = [self.position[0] - size, self.position[1]]
		elif side == "s":
			vector = [self.position[0], self.position[1] - size]
		elif side == "d":
			vector = [self.position[0] + size, self.position[1]]

		return (self.collides(vector)[0] == 1)

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