#import w1thermsensor

# requires w1_gpio and w1_therm kernel modules
#  thermosensor must be connected to GPIO4

class ThermoSensorW1:
	def __init__(self, config_str):
		pass
		# self.sensor = w1thermsensor.W1ThermSensor()


	def read(self):
		# return self.sensor.get_temperature()
		return 0
