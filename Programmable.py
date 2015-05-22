from Instruction import Instruction

class Programmable:
	def __init__(self, program={}):
		self.program = program
		self.current_instruction = program.get("0", 0)

	def program(self, p):
		self.program = p

	def parse_program(self, p):
		self.program.clear()

		del_p = p.split("(")
		for i in del_p:
			inst = Instruction.parse(i.split(")")[0])
			if inst:
				self.program[inst.name] = inst

	def run(self):
		if self.current_instruction:
			self.current_instruction = program[self.current_instruction.execute(self)]