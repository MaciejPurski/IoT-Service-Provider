import RPi.GPIO as GPIO

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

		GPIO.setmode(GPIO.BOARD)
		if self.direction == b'IN':
			GPIO.setup(self.nr, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		else:
			GPIO.setup(self.nr, GPIO.OUT)

	def read(self):
		if self.direction == 'OUT':
			raise ValueError('Attempt to read from output gpio device')
			return

		return 0.0 if GPIO.input(self.nr) == GPIO.LOW else 1.0

	def write(self, val):
		GPIO.output(self.nr, GPIO.LOW if val == 0.0 else GPIO.HIGH)

	def close(self):
		GPIO.cleanup()





