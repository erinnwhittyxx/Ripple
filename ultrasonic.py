# References:
#
# Community.wia.io. 2018. Build a smart mailbox with a Sigfox and Pycom. 
# [online] Available at: <https://community.wia.io/d/42-build-a-smart-mailbox-with-a-sigfox-and-pycom> [Accessed 27 April 2022].
#

from machine import Pin, Timer
import pycom
import time

def calibration(chrono, trigger, echo, led = False):
    if led:
        pycom.rgbled(0x7f0000) # red
    prev_distance = 0
    distance = getDistance(chrono, trigger, echo)
    print("calibration distance is {}".format(distance))
    count = 0
    while True:
        prev_distance = distance
        distance = getDistance(chrono, trigger, echo)
        while prev_distance == distance:
            count+=1
            print("count: {}".format(count))
            if count > 5:
                if led:
                    pycom.rgbled(0x007f00) # green
                    time.sleep(1.5)
                    pycom.rgbled(0) # off
                return distance
            time.sleep(1)
            prev_distance = distance
            distance = getDistance(chrono, trigger, echo)
        else:
            count = 0

def getDistance(chrono, trigger, echo):
    chrono.reset()
    trigger(1)
    time.sleep_us(10)
    trigger(0)

    while echo() == 0:
        pass
    chrono.start()

    while echo() == 1:
        pass
    chrono.stop()

    distance = chrono.read_us() / 58.0
    if distance > 400:
        return -1
    else:
        return int(distance)
