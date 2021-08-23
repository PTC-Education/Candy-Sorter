## Python Library

This folder contains a python library with all of the functions needed to control the candy sorter. By running a python REPL from the main folder, you can `import candysorter`, which will execute the `__init__.py` file from this folder.

## Functions

Below are a list of functions in this library to help you get started with the candy sorter.

### Test Scripts
```
candysorter.feederServoTest()
candysorter.rampServoTest()
candysorter.sensorTest()
candysorter.fullServoTest()
candysorter.testConnection()
```
### Settings Scripts
```
candysorter.setServoNumbers()
candysorter.setColorPos()
candysorter.setFeederPos()
candysorter.setThingWorxCreds()
```
### Main Scripts
The scripts below can be used to operate the sorter machine once it has been set up and tested.

#### Build Data Set
Script for manually inputting the color of the candy and logging data to a ThingWorx data table
```
candysorter.mainTraining(5) # input arguement is number of rows to add per candy
```

#### Train Model
Script for training a model in ThingWorx. 
```
candysorter.trainModel()
```
* The script should prompt you to type in the data type and operational type of each of the fields.
    * For the Red, Green, and Blue fields, they should be INTEGER and CONTINUOUS.
    * The Temperature and Lux fields should be NUMBER and CONTINUOUS.
    * The Color field should be STRING and CATEGORICAL.
    * And for the values of the Color field, you should put in the values as an array ["red","green","orange","purple","yellow","none"]

#### Get Model Status
Script for checking if the model has finished training
```
candysorter.getModelStatus()
```

#### Run Candy Sorter with Realtime Predictions
The script for running the machine with real time predicitons from your model in ThingWorx
```
candysorter.mainAutoSort()
```
