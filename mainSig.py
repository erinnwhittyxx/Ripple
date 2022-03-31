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

while True:
    temp.start_conversion()
    time.sleep(1)

    print("temperature: {}".format(temp.read_temp_async()))
    time.sleep(2)
    distance = ultrasonic.getDistance(chrono, trigger, echo)
    print("tide height: {}".format(distance))
    time.sleep(2)

    distToFloat = float(distance)

    tempBytes=bytearray(struct.pack("f", temp.read_temp_async())) #Converts float into bytearray
    tempBytes += struct.pack("f", distToFloat)
    s.send(tempBytes) #Sends message to SigFox

    print(tempBytes)