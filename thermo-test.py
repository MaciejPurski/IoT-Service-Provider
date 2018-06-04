from service.drivers.ThermoSensorW1 import *
import time

term = ThermoSensorW1('')

while True:
	print(term.read())
	time.sleep(2)