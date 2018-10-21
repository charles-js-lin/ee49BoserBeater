from max6675 import MAX6675
from machine import Pin
from time import sleep
from board import A6, A14, A15

#When configured as open drain, a pin is pulled low (tied to GND) when set to 0, and open when set to 1.
#sck -> low
#cs -> high
#so -> low

so = Pin(A14, mode=Pin.IN)
cs = Pin(A15, mode=Pin.OUT)
sck = Pin(A6, mode=Pin.OUT)

thermo = MAX6675(sck, cs, so)

for _ in range(10):
	print(thermo.read())
	sleep(1)