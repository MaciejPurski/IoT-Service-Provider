#!/usr/bin/python3.6

from ProtocolLayer import *
from ConfigParser import *
from Service import Service
import sys

if len(sys.argv) != 2:
	print("Expected one argument")
	sys.exit(1)

config = Config(sys.argv[1])

device_namedtuple = config.parse_device_config()

services_tuples_list = config.parse_services_config()

services_list = [Service(*t) for t in services_tuples_list]


protocol = Protocol(*device_namedtuple)

protocol.register(services_list)