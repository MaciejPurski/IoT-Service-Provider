#!/usr/bin/python3.6

classes_dict = {
	'DIGITAL_IN' : 0x00,
	'DIGITAL_OUT' : 0x01,
	'ANALOG_IN' : 0x02,
	'ANALOG_OUT' : 0x03 }

class Service:
	def __init__(self, name, service_class, min_value, max_value, unit):
		# TODO values check
		self.name = name 
		self.service_class = classes_dict[service_class]
		self.min_value = float(min_value)
		self.max_value = float(max_value)
		self.unit = unit

	def set_id(self, id):
		self.id = id

	def get_value(self):
		return 0.0

	def set_value(self):
		pass

