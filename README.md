# Candy-Sorter

## Parts
[Color sensor](https://learn.adafruit.com/assets/59109)
[Servo motor hat](https://www.adafruit.com/product/2327?gclid=CjwKCAjw87SHBhBiEiwAukSeUXhnyrBdVb3wdNFaqTztPAIurUUoyuI3_6jCyiNULFe7ilsiTvhqtRoCTJgQAvD_BwE)
[Power supply](https://www.adafruit.com/product/276)
[Raspberry Pi stacking headers](https://www.adafruit.com/product/2223)

### Build Candy Sorting Machine (using AR work instructions)
1. 3D print and laser cut all components 
2. Assmeble the base with motors (do not attach hubs yet)
3. Press fit or hot glue servo hubs into the feeder disk and ramp (do not attach hubs yet)
4. Solder motor shield and sensor, and connect wires


### Set up Raspberry Pi
1. Flash clean image of raspian to an SD card, boot up pi, and connect to internet
2. Connect to pi over vnc (recommended) or headless with ssh
3. Enable I2C pins and remote GPIO control
4. Clone this repo
```
git clone https://github.com/PTC-Education/Candy-Sorter
```
5. Run the following commands from within the CandySorter folder in the terminal on the Raspberry Pi (run "cd CandySorter" from terminal to get into the CandySorter folder on the pi)
```
sudo pip3 install adafruit-circuitpython-servokit
sudo pip3 install adafruit-circuitpython-tcs34725
sudo apt-get install python3-pandas
```

### Test and Calibrate Motors and Sensor
1. Start a python repl from the CandySorter folder by typing python3
```
python3
```
2. Import the candysorter python library
```
>>>import candysorter
```
3. Run the test scripts
```
candysorter.feederServoTest()
candysorter.rampServoTest()
candysorter.sensorTest()
```
and run the settings scripts if things are not working
```
candysorter.setServoNumbers()
candysorter.setThingWorxCreds()
candysorter.setColorPos()
candysorter.setFeederPos()
```
4. Once everything looks good, run the full motor test script. Motors will end at 90 degrees.
```
candysorter.fullServoTest()
```
5. Attach feeder disk to the servo so that the candy hole is lined up with where the sensor goes and the ramp so it is pointing toward the middle color bin.

### Set up ThingWorx Entities and Test REST API Connection
**OPTION 1 - Import DataTable Thing**

Download the file named "Things_CandySorter.xml" from this repo following [these instructions](https://support.ptc.com/help/thingworx_hc/thingworx_8_hc/en/index.html#page/ThingWorx/Help/Getting_Started/ImportingandExportinginThingWorx/ImportingandExportingDataEntitiesandExtensions.html). You should then see a DataTable Thing in your ThingWorx instance which has the properties and services listed below.

**OPTION 2 - Create Entities Yourself**

1. Create a new Data Table Thing

### Calibrate Machine and Train Model
