import time
import RPi.GPIO as GPIO


# requires pigpiod running in the background

class OutputPWM:
	def __init__(self, config_str):
		args = config_str.split()

		gpio_nr = int(args[0])
		if gpio_nr > 53:
			raise ValueError('Non existing gpio nr in PWMOutput module')

		frequency = int(args[1])
		GPIO.setmode(GPIO.BOARD)

		GPIO.setup(gpio_nr, GPIO.OUT)
		self.pwm = GPIO.PWM(gpio_nr, frequency)
		self.pwm.start(0)

	def write(self, percentage):
		if percentage < 0 or percentage > 100.0:
			raise RuntimeWarning('Can\'t set value {} for PWM output module'.format(percentage))

		self.pwm.ChangeDutyCycle(int(percentage))

	def close(self):
		self.pwm.stop()
		GPIO.cleanup()
