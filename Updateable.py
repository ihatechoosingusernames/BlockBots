from Config		import Config

cfg = Config()

update_debug = cfg.update_debug
update_count = cfg.update_count

class Updateable:
	updateables = []

	update_counter = 0
	update_time = 0.5

	def __init__(self):
		Updateable.updateables.append(self)

	def update_self(self):
		pass

	@staticmethod
	def update(dt, time):
		global update_count
		Updateable.update_counter += dt

		if Updateable.update_counter > Updateable.update_time:

			Updateable.update_counter = 0
			update_count += 1
			
			print("\n\nStarting Moveables update " + str(update_count) + " on " + str(len(Updateable.updateables)) + " updateables at time " + str(time) + " seconds") if update_debug else 0

			for u in Updateable.updateables:
				u.update_self(Updateable.update_time)

	def delete(self):
		Updateable.updateables.remove(self)