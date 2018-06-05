from service.drivers.OutputPWM import *
import time

g = OutputPWM(b'32 60')

try:
	while True:
		for i in range(0, 100):
			g.write(i)
			time.sleep(0.01)

		for i in range(100, 0, -1):
			g.write(i)
			time.sleep(0.01)
except KeyboardInterrupt:
	g.close()






