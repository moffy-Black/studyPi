from datetime import datetime
import time
import RPi.GPIO as GPIO
import pyrebase
import json

with open("./firebaseConfig.json") as f:
    firebaseConfig = json.loads(f.read())
firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()
INTERVAL = 1
SLEEPTIME = 0
GPIO_PIN = 18
SENSOR_COUNT = 0
SNESOR_DISCOUNT = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN,GPIO.IN)

if __name__ == '__main__':
  try:
    
    while True:
      if(GPIO.input(GPIO_PIN) == GPIO.HIGH):
        print(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
        now = datetime.now()
        SENSOR_COUNT += SNESOR_DISCOUNT + 1
        SNESOR_DISCOUNT = 0
        SLEEPTIME = 0
        time.sleep(INTERVAL)
      else:
        SNESOR_DISCOUNT += 1
        SLEEPTIME += 1
        print(SLEEPTIME)
        time.sleep(INTERVAL)
        if SLEEPTIME >= 20:
          break
  except KeyboardInterrupt:
    pass
    
  finally:
    s = SENSOR_COUNT
    date = now.strftime('%Y-%m-%d')
    term = s // 60
    time = now.strftime('%H:%M')
    push_date = {
      "date": date,
      "term": term,
      "time": time
    }
    records = db.child("records").child("bz5pWlLkslU1TM7YReke8OSuxSM2").push(push_date)
    GPIO.cleanup()
    print("GPIO clean完了")
