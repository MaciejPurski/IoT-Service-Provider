#!/usr/bin/python3.6

from communication.ProtocolLayer import *
from service.ConfigParser import *
from service.Service import Service
import sys
import time
import signal

if len(sys.argv) != 2:
	print("Expected one argument")
	sys.exit(1)

config = Config(sys.argv[1])

device_namedtuple = config.parse_device_config()

services_tuples_list = config.parse_services_config()

services_list = [Service(*t) for t in services_tuples_list]

protocol = Protocol(*device_namedtuple)


def signal_handler(signal, frame):
	print('Pending exit...')
	protocol.pend_exit()


signal.signal(signal.SIGINT, signal_handler)

try:
	protocol.register(services_list)

	while True:
		time.sleep(4)
		protocol.transmission(services_list)
except RuntimeError as e:
	sys.stderr.write('Runtime error: {} exiting program'.format(e))
	exit(1)
