from service.drivers.OutputPWM import *
import time

g = OutputPWM(b'32 60')

while True:
	g.write(0)
	time.sleep(1)
	g.write(50)
	time.sleep(1)
	g.write(100)
	time.sleep(1)
	g.write(50)
	time.sleep(1)



