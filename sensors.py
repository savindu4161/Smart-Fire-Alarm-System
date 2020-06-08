#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import subprocess
#GPIO SETUP
water = 21
smoke = 20
fire = 14
push = 10
alarm_active = True
push_status = True
GPIO.setmode(GPIO.BCM)
GPIO.setup(push, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(water, GPIO.IN)
GPIO.setup(smoke, GPIO.IN)
GPIO.setup(fire, GPIO.IN)


def check_button_push(push_status, alarm_active):
        push_detected = GPIO.input(push)
        if push_detected == 1:
                print('push detected')
                push_status = True
                alarm_active = not alarm_active
        else:
                print('push not detected')

        if push_status and alarm_active:
                subprocess.check_output('mpg123 sounds/active.mp3', shell=True)
                push_status = False

        if push_status and not alarm_active:
                subprocess.check_output('mpg123 sounds/inactive.mp3', shell=True)
                push_status = False
                return push_status, alarm_active

 
# infinite loop
while True:
	(push_status, alarm_active) = check_button_push(push_status, alarm_active)

	water_detected = GPIO.input(water)
	if water_detected == 0 and alarm_active:
		print('water detected')
		subprocess.check_output('mpg123 sounds/water_detected.mp3', shell=True)
		subprocess.check_output('mpg123 sounds/alarm.mp3', shell=True)
	else:
		print('no water detected')

	(push_status, alarm_active) = check_button_push(push_status, alarm_active)
	fire_detected = GPIO.input(fire)
	if fire_detected == 1 and alarm_active:
                print('fire detected')
                subprocess.check_output('mpg123 sounds/fire_detected.mp3', shell=True)
                subprocess.check_output('mpg123 sounds/alarm.mp3', shell=True)
        else:
                print('no fire detected')

	(push_status, alarm_active) = check_button_push(push_status, alarm_active)

        smoke_detected = GPIO.input(smoke)
        if smoke_detected == 0 and alarm_active:
                print('smoke detected')
                subprocess.check_output('mpg123 sounds/smoke_detected.mp3', shell=True)
                subprocess.check_output('mpg123 sounds/alarm.mp3', shell=True)
        else:
                print('no smoke detected')
        time.sleep(2)
