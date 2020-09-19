from datetime import datetime
import time
import RPi.GPIO as GPIO

GPIO_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN,GPIO.IN)
second = 0

while True:
  try:
    if GPIO.input(GPIO_PIN) == GPIO.HIGH:
      print("high")
      time.sleep(1)
    else:
      print("low")
      time.sleep(1)
  except KeyboardInterrupt:
    break

    for i in range(5):
      array[i] = GPIO.input(GPIO_PIN)
      time.sleep(1)