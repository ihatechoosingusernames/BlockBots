from Config		import Config

cfg = Config()

update_debug = cfg.update_debug
update_count = cfg.update_count

class Updateable:
	updateables = []

	update_counter = 0
	update_time = 0.5
	pause = 0

	def __init__(self):
		Updateable.updateables.append(self)

	def update_self(self):
		return 0

	@staticmethod
	def update(dt, time):
		if not Updateable.pause:
			return 0

		global update_count
		Updateable.update_counter += dt

		score_update = 0

		if Updateable.update_counter > Updateable.update_time:

			Updateable.update_counter = 0
			update_count += 1
			
			print("\n\nStarting Moveables update " + str(update_count) + " on " + str(len(Updateable.updateables)) + " updateables at time " + str(time) + " seconds") if update_debug else 0

			for u in Updateable.updateables:
				score_delta = u.update_self(Updateable.update_time)

				if type(score_delta) is int:
					score_update += score_delta

			print("\nFinishing Moveables update " + str(update_count) + " with score " + str(score_update)) if update_debug else 0

		return score_update

	@staticmethod
	def pause():
		Updateable.pause = 0 if Updateable.pause else 1

	def delete(self):
		Updateable.updateables.remove(self)