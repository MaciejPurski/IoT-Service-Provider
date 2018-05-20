#!/usr/bin/python3.6

class DeviceType:
	DIGITAL_IN = 0x00
	DIGITAL_OUT = 0x01
	ANALOG_IN = 0x02
	ANALOG_OUT = 0x03

class Device:
	def __init__(self, name, dev_type, min_value = 0.0, max_value = 1.0):
		self.