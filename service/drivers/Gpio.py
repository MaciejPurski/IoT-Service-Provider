#import RPi.GPIO as GPIO


class Gpio:
	def __init__(self, config_str):
		if not isinstance(config_str, bytes):
			raise TypeError("Expected bytes type as gpio driver argument")

		desc = config_str.split()
		if len(desc) != 2:
			raise ValueError("Wrong config argument for gpios driver")

		self.nr = int(desc[0])
		#TODO sprawdzenie gpiosa

		self.direction = desc[1]

		if not self.direction in [b'IN', b'OUT']:
			raise ValueError("Expected IN or OUT in gpios driver config")

		#GPIO.setmode(GPIO.board)
		#GPIO.setup(self.nr,  GPIO.IN if self.direction == b'IN' else GPIO.OUT)

	def read(self):
		if self.direction == 'OUT':
			print('Attempt to read from output gpio device')
			return

		return True
			#return GPIO.input(self.nr) == GPIO.HIGH

	def write(self, val):
		if not isinstance(val, bool):
			raise TypeError("Expected boolean input argument")

		#GPIO.output(self.nr, GPIO.HIGH if val else GPIO.LOW)





