#!/usr/bin/python
import os
import signal
import subprocess
import RPi.GPIO as GPIO
import time

cmd = 'sudo arecord -v --format=S16_LE --rate=48000 --channels=1 -t wav | aplay -v --format=S16_LE --rate=48000  -D plug:stereoonly'
mic_off = False
mic_toggle = False

#GPIO SETUP
push = 9
status_led = 11
push_status = True
GPIO.setmode(GPIO.BCM)
GPIO.setup(push, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(status_led, GPIO.OUT)


def check_button_push(push_status, mic_off):
        push_detected = GPIO.input(push)
        if push_detected == 1:
                print 'push detected'
                push_status = True
		mic_off = not mic_off
        else:
                print 'push not detected'

        if push_status and mic_off:
                print 'LED on'
		GPIO.output(status_led, GPIO.HIGH)
                push_status = False

        if push_status and not mic_off:
                print 'LED off'
		GPIO.output(status_led, GPIO.LOW)
                push_status = False

        return push_status, mic_off

while True:
	(push_status, mic_off) = check_button_push(push_status, mic_off)
	if mic_off and not mic_toggle:
		print 'mic ON'
		pro = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                       shell=True, preexec_fn=os.setsid)
		mic_toggle = True
	if not mic_off and mic_toggle:
		print 'mic OFF'
		os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
		mic_toggle = False
	time.sleep(1)
