from Config		import Config

update_debug = Config.get_val("update_debug")
update_count = Config.get_val("update_count")

class Updateable:
	updateables = []

	update_counter = 0
	update_time = 0.5

	def __init__(self):
		Updateable.updateables.append(self)

	def update_self(self):
		return 0

	@staticmethod
	def update(dt, time):
		global update_count
		Updateable.update_counter += dt

		if Updateable.update_counter > Updateable.update_time:
			score = 0

			Updateable.update_counter = 0
			update_count += 1
			
			print("\n\nStarting Moveables update " + str(update_count) + " on " + str(len(Updateable.updateables)) + " updateables at time " + str(time) + " seconds") if update_debug else 0

			for u in Updateable.updateables:
				tentative_score = u.update_self(Updateable.update_time)
				score += tentative_score if type(tentative_score) is int else 0

			return score
		return 0

	def delete(self):
		Updateable.updateables.remove(self)