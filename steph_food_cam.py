# A basic Python Raspberry Pi project with twitter API integration and GPIO usage
# It requires that you have a Pi camera installed and enabled

# Originally written by Mike Haldas (Email: mike@cctvcamerapros.net, Twitter: @haldas, Google+: +Mike Haldas)
# Adapted by Coding for Good for use in UWCSEA
# We can be reached at foodpicturescoding@gmail.com on Email or @uwcfoodpictures on Twitter
# Detailed instructions for code and associated hardware available at

location = '' # put in the name of the location of your camera

IMG_WIDTH = "1280"
IMG_HEIGHT = "720"
IMG_NAME = "tweet-pic.jpg"
TIME = 2000

import time
import subprocess
import RPi.GPIO as GPIO
from twython import Twython
from gpiozero import Button,LED
from time import sleep

# sets up GPIO using Broadcom SOC channel numbering
GPIO.setmode(GPIO.BCM)
BUTTON = Button(12) # pin connected with the button
SYSTEM_READY = LED(7) # pin connected to the system ready (green) LED
SYSTEM_RUNNING = LED(13) # pin connected to the system running (red) LED

# your twitter app keys go here
apiKey = '' # put twitter API Key here
apiSecret = '' # put twitter API Secret here
accessToken = '' # twitter access token here
accessTokenSecret = '' # twitter access token secret

# this is the command to capture the image using pi camera
snapCommand = "raspistill -t "+str(TIME)+" -w " + IMG_WIDTH +  " -h " + IMG_HEIGHT + " -o " + IMG_NAME

api = Twython(apiKey,apiSecret,accessToken,accessTokenSecret)

SYSTEM_READY.on() # set ready LED to on
SYSTEM_RUNNING.off() # working LED to off
print("System Ready - push button to take picture and tweet.\n")

try:
	while True:
                while True:
                    if (BUTTON.is_pressed):
                        time.sleep(3)
                        break

                SYSTEM_READY.off() # signals program not ready
                SYSTEM_RUNNING.on() # signals program running
                print("Program running...\n")

                print("Capturing photo...\n")
                ret = subprocess.call(snapCommand, shell=True) # captures photo
                photo = open(IMG_NAME, 'rb')

                print("Uploading photo to twitter...\n") # uploads photo
                media_status = api.upload_media(media=photo)

                time_now = time.strftime("%H:%M:%S") # get current time
                date_now =  time.strftime("%d/%m/%Y") # get current date
                tweet_txt = 'This was captured at ' + location ' at ' + time_now + " on " + date_now + '.' # edit this message as you wish, bearing in mind the 140 character limit of twitter

                print("Posting tweet with picture...\n")
                api.update_status(media_ids=[media_status['media_id']], status=tweet_txt) # posts your message along with your photo as a tweet

                SYSTEM_READY.on() # signals program ready
                SYSTEM_RUNNING.off() # signals program not running
                print("System Ready - push button to take picture and tweet.\n")

except KeyboardInterrupt:
	SYSTEM_READY.off()
	GPIO.cleanup()

finally:
	GPIO.cleanup() # ensures a clean exit