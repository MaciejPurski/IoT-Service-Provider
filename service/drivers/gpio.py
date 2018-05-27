

class Gpio:
	def __init__(self, config_str):
		if not isinstance(config_str, bytes):
			raise TypeError("Expected bytes type as gpio driver argument")

		desc = config_str.split()
		if len(desc) != 2:
			raise ValueError("Wrong config argument for gpios driver")

		self.gpio_nr = int(desc[0])
		#TODO sprawdzenie gpiosa

		self.gpio_direction = desc[1]

		if not self.gpio_direction in [b'IN', b'OUT']:
			raise ValueError("Expected IN or OUT in gpios driver config")



