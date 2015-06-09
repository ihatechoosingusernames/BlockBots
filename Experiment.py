num = 0

seq = bin(min(num, 15)).lstrip('-0b')
for i in range(4 - len(seq)):
	seq = '0' + seq

print(" : " + seq)