import serial
import time
from lewansoul_lx16a_controller import ServoController

#logging.basicConfig(level=logging.DEBUG)

s = serial.Serial('/dev/usb/hiddev0', 9600, timeout=2)
c = ServoController(s, timeout=5)

print(c.get_battery_voltage())

servo1_id = 3
servo2_id = 5

print(c.get_positions([servo1_id, servo2_id]))

c.move({servo1_id: 1000, servo2_id: 500}, time=300)
time.sleep(0.3)
c.move({servo1_id: 800, servo2_id: 500}, time=2000)
time.sleep(2)
c.unload([servo1_id, servo2_id])
time.sleep(0.1) # important not to close serial connection immediately