print(f'Invoking __init__.py for {__name__}')

import time
import requests
import json
import numpy
import pandas as pd
import smbus
import math

import board
import adafruit_tcs34725

motordriver = 0

## 
## 
## Set Defaults
##

## Set Motor Numbers
feederServo = 6
rampServo = 7

## Set Default Ramp Servo Positions
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
##
## Set MotorDriver type and default positions if not driver 1
##
try:
    from adafruit_servokit import ServoKit
    kit = ServoKit(channels=16)
    i2c = board.I2C()
    sensor = adafruit_tcs34725.TCS34725(i2c)
    motordriver = 1
except:
    from OnshapeCandySorter.PCA9685 import PCA9685
    pwm = PCA9685(0x40, debug=False)
    pwm.setPWMFreq(50)
    motordriver = 2    
    ## Set Default Ramp Servo Positions
    orangePos = 2200
    redPos = 2000
    yellowPos = 1600
    greenPos = 1200
    purplePos = 800
    ## Set Feeder Disk Motor Positions
    hopperPos = 2200
    sensorPos = 1500
    rampPos = 800

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

## Define Motor Position function
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
def servoDriverTest():
    for i in range(500,2500,10):  
        pwm.setServoPulse(0,i)   
        time.sleep(0.02)     

    for i in range(2500,500,-10):
        pwm.setServoPulse(0,i) 
        time.sleep(0.02)  

def feederServoTest():
    print('moving feeder servo')
    if motordriver == 1:
        kit.servo[feederServo].angle = hopperPos
        time.sleep(1)
        kit.servo[feederServo].angle = sensorPos
        time.sleep(1)
        kit.servo[feederServo].angle = rampPos
        time.sleep(1)
    elif motordriver == 2:
        pwm.setServoPulse(feederServo,hopperPos)
        time.sleep(1)
        pwm.setServoPulse(feederServo,sensorPos)
        time.sleep(1)
        pwm.setServoPulse(feederServo,rampPos)
        time.sleep(1)
    else:
        print('error running motors')

def rampServoTest():
    print('moving ramp servo')
    if motordriver == 1:
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
    elif motordriver == 2:
        pwm.setServoPulse(rampServo,MotorColorPos('orange'))
        time.sleep(1)
        pwm.setServoPulse(rampServo,MotorColorPos('red'))
        time.sleep(1)
        pwm.setServoPulse(rampServo,MotorColorPos('yellow'))
        time.sleep(1)
        pwm.setServoPulse(rampServo,MotorColorPos('green'))
        time.sleep(1)
        pwm.setServoPulse(rampServo,MotorColorPos('purple'))
        time.sleep(1)
    else:
        print('motor driver error')

def fullServoTest():
    rampServoTest()
    feederServoTest()
    if motordriver == 1:
        kit.servo[feederServo].angle = 90
        kit.servo[rampServo].angle = 90
    elif motordriver == 2:
        pwm.setServoPulse(rampServo,1500)
        pwm.setServoPulse(feederServo,1500)

def sensorTest():
    RGB = sensor.color_rgb_bytes
    L = sensor.lux
    T = sensor.color_temperature
    print(RGB,L,T)

##
##
## Define ThingWorx Analytics Functions
##
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
def trainModel():
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
        if motordriver == 1:
            kit.servo[feederServo].angle = 15
            time.sleep(0.05)
            kit.servo[feederServo].angle = 100
            time.sleep(0.05)
        elif motordriver == 2:
            pwm.setServoPulse(feederServo,700)
            time.sleep(0.05)
            pwm.setServoPulse(feederServo,2200)
            time.sleep(0.05)
  
# Automatic sorting program
def mainAutoSort():
    while(True):
        if motordriver == 1:
            kit.servo[feederServo].angle = hopperPos # candy hopper position
            time.sleep(0.5)
            kit.servo[feederServo].angle = sensorPos # color sensor position
            time.sleep(0.5)
        elif motordriver == 2:
            pwm.setServoPulse(feederServo,hopperPos)
            time.sleep(0.5)
            pwm.setServoPulse(feederServo,sensorPos)
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
        if motordriver == 1:
            kit.servo[feederServo].angle = hopperPos # candy hopper position
            time.sleep(0.5)
            kit.servo[feederServo].angle = sensorPos # color sensor position
            time.sleep(0.5)
        elif motordriver == 2:
            pwm.setServoPulse(feederServo,hopperPos)
            time.sleep(0.5)
            pwm.setServoPulse(feederServo,sensorPos)
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
            RGB = sensor.color_rgb_bytes
            UpdateJsonDataArray([RGB[0],RGB[1],RGB[2],sensor.lux,sensor.color_temperature,"none"])
            Shake()
        else:
            newData = []
            for i in range(duplicationNum):
                newData.append([RGB[0],RGB[1],RGB[2],sensor.lux,sensor.color_temperature,color])
            UpdateJsonDataArray(newData)
            if motordriver == 1:
                kit.servo[rampServo].angle = MotorColorPos(color)
                time.sleep(0.5)
                kit.servo[feederServo].angle = rampPos # Ramp position
                time.sleep(0.5)
            elif motordriver == 2:
                pwm.setServoPulse(rampServo,MotorColorPos(color))
                time.sleep(0.5)
                pwm.setServoPulse(feederServo,rampPos)
                time.sleep(0.5)


##
##
## Onshape IoT Functions   
##
##

def ConfigClient():
    print('Importing Onshape Python client - may take a minute')
    global client
    global base
    from onshape_client.client import Client
    import json
    base = 'https://cad.onshape.com' # change this if you're using a document in an enterprise (i.e. "https://ptc.onshape.com")
    access = input('What is your access key?')
    secret = input('What is your secret key?')
    client = Client(configuration={"base_url": base,
                                "access_key": access,
                                "secret_key": secret})
    print('client configured')
    return client

def MassProp():
    fixed_url = '/api/partstudios/d/did/w/wid/e/eid/massproperties'

    # https://cad.onshape.com/documents/263517311c2ad139d4eb57ca/w/b45057ae06777e0c28bca6c5/e/d316bcbc694c9dbb6555f340
    did = '263517311c2ad139d4eb57ca'
    wid = 'b45057ae06777e0c28bca6c5'
    eid = 'd316bcbc694c9dbb6555f340'

    method = 'GET'

    params = {}
    payload = {}
    headers = {'Accept': 'application/vnd.onshape.v1+json; charset=UTF-8;qs=0.1',
            'Content-Type': 'application/json'}

    fixed_url = fixed_url.replace('did', did)
    fixed_url = fixed_url.replace('wid', wid)
    fixed_url = fixed_url.replace('eid', eid)

    response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers, body=payload)

    parsed = json.loads(response.data)
    # The command below prints the entire JSON response from Onshape
    # print(json.dumps(parsed, indent=4, sort_keys=True))
    return response.status

def SetDocIds():
    global did
    global wid
    did = input('What is the Onshape documents document id? ')
    wid = input('What is the Onshape documents workspace id? ')

def SetStorageId():
    global eid
    eid = input('What is the element id of the storage AppElement in Onshape? ')

def CreateStorage():
    fixed_url = '/api/appelements/d/did/w/wid'
    global eid

    method = 'POST'

    params = {}
    payload = {
        "formatId": "com.onshapeiot",
        "name": "IoT Data",
        "description": "Created App Element",
        "jsonTree": {"dataShape":['r','g','b','l','t','color'],
            "data":[]}
        }
    headers = {'Accept': 'application/vnd.onshape.v1+json',
            'Content-Type': 'application/json'}

    fixed_url = fixed_url.replace('did', did)
    fixed_url = fixed_url.replace('wid', wid)

    response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers, body=payload)

    parsed = json.loads(response.data)
    # The command below prints the entire JSON response from Onshape
    eid = parsed['elementId']
    print('Storage element Id set to '+eid)

def GetJsonTree():
    fixed_url = '/api/appelements/d/did/w/wid/e/eid/content/json'

    method = 'GET'

    params = {}
    payload = {}
    headers = {'Accept': 'application/vnd.onshape.v2+json',
                'Content-Type': 'application/json'}

    fixed_url = fixed_url.replace('did', did)
    fixed_url = fixed_url.replace('wid', wid)
    fixed_url = fixed_url.replace('eid', eid)

    # print(base + fixed_url)

    response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers, body=payload)

    parsed = json.loads(response.data)
    # The command below prints the entire JSON response from Onshape
    # print(json.dumps(parsed, indent=4, sort_keys=True))
    return parsed

def UpdateJsonKey(key,value):
    fixed_url = '/api/appelements/d/did/w/wid/e/eid/content'

    method = 'POST'

    # Insertion: { 'btType' : 'BTJEditInsert-2523', 'path' : path, 'value' : newValue }
    jsonTreeData = GetJsonTree()

    params = {}
    payload = {
        "parentChangeId": jsonTreeData['changeId'],
        "jsonTreeEdit": {"btType" : "BTJEditChange-2636", 
                        "path" : { 'btType' : 'BTJPath-3073', 'startNode' : '', 'path' : [{ 'btType' : 'BTJPathKey-3221', 'key' : key }] }, 
                        'value' : value }
        }

    headers = {'Accept': 'application/vnd.onshape.v1+json',
            'Content-Type': 'application/json'}

    fixed_url = fixed_url.replace('did', did)
    fixed_url = fixed_url.replace('wid', wid)
    fixed_url = fixed_url.replace('eid', eid)

    response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers, body=payload)

    parsed = json.loads(response.data)
    # The command below prints the entire JSON response from Onshape
    return parsed['errorDescription']

## Append value onto array that is set to Json key named "data"
def ResetJsonDataArray():
    fixed_url = '/api/appelements/d/did/w/wid/e/eid/content'

    method = 'POST'

    # Insertion: { 'btType' : 'BTJEditInsert-2523', 'path' : path, 'value' : newValue }
    jsonTreeData = GetJsonTree()

    params = {}
    payload = {
        "parentChangeId": jsonTreeData['changeId'],
        "jsonTreeEdit": {"btType" : "BTJEditChange-2636", 
                        "path" : { 'btType' : 'BTJPath-3073', 'startNode' : '', 'path' : [{ 'btType' : 'BTJPathKey-3221', 'key' : 'data' }] }, 
                        'value' : [] }
        }

    headers = {'Accept': 'application/vnd.onshape.v1+json',
            'Content-Type': 'application/json'}

    fixed_url = fixed_url.replace('did', did)
    fixed_url = fixed_url.replace('wid', wid)
    fixed_url = fixed_url.replace('eid', eid)

    response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers, body=payload)

    parsed = json.loads(response.data)
    # The command below prints the entire JSON response from Onshape
    return parsed['errorDescription']

## Append value onto array that is set to Json key named "data"
def UpdateJsonDataArray(valueArray):
    fixed_url = '/api/appelements/d/did/w/wid/e/eid/content'

    method = 'POST'

    # Insertion: { 'btType' : 'BTJEditInsert-2523', 'path' : path, 'value' : newValue }
    jsonTreeData = GetJsonTree()
    dataArray = jsonTreeData['tree']['data']
    for row in valueArray:
        dataArray.append(row)

    params = {}
    payload = {
        "parentChangeId": jsonTreeData['changeId'],
        "jsonTreeEdit": {"btType" : "BTJEditChange-2636", 
                        "path" : { 'btType' : 'BTJPath-3073', 'startNode' : '', 'path' : [{ 'btType' : 'BTJPathKey-3221', 'key' : 'data' }] }, 
                        'value' : dataArray }
        }

    headers = {'Accept': 'application/vnd.onshape.v1+json',
            'Content-Type': 'application/json'}

    fixed_url = fixed_url.replace('did', did)
    fixed_url = fixed_url.replace('wid', wid)
    fixed_url = fixed_url.replace('eid', eid)

    response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers, body=payload)

    parsed = json.loads(response.data)
    # The command below prints the entire JSON response from Onshape
    return parsed['errorDescription']

def AddJsonKey(key,value):
    fixed_url = '/api/appelements/d/did/w/wid/e/eid/content'

    method = 'POST'

    # Insertion: { 'btType' : 'BTJEditInsert-2523', 'path' : path, 'value' : newValue }

    params = {}
    payload = {
        "parentChangeId": GetJsonTree()['changeId'],
        "jsonTreeEdit": {'btType' : 'BTJEditInsert-2523', 
                        'path' : { 'btType' : 'BTJPath-3073', 'startNode' : '', 'path' : [{ 'btType' : 'BTJPathKey-3221', 'key' : key }] }, 
                        'value' : value }
        }

    headers = {'Accept': 'application/vnd.onshape.v1+json',
            'Content-Type': 'application/json'}

    fixed_url = fixed_url.replace('did', did)
    fixed_url = fixed_url.replace('wid', wid)
    fixed_url = fixed_url.replace('eid', eid)

    response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers, body=payload)

    parsed = json.loads(response.data)
    # The command below prints the entire JSON response from Onshape
    return parsed['errorDescription']

##
##
## define Onshape data storage
##
