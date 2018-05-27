#!/usr/bin/python3.6

classes_dict = {
	'DIGITAL_IN': 0x00,
	'DIGITAL_OUT': 0x01,
	'ANALOG_IN': 0x02,
	'ANALOG_OUT': 0x03}


class Service:

	def __init__(self, service_class, name, unit, min_value, max_value):
		self.is_input = False
		self.name = bytes(name, 'utf-8')
		if service_class not in classes_dict:
			raise TypeError('Wrong service_class type')

		self.service_class = classes_dict[service_class]

		if service_class in ['DIGITAL_IN', 'ANALOG_IN']:
			self.is_input = True
		else:
			self.is_input = False

		self.min_value = float(min_value)
		self.max_value = float(max_value)
		self.unit = bytes(unit, 'utf-8')
		self.id = 0

	def set_id(self, id):
		self.id = id

	def get_value(self):
		return 0.0

	def set_value(self):
		return True
