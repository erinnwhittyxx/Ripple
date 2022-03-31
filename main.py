import time
import network
import pycom
import ultrasonic
from onewire import DS18X20
from onewire import OneWire
from machine import Pin, Timer

pycom.heartbeat(False)

echo = Pin(Pin.exp_board.G7, mode=Pin.IN)
trigger = Pin(Pin.exp_board.G8, mode=Pin.OUT)
trigger(0)

chrono = Timer.Chrono()

# api_key = 'PCIO3UGHDNAF3GT0'
# field_name = 'field1'
# field_value = 22

wlan = network.WLAN(mode=network.WLAN.STA)
wlan.ifconfig(config = "dhcp")
wlan.scan()
wlan.connect("VM3476012", auth=(network.WLAN.WPA2, "ap4Bjyzja6mt"))

while not wlan.isconnected(): 
    print("Connecting...")
    time.sleep(1)
print("WiFi connected successfully")
print("IP address " + str(wlan.ifconfig()[0]) + ", Port " + str(100))

# host = 'api.thingspeak.com'
# path = '/update?api_key=' + api_key + '&' + field_name + '=' + str(field_value)

pinUsed = OneWire(Pin('P10'))
temp = DS18X20(pinUsed)


while True:
    temp.start_conversion()
    time.sleep(2)
    
    print("temperature: {}".format(temp.read_temp_async()))
    time.sleep(2)
    distance = ultrasonic.getDistance(chrono, trigger, echo)
    print("tide height: {}".format(distance))
    