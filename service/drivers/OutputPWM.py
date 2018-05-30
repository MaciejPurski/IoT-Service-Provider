import time
#import pigpio
#import wavePWM


# requires pigpiod running in the background


class OutputPWM:
	def __init__(self, config_str):
		self.gpio_nr = int(config_str)
		if self.gpio_nr > 53:
			raise ValueError('Non existing gpio nr in PWMOutput module')

		#self.pi = pigpio.pi()
		#if not self.pi.connected:
			#exit(0)
		#self.pwm = wavePWM.PWM(self.pi)


	def write(self, percentage):
		if percentage < 0 or percentage > 100.0:
			raise RuntimeWarning('Can\'t set value {} for PWM output module'.format(percentage))

		#self.pwm.set_pulse_start_in_fraction(self.gpio_nr, 0)
		#self.pwm.set_pulse_length_in_fraction(pin, percentage / 100.0)
		#self.pwm.update()


	def close(self):
		pass
		#self.pwm.cancel()
		#self.pi.stop()

