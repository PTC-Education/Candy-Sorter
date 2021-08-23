import time
import requests
import json

from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
import board
import adafruit_tcs34725
i2c = board.I2C()
sensor = adafruit_tcs34725.TCS34725(i2c)

## Set ThingWorx Parameters
baseURL = "https://pp-2101111403aw.portal.ptc.io/Thingworx/Things/CandySorter/Services/"
appKey = '156f0901-bed5-41fb-a2bd-34b5580ecf38'

## Set Motor Numbers
feederServo = 6
rampServo = 7

## Set Ramp Motor Positions
def MotorColorPos(argument):
    switcher = {
        'orange': 120,
        'red': 98,
        'yellow': 75,
        'green': 52,
        'purple': 30
    }
    return switcher.get(argument, "nothing")

## Set Feeder Disk Motor Positions
hopperPos = 160
sensorPos = 90
rampPos = 20

def FeederServoTest():
    kit.servo[feederServo].angle = hopperPos
    time.sleep(1)
    kit.servo[feederServo].angle = sensorPos
    time.sleep(1)
    kit.servo[feederServo].angle = rampPos
    time.sleep(1)

def MotorTest():
    kit.servo[rampServo].angle = MotorColorPos('orange')
    time.sleep(1)
    kit.servo[rampServo].angle = MotorColorPos('red')
    time.sleep(1)
    kit.servo[rampServo].angle = MotorColorPos('yellow')
    time.sleep(1)
    kit.servo[rampServo].angle = MotorColorPos('green')
    time.sleep(1)
    kit.servo[rampServo].angle = MotorColorPos('purple')
    time.sleep(1)
    FeederServoTest()
    kit.servo[feederServo].angle = 90
    kit.servo[rampServo].angle = 90


def GetPrediction(RGB,L,T):
    twService = "ColorPredictionService"
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

    response = requests.request("POST", baseURL+twService, headers=headers, data=json.dumps(payload))
    
    result = response.json()['rows'][0]['result'].split("result=")[1].split(",")[0]
    
    print(result)
    return result

def LogData(RGB,L,T,color):
    twService = "AddCandyData"
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

    response = requests.request("POST", baseURL+twService, headers=headers, data=json.dumps(payload))

    print(response.status_code)

def Shake():
    for i in range(5):
        kit.servo[feederServo].angle = 15
        time.sleep(0.05)
        kit.servo[feederServo].angle = 100
        time.sleep(0.05)
  
# Automatic sorting program
def autoMain():
    while(True):
        kit.servo[feederServo].angle = hopperPos # candy hopper position
        time.sleep(0.5)
        kit.servo[feederServo].angle = sensorPos # color sensor position
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
            kit.servo[rampServo].angle = MotorColorPos(color)
            time.sleep(0.5)
            kit.servo[feederServo].angle = rampPos # Ramp position
            time.sleep(0.5)

# Training program
def trainingMain():
    while(True):
        kit.servo[feederServo].angle = hopperPos # hopper position
        time.sleep(0.5)
        kit.servo[feederServo].angle = sensorPos # color sensor position
        time.sleep(0.5)

        print('Color: ({0}, {1}, {2})'.format(*sensor.color_rgb_bytes))
        print('Temperature: {0}K'.format(sensor.color_temperature))
        print('Lux: {0}'.format(sensor.lux))
        RGB = sensor.color_rgb_bytes
        L = sensor.lux
        T = sensor.color_temperature    

        color = input("Enter candy color:")

        if MotorColorPos(color)=="nothing":
            print("no skittle - time to shake!")
            LogData(RGB,L,T,color)
            Shake()
        else:
            LogData(RGB,L,T,color)
            kit.servo[rampServo].angle = MotorColorPos(color)
            time.sleep(0.5)
            kit.servo[feederServo].angle = 15 # Ramp position
            time.sleep(0.5)