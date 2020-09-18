from datetime import datetime
import time
import RPi.GPIO as GPIO

GPIO_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN,GPIO.IN)
second = 0
flag = True
judge = True

if __name__ == '__main__':
  while judge:
    try:
      while flag:
        if (GPIO.input(GPIO_PIN) == GPIO.HIGH):
          print("Yes")
          time.sleep(10)
          second += 10
        elif second >= 60:
          flag = False 
        else:
          print("No")
          time.sleep(10)
          second += 10
    except KeyboardInterrupt:
      judge = False
    finally:
      print("finish")
