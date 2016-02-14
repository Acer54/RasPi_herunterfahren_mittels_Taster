#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################
# This script should be started during startup (/etc/rc.local as example)
# insert "/usr/bin/python /home/pi/shutdown_daemon.py" before "exit 0"
# This script sets the GPIO3 (Pin5) as a trigger to shut down, whenever it 
# recognizes a falling flank. 
# Physically, you can connect a switch between pin5 (GPIO3) and pin6 (GND)
# because of the internal circuit you dont need any other additional electronics.
# WARNING: Make sure, that this script is executet with root-privilegues !
# otherwise it might be, that you get a runtime-Error because the callback
# can not be added...
################################

import RPi.GPIO as GPIO
import subprocess as sp
import time
import sys
import argparse

timeToExit = False

def shutdown(GPIO_CHANNEL):
    global timeToExit
    if args.debug:
        print("shutdown called")
    if not timeToExit:
        if not args.debug:
            timeToExit = True
            systemCall("wall 'Power-Switch was pressed, Shutdown now. See you later!'")
            systemCall("sudo shutdown -h now")
        else:
            timeToExit = True
            print("shutdown now... (simulation only)")

def systemCall(command):
    return_value = sp.Popen(command, shell=True, stdout=sp.PIPE).stdout.read()
    return return_value

parser = argparse.ArgumentParser(description='*** Raspi Shutdown Daemon ***  by Matthias Laumer')
parser.add_argument('--debug', action='store_true', help='Dont run any command, just debug')
args = parser.parse_args()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)  #setup GPIO using Board numbering (pins, not GPIOs)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(5, GPIO.FALLING, callback=shutdown, bouncetime=500)

# wait ...
while True:
    try:
        time.sleep(1)
        if timeToExit:
            break
    except KeyboardInterrupt:  
        GPIO.remove_event_detect(5)
        GPIO.cleanup()       # clean up GPIO on CTRL+C exit 
        sys.exit(1)          # exit with status 1
GPIO.remove_event_detect(5)
GPIO.cleanup()       # clean up GPIO on CTRL+C exit 
sys.exit(0)          # exit with status 0
