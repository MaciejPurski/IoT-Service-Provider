#!/usr/bin/python3.6

from ProtocolLayer import *
from ConfigParser import *
from Service import Service
import sys
import time

if len(sys.argv) != 2:
	print("Expected one argument")
	sys.exit(1)

config = Config(sys.argv[1])

device_namedtuple = config.parse_device_config()

services_tuples_list = config.parse_services_config()

services_list = [Service(*t) for t in services_tuples_list]


protocol = Protocol(*device_namedtuple)

protocol.register(services_list)

while True:
	time.sleep(3)
	protocol.transmission(services_list)