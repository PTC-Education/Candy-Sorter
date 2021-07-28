print(f'Invoking __init__.py for {__name__}')

import time
import requests
import json
import pandas as pd

from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
import board
import adafruit_tcs34725
i2c = board.I2C()
sensor = adafruit_tcs34725.TCS34725(i2c)

## Set ThingWorx Parameters
baseURL = "https://pp-2101111403aw.portal.ptc.io/Thingworx/Things/CandySorter/"
appKey = '156f0901-bed5-41fb-a2bd-34b5580ecf38'

## Set Motor Numbers
feederServo = 6
rampServo = 7

## Set Ramp Servo Positions
orangePos = 120
redPos = 98
yellowPos = 75
greenPos = 52
purplePos = 30

## Set Feeder Disk Motor Positions
hopperPos = 160
sensorPos = 90
rampPos = 20

##
## Define Settings Functions
##
##
def setServoNumbers():
    global feederServo
    feederServo = int(input("Enter pin number of feeder servo:"))
    global rampServo
    rampServo = int(input("Enter pin number of ramp servo:"))

def setThingWorxCreds():
    global baseURL
    global appKey
    baseURL = input("Enter your ThingWorx URL including the name of your thing (i.e. 'https://pp-123abc.portal.ptc.io/Thingworx/Things/CandySorter/'):")
    appKey = input("Enter your ThingWorx appKey:")

def setColorPos():
    global orangePos
    global redPos
    global yellowPos
    global greenPos
    global purplePos
    orangePos = int(input("Input new orange bin angle: (current position is "+str(orangePos)+"):"))
    redPos = int(input("Input new red bin angle: (current position is "+str(redPos)+"):"))
    yellowPos = int(input("Input new yellow bin angle: (current position is "+str(yellowPos)+"):"))
    greenPos = int(input("Input new green bin angle: (current position is "+str(greenPos)+"):"))
    purplePos = int(input("Input new purple bin angle: (current position is "+str(purplePos)+"):"))

def setFeederPos():
    global hopperPos
    global sensorPos
    global rampPos
    hopperPos = int(input("Input new hopper position angle: (current position is "+str(hopperPos)+"):"))
    sensorPos = int(input("Input new sensor position angle: (current position is "+str(sensorPos)+"):"))
    rampPos = int(input("Input new ramp position angle: (current position is "+str(rampPos)+"):"))

## Set Ramp Motor Positions
def MotorColorPos(argument):
    switcher = {
        'orange': orangePos,
        'red': redPos,
        'yellow': yellowPos,
        'green': greenPos,
        'purple': purplePos
    }
    return switcher.get(argument, "nothing")

## Define Testing Functions
##
##
def feederServoTest():
    print('moving feeder servo')
    kit.servo[feederServo].angle = hopperPos
    time.sleep(1)
    kit.servo[feederServo].angle = sensorPos
    time.sleep(1)
    kit.servo[feederServo].angle = rampPos
    time.sleep(1)

def rampServoTest():
    print('moving ramp servo')
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

def fullServoTest():
    print('moving ramp servo')
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
    print('moving feeder servo')
    feederServoTest()
    kit.servo[feederServo].angle = 90
    kit.servo[rampServo].angle = 90

def sensorTest():
    RGB = sensor.color_rgb_bytes
    L = sensor.lux
    T = sensor.color_temperature
    print(RGB,L,T)

##
## Define ThingWorx Functions
##
## Helper functions
def GetPrediction(RGB,L,T):
    twService = "Services/ColorPredictionService"
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
    twService = "Services/AddCandyData"
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

def GetData():
    twService = "Services/SearchDataTableEntries"

    payload=json.dumps({"maxItems":500})
    headers = {
    'appKey': appKey,
    'Content-Type': 'application/json',
    'accept': 'text/csv'
    }

    response = requests.request("POST", baseURL+twService, headers=headers, data=payload)
    print(response)

    with open('trainingdata.csv','w') as f:
        f.write(response.text)

    data = pd.read_csv('trainingdata.csv')
    data.drop('key', inplace=True, axis=1)
    data.drop('location', inplace=True, axis=1)
    data.drop('source', inplace=True, axis=1)
    data.drop('sourceType', inplace=True, axis=1)
    data.drop('tags', inplace=True, axis=1)
    data.drop('timestamp', inplace=True, axis=1)
    data.drop('CandyNumber', inplace=True, axis=1)
    
    transformed_data =  {'rows': []}
    for row in range(len(data.values)):
    # create an empty dictionary for each row
        dict= {}
        for col in range(len(data.values[0])):
            # add new key - value pairs for the dict, one pair for each column
            dict [data.columns[col]] = data.values[row][col] 

        # append the dictionary of one row to the list of dictionaries
        transformed_data['rows'].append(dict)

    return transformed_data, data

def callTrainModelService():
    transformed_data, data = GetData()
    twService = "Services/TrainAnalyticsModel"
    goal = input("Which of the following fields "+str(data.columns)+" is the goal you'd like to predict?")
    headers = {
      'appKey': appKey,
      'Content-Type': 'application/json',
      'accept': 'application/json'
    }
    payload = {"goal": goal, # use the input from the user as goal 
                "trainingData": { # Thingworx Infotable containing the training data
                    "dataShape": { # Thingworx needs this information to know which name and data types the individual columns in spreadsheet have
                        "fieldDefinitions": { # add a empty dictionary, data shape information gets filled in later
                        }
                    },
                "rows": transformed_data["rows"]}, # each row contains the values of one row of the spreadsheet that was read in before
                "metadataInput": { # Thingworx Analytics need additional information of the data supplied for training
                    "dataShape": { # Same reason as above, used to define the structure of the Thingworx Infotable
                        "fieldDefinitions": { # following fields are the Infotable structure for AnalyticsDatasetMetadataFlattened Infotable
                                            # in Analytics builder you can manually add those definitions with a GUI 
                                            # https://support.ptc.com/help/thingworx_hc/thingworx_analytics_8/index.html#page/analytics%2Fanalytics-builder%2Freview_edit_metadata.html%23
                            "fieldName": {
                                "name": "fieldName",
                                "description": "",
                                "baseType": "STRING",
                                "ordinal": 0,
                                "aspects": {

                                }
                            },
                            "dataType": {
                                "name": "dataType",
                                "description": "",
                                "baseType": "STRING",
                                "ordinal": 0,
                                "aspects": {

                                }
                            },
                            "opType": {
                                "name": "opType",
                                "description": "",
                                "baseType": "STRING",
                                "ordinal": 0,
                                "aspects": {

                                }
                            },
                            "min": {
                                "name": "min",
                                "description": "",
                                "baseType": "NUMBER",
                                "ordinal": 0,
                                "aspects": {

                                }
                            },
                            "max": {
                                "name": "max",
                                "description": "",
                                "baseType": "NUMBER",
                                "ordinal": 0,
                                "aspects": {

                                }
                            },
                            "values": {
                                "name": "values",
                                "description": "",
                                "baseType": "INFOTABLE",
                                "ordinal": 0,
                                "aspects": {
                                    "dataShape": "GenericStringList"
                                }
                            },
                            "timeSamplingInterval": {
                                "name": "timeSamplingInterval",
                                "description": "",
                                "baseType": "INTEGER",
                                "ordinal": 0,
                                "aspects": {

                                }
                            },
                            "isStatic": {
                                "name": "isStatic",
                                "description": "",
                                "baseType": "BOOLEAN",
                                "ordinal": 0,
                                "aspects": {
                                    "defaultValue": "false"
                                }
                            }
                        }
                    },
                    "rows": [ # add empty list for the meta data information for each feature, data gets filled in later
                    ]
                }
                }

    datashape_dict = {"fieldDefinitions" : {}} # create a empty dictionary to fill in the field definitions for the training data
    metadata_list = [] # create a empty list to fill in the metadata information

    # fill the datashape definition of the training data read from the spreadsheet
    for col in range(len(data.columns)): # iterate over columns
        baseType = input("Input the base type for the field named "+data.columns[col]+" (i.e. INTEGER, NUMBER, STRING, etc.):")
        opType = input("Input the op type for the field named "+data.columns[col]+" (i.e. CONTINUOUS, CATEGORICAL, etc.):")
        datashape_dict["fieldDefinitions"][data.columns[col]]= { #add new key to field definitions
            "name" : data.columns[col], # name is the same value as the key 
            "aspects" : {
                "isPrimaryKey": "false"
            },
            "description": "",
            "baseType": baseType # only numbers are used for this script, Thingworx base types that can be used with Analytics are supported, see link down below
        }
        if opType == "CATEGORICAL":
            valueList = input("Input the various values for the categorical field as array (i.e. ['red','green','blue']):")
            metadata_list.append({ # add metadata information for each column supplied in the spreadsheet, info on Analytics data types:
                                ## https://support.ptc.com/help/thingworx_hc/thingworx_analytics_8/index.html#page/analytics%2Fanalytics-data-key-infotables.html%23wwID0EONHU
                                "fieldName": data.columns[col],
                                "dataType": baseType,
                                "opType": opType,
                                "isStatic": "false",
                                "values": valueList
                            })
        elif baseType == "NUMBER":
            metadata_list.append({ # add metadata information for each column supplied in the spreadsheet, info on Analytics data types:
                                ## https://support.ptc.com/help/thingworx_hc/thingworx_analytics_8/index.html#page/analytics%2Fanalytics-data-key-infotables.html%23wwID0EONHU
                                "fieldName": data.columns[col],
                                "dataType": "DOUBLE",
                                "opType": opType,
                                "isStatic": "false"
                            })
        else:
            metadata_list.append({ # add metadata information for each column supplied in the spreadsheet, info on Analytics data types:
                                ## https://support.ptc.com/help/thingworx_hc/thingworx_analytics_8/index.html#page/analytics%2Fanalytics-data-key-infotables.html%23wwID0EONHU
                                "fieldName": data.columns[col],
                                "dataType": baseType,
                                "opType": opType,
                                "isStatic": "false"
                            })

    payload["metadataInput"]["rows"].extend(metadata_list) # add metadata information to the payload sent to Thingworx
    #print(payload["metadataInput"]["rows"])
    #print (datashape_dict)
    payload["trainingData"]["dataShape"].update(datashape_dict) # add training data information to the payload sent to Thingworx
    #print(payload["trainingData"]["dataShape"])
    thingworx_response = requests.post(baseURL+twService, headers=headers, json=payload, verify=False)
    return thingworx_response

## Main TW Functions
def trainMode():
    response = callTrainModelService() # execute the the service call
    if response.status_code == 200: # check the response 
        result = json.loads(response.text)
        modelUri = result["rows"][0]["result"] # read the model URI from the complete Thingworx response    
        print("The URI for the Analytics model is: " + modelUri)
        print("Please call the check model status service next, to see if the training is finished!")
    else:
        print("Request failed with error code: " + str(response))
        print("Thingworx error code: " + str(response.text))

def getModelStatus():
    url = 'https://pp-2101111403aw.portal.ptc.io/Thingworx/Things/CandySorter/Services/GetModelStatus'
    headers = {'Content-Type': 'application/json', 'accept': 'application/json', "appKey": appKey}

    def call_thingworx_service():
        payload = {"modelUri": "0feb6101-0575-4713-9fc3-ae91ff59f069"}
        thingworx_response = requests.post(url, headers=headers, json=payload, verify=False)
        return thingworx_response


    response = call_thingworx_service()
    if response.status_code == 200:
        result = json.loads(response.text)
        while result["rows"][0]["state"] != "COMPLETED":
            print("Training of the model is not finished yet.")
            time.sleep(20)
            response = call_thingworx_service()
            if response.status_code == 200:
                result = json.loads(response.text)  
            

        status = result["rows"][0]["state"]  # read the state of the complete Thingworx response
        print("The current training status for the Analytics model is: " + status)
    else:
        print("Request failed with error code: " + str(response))
        print("Thingworx error code: " + str(response.text))

##
## Define Main Functions
##
##
def Shake():
    for i in range(5):
        kit.servo[feederServo].angle = 15
        time.sleep(0.05)
        kit.servo[feederServo].angle = 100
        time.sleep(0.05)
  
# Automatic sorting program
def mainAutoSort():
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
            Shake()
        else:
            kit.servo[rampServo].angle = MotorColorPos(color)
            time.sleep(0.5)
            kit.servo[feederServo].angle = rampPos # Ramp position
            time.sleep(0.5)

# Training program
def mainTraining(duplicationNum):
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
            LogData(sensor.color_rgb_bytes,sensor.lux,sensor.color_temperature,"none")
            Shake()
        else:
            for i in range(duplicationNum):
                LogData(sensor.color_rgb_bytes,sensor.lux,sensor.color_temperature,color)
            kit.servo[rampServo].angle = MotorColorPos(color)
            time.sleep(0.5)
            kit.servo[feederServo].angle = 15 # Ramp position
            time.sleep(0.5)