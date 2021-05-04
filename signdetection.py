#!/usr/bin/python
# -*- coding: utf-8 -*-

from PCA9685 import PCA9685
import time

Dir = ['forward', 'backward']
pwm = PCA9685(0x40, debug=False)
pwm.setPWMFreq(50)


class MotorDriver:

    def __init__(self):
        self.PWMA = 0
        self.AIN1 = 1
        self.AIN2 = 2
        self.PWMB = 5
        self.BIN1 = 3
        self.BIN2 = 4

    def MotorRun(
        self,
        motor,
        index,
        speed,
        ):

        if speed > 100:
            return
        if motor == 0:
            pwm.setDutycycle(self.PWMA, speed)
            if index == Dir[0]:
                print '1'
                pwm.setLevel(self.AIN1, 0)
                pwm.setLevel(self.AIN2, 1)
            else:
                print '2'
                pwm.setLevel(self.AIN1, 1)
                pwm.setLevel(self.AIN2, 0)
        else:
            pwm.setDutycycle(self.PWMB, speed)
            if index == Dir[0]:
                print '3'
                pwm.setLevel(self.BIN1, 0)
                pwm.setLevel(self.BIN2, 1)
            else:
                print '4'
                pwm.setLevel(self.BIN1, 1)
                pwm.setLevel(self.BIN2, 0)

    def MotorStop(self, motor):
        if motor == 0:
            pwm.setDutycycle(self.PWMA, 0)
        else:
            pwm.setDutycycle(self.PWMB, 0)


from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
import subprocess
from PIL import Image
import sys
import time
import re

subscription_key = '27881906babf49308ac55dacf12b427d'
endpoint = 'https://stopsignproject.cognitiveservices.azure.com/'

computervision_client = ComputerVisionClient(endpoint,
        CognitiveServicesCredentials(subscription_key))

# testbench

Motor = MotorDriver()
stopSignDetected = 0
aprilTagDetected = 0
shapeDetected = 0

  # command to run servos !

Motor.MotorRun(0, 'forward', 45)
Motor.MotorRun(1, 'forward', 40)
img_counter = 0
while stopSignDetected == 0 and aprilTagDetected == 0 and shapeDetected == 0:

    # start photo stream !!!!!!

    command = \
        'fswebcam -r 1280x720 --no-banner --flip h,v ./{}.jpg '.format(img_counter)
    os.system(command)

    command1 = 'git add {}.jpg'.format(img_counter)
    command2 = "git commit -m '{}-uploaded!'".format(img_counter)
    command3 = 'git push'

    os.system(command1)
    os.system(command2)
    os.system(command3)

    # code to take github

    remote_image_url = \
        'https://raw.githubusercontent.com/Jtang6460/Robot2/main/{}.jpg'.format(img_counter)

    # Call API with remote image

    tags_result_remote = \
        computervision_client.tag_image(remote_image_url)

    # Print results with confidence score

    print 'Tags in the remote image: '
    if len(tags_result_remote.tags) == 0:
        print 'No tags detected.'
    else:
        imageData = ''
        for tag in tags_result_remote.tags:
            data = str("'{}' with confidence {:.2f}%".format(tag.name,
                       tag.confidence * 100))
            imageData = imageData + data

    object = imageData.find("'stop'")
    print(imageData)
    if object == -1:
        print 'stop sign not found!'
    else:
        confidence = re.sub('[^0-9]', '', imageData[object:object+50])
        Value = int(confidence)
        if Value > 5000:
            print 'Stop Sign found!'
            stopSignDetected = 1
    img_counter += 1

# stop servos

Motor.MotorStop(0)
Motor.MotorStop(1)
