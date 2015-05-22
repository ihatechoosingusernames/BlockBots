from Config import Config

cfg = Config()
parser_debug = cfg.parser_debug

class Instruction:
	def __init__(self, name, actions, transitions):
		self.name = name
		self.actions = actions
		self.transitions = transitions
		self.current_action = 0

	def execute(self, programmable):
		if self.current_action < len(self.actions):
			self.actions[self.current_action](programmable)
			self.current_action += 1
		else:
			self.current_action = 0
			for t in self.transitions:
				if t[0](programmable): return t[1]
		return self.name

	@staticmethod
	def parse(inst): # Takes a string representation of an instruction and turns it into a real one
		if not inst:
			return

		print("\nParsing: " + inst) if parser_debug else 0
		inst_parts = inst.split(",") # Splits instruction into its parts

		name_string = inst_parts[0] # Should be the Name of the instruction
		actions_string = inst_parts[1] # Should be the Actions part of the instruction
		transitions_string = inst_parts[2] # Should be the Transitions part of the instruction

		name = name_string  # The final name
		actions = []		# The final list of actions
		transitions = []	# The final list of transitions

		print("Instruction Parts:\n  Name: " + name_string + "\n  Actions: " + actions_string + "\n  Transitions: " + transitions_string) if parser_debug else 0

		if len(actions_string) > 0: # Only runs the action code if there are actions
			action_index = len(actions_string)

			print("  Number of Actions: " + str(action_index)) if parser_debug else 0

			for a in range(action_index):
				if  actions_string[a] == 'w':
					actions.append(lambda moveable : move_up())
				elif actions_string[a] == 's':
					actions.append(lambda moveable : move_down())
				elif actions_string[a] == 'a':
					actions.append(lambda moveable : move_left())
				elif actions_string[a] == 'd':
					actions.append(lambda moveable : move_right())

		if len(transitions_string) > 0:
			transition_strings = transitions_string.split("/") # Delimiting the transitions, format is: Transition_Rule_1->Destination/Transition_Rule_2->Destination etc.
			print("\nTransitions:") if parser_debug else 0

			for t in transition_strings: # Finding the transition that passes first
				print("  Transition Rule: " + t) if parser_debug else 0

				t_part = t.split("->")
				condition = t_part[0] # Splitting it into rule and destination
				destination = t_part[1] if len(t_part) > 1 else name

				operator_stack = ["|"] # This ensures the first value is considered if there is no operator before it
				condition_rule = lambda robot : 1

				for c in condition: # Parsing each character in a condition building a function from it
					print("    Parsing Character: " + c + "    Operator Stack: " + str(len(operator_stack))) if parser_debug else 0

					if (c == 'w') or (c == 'a') or (c == 's') or (c == 'd'):
						c_result = lambda robot : robot.sensor(c) # Find the initial value of that sensor reading
						print("    Condition Function: " + str(c_result)) if parser_debug else 0
						p = operator_stack.pop(len(operator_stack)-1) # Find the most recent operator for it

						if p == "!": # The "not" operator is used in conjunction with other operators, so the next is popped
							c_result = lambda robot : not c_result(robot)
							p = operator_stack.pop(len(operator_stack)-1)

						if p == "&":
							condition_rule = lambda robot : condition_rule(robot) and c_result(robot)
						elif p == "|":
							condition_rule = lambda robot : condition_rule(robot) or c_result(robot)

					else: # Add all operators to operator stack
						operator_stack.append(c)

					print("    Parsed  Character: " + c + "    Operator Stack: " + str(len(operator_stack))) if parser_debug else 0

				transitions.append((condition_rule, destination)) # Add the conditions and destinations as a tuple
		return Instruction(name, actions, transitions)