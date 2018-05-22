#!/usr/bin/python3.6

import configparser
from collections import namedtuple

class Config:
	Device_namedtuple = namedtuple('DEVICE', 'server_ip server_port device_id server_key client_key')
	Service_namedtuple = namedtuple('SERVICE', 'name service_class min_value max_value unit')

	def __init__(self, file_name):
		self.config = configparser.ConfigParser()
		self.config.read(file_name)

	def parse_device_config(self):
		device_tuple = self.section_to_tuple('DEVICE', Config.Device_namedtuple)
		if device_tuple is None:
			raise ValueError('Missing DEVICE section in config file')
		
		return device_tuple

	def parse_services_config(self):
		services_list = []

		for i in range(0, 255):
			t = self.section_to_tuple('SERVICE-' + str(i), Config.Service_namedtuple)
			if t is None:
				break
			services_list.append(t)

		return services_list


	def section_to_tuple(self, section, section_tuple):
		if section not in self.config:
			return None

		fields_list = []

		for field in section_tuple._fields:
			if field not in self.config[section]:
				raise ValueError('Missing field {} in device config'.format(field))

			fields_list.append(self.config[section][field])

		return section_tuple(*fields_list)


