from service.drivers.Gpio import *
import time

g = Gpio(b'40 OUT')
switch = Gpio(b'36 IN')

while True:
	pressed = switch.read()
	if pressed:
		g.write(True)
	else:
		g.write(False)
