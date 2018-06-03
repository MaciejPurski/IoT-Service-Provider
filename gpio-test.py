from service.drivers.Gpio import *
import time

g = Gpio(b'40 OUT')


while True:
    g.write(True)
    time.sleep(1)
    g.write(False)
    time.sleep(1)



