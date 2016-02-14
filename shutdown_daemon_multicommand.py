#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################ shutdown_daemon_multicommand ###################
# EXPERIENCED USERS ONLY !
# This script should be started during startup (/etc/rc.local as example)
# insert "/usr/bin/python /home/pi/shutdown_daemon_multicommand.py &" before "exit 0"
# This script sets the GPIO3 (Pin5) as a trigger to shut down, whenever it 
# recognizes a falling flank. 
# Physically, you can connect a switch between pin5 (GPIO3) and pin6 (GND)
# because of the internal circuit you dont need any other additional electronics.
# You can click several times on your button, triggering different defined actions
# WARNING: Make sure, that this script is executed with root-privilegues !
# otherwise it might be, that you get a runtime-Error because the callback
# can not be added...
#################################################################################

import RPi.GPIO as GPIO
import subprocess as sp
import time
import sys
from threading import Timer
import argparse

############################ USER AREA:###############################################################################
# Define how many seconds to wait for additional clicks until the action is triggered:
timeForFurtherClicks = 5            # seconds where the user has time to click the btn, maybe you have to enlarge this

# Define multiple actions for your button:
      #clickCount    command                        helptext                                timeToExit (bool)
actions = {1: ["sudo reboot", "Reset was pressed, Rebooting now. See you later!", True],
           2: ["sudo shutdown -h now", "Power-Switch was pressed, Shutdown now. See you later!", True],
           3: ["echo 'cool Function'", "This is only another cool function which does not shutdown...", False]}

# Define the "bouncetime" of your switch which is attached to pin 5 (GPIO3) in milliseconds
# Note: Firsttime running with your hardwaresetup use argument --debug
# (python /path/to/script/shutdown_daemon_multicommand.py --debug)
btime = 500   #ignore "bouncing" of switch for about xxx milliseconds

# END OF USER AREA####################################################################################################


timeToExit = False
clickCount = 0

def btn_press(GPIO_CHANNEL):               # callbackfunction for GPIO3
    global clickCount
    global shutdown_trigger
    clickCount += 1                        # increment count of clicks with any falling event
    if not shutdown_trigger.isAlive():     # it the trigger is not triggered
        shutdown_trigger.start()           # ... just aim :-)

def react_on_btn_press():                 # function which is called when the trigger is shooting
    global timeToExit
    global clickCount
    global actions
    if args.debug:
        print("You clicked {0} times, if this is wrong, review 'btime' variable in script".format(clickCount))
    if clickCount > len(actions):         # if you press the button a hundred time,
        clickCount = len(actions)      # only the action with the maximum "clicks" will be called

    action = actions.get(clickCount)
    if action is not None:
        command = action[0]
        infotext = action[1]
        command_shutsdown = action[2]
        if not timeToExit and command_shutsdown:
            timeToExit = True
            systemCall("wall '{0}'".format(infotext))
            if not args.debug:
                systemCall(command)
            else:
                print(command)
        else:
            #timeToExit = False
            global shutdown_trigger
            global timeForFurtherClicks
            clickCount = 0
            shutdown_trigger = None
            shutdown_trigger = Timer(timeForFurtherClicks, react_on_btn_press)
            systemCall("wall '{0}'".format(infotext))
            if not args.debug:
                systemCall(command)
            else:
                print(command)

def systemCall(command):
    return_value = sp.Popen(command, shell=True, stdout=sp.PIPE).stdout.read()
    return return_value

parser = argparse.ArgumentParser(description='*** Raspi Shutdown Daemon ***  by Matthias Laumer')
parser.add_argument('--debug', action='store_true', help='Dont run any command, just debug')
args = parser.parse_args()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)  #setup GPIO using Board numbering (pins, not GPIOs)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(5, GPIO.FALLING, callback=btn_press, bouncetime=btime)   #maybe you have to adjust bouncetime!

shutdown_trigger = Timer(timeForFurtherClicks, react_on_btn_press)  # define a trigger for an action

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
