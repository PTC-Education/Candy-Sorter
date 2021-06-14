import time
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
import board
import adafruit_tcs34725
i2c = board.I2C()
sensor = adafruit_tcs34725.TCS34725(i2c)

import requests
import json

def GetPrediction(RGB,L,T):
    url = "https://pp-2101111403aw.portal.ptc.io/Thingworx/Things/MM_CandyLiveData/Services/ColorPredictionService"
    appKey = '156f0901-bed5-41fb-a2bd-34b5580ecf38'
    payload={'Rin':RGB[0],
             'Gin':RGB[1],
             'Bin':RGB[2],
             'Lin':L,
             'Tin':T}
    headers = {
      'appKey': appKey,
      'Content-Type': 'application/json',
      'accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    
    result = response.json()['rows'][0]['result'].split("result=")[1].split(",")[0]
    
    print(result)
    return result

def LogData(RGB,L,T,color):
    url = "https://pp-2101111403aw.portal.ptc.io/Thingworx/Things/SkittleTraining1/Services/AddCandyData"
    appKey = '156f0901-bed5-41fb-a2bd-34b5580ecf38'
    payload={'inR':RGB[0],
             'inG':RGB[1],
             'inB':RGB[2],
             'inL':L,
             'inT':T,
             'inColor':color}
    headers = {
      'appKey': appKey,
      'Content-Type': 'application/json',
      'accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

    print(response.status_code)

def MotorColorPos(argument):
    switcher = {
        'orange': 120,
        'red': 98,
        'yellow': 75,
        'green': 52,
        'purple': 30
    }
    return switcher.get(argument, "nothing")

def Shake():
    for i in range(5):
        kit.servo[0].angle = 15
        time.sleep(0.05)
        kit.servo[0].angle = 100
        time.sleep(0.05)
  
# Driver program
while(True):

    kit.servo[0].angle = 180 # feeder disk position
    time.sleep(0.5)
    kit.servo[0].angle = 80 # color sensor position
    time.sleep(0.5)

    print('Color: ({0}, {1}, {2})'.format(*sensor.color_rgb_bytes))
    print('Temperature: {0}K'.format(sensor.color_temperature))
    print('Lux: {0}'.format(sensor.lux))
    RGB = sensor.color_rgb_bytes
    L = sensor.lux
    T = sensor.color_temperature
    
    color = GetPrediction(RGB,L,T)
    
    if MotorColorPos(color)=="nothing":
        print("no skittle - time to shake!")
        LogData(RGB,L,T,color)
        Shake()
    else:
        LogData(RGB,L,T,color)
        kit.servo[1].angle = MotorColorPos(color)
        time.sleep(0.5)
        kit.servo[0].angle = 15 # Ramp position
        time.sleep(0.5)
