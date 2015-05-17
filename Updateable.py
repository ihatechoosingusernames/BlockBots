from Config		import Config

class Updateable:
	updateables = []

	update_counter = 0
	update_time = 1

	def __init__(self):
		Updateable.updateables.append(self)

	def update_self(self):
		pass

	@staticmethod
	def update(dt, time):
		Updateable.update_counter += dt

		if Updateable.update_counter > Updateable.update_time:

			global update_count
			update_count += 1
			print("\n\nStarting Moveables update " + str(update_count) + " at time " + str(time) + " seconds") if update_debug else 0

			Updateable.update_counter = 0
			for u in Updateable.updateables:
				u.update_self(Updateable.update_time)

	def delete(self):
		Updateable.updateables.remove(self)