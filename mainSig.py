from network import Sigfox
import socket
from machine import Pin, Timer
import ultrasonic
from onewire import DS18X20
from onewire import OneWire
import time
import struct


# init Sigfox for RCZ1 (Europe)
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)

# create a Sigfox socket
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)

# make the socket blocking
s.setblocking(True)

# configure it as uplink only
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)

echo = Pin(Pin.exp_board.G7, mode=Pin.IN)
trigger = Pin(Pin.exp_board.G8, mode=Pin.OUT)
trigger(0)

chrono = Timer.Chrono()

pinUsed = OneWire(Pin('P10'))
temp = DS18X20(pinUsed)

dummydata = 10
mult = 1

while True:
    temp.start_conversion()
    time.sleep(1)
    
    #messageBytes=bytes((temp.read_temp_async() & 0xff, ((temp.read_temp_async() >> 8) & 0xff)))
    #s.send(messageBytes)

    if dummydata >30:
        mult = -1
    elif dummydata<10:
        mult = 1

    dummydata+=mult*2

    s.send(struct.pack("<i",  dummydata))

    print("temperature: {}".format(temp.read_temp_async()))
    time.sleep(2)
    distance = ultrasonic.getDistance(chrono, trigger, echo)
    print("tide height: {}".format(distance))
    time.sleep(2)
    