# Candy-Sorter

<img src="./Resources/CandySorterOnshapeAnimation.gif" alt="CandySorterOnshapeAnimation" width="50%" align="middle"/>

## What is this?
The goal of the candy sorter activity is to introduce students to the process of designing, building, and analyzing a closed loop manufacturing process. 

#### This tutorial shows you how to put together the candy sorting machine found in [this Onshape document](https://cad.onshape.com/documents/9538cae8040bf2539c85bf1f/w/b1f052bee86b8f568c4616e4/e/a4dabf18665eca6b067f7bca)
The original version of the candy sorting machine was made to sort skittles, but the model can be configured to fit any size candy of different color.

<details><summary><b>Software</b></summary>
<ul>
<li>Onshape</li>
<li>ThingWorx</li>
<li>Vuforia View</li>
</ul>
</details>
  
<details><summary><b>Hardware</b></summary>
<ul>
  <li><a href="https://www.raspberrypi.org/">Raspberry Pi</a> (tested with 3B+, Pi Zero W and Pi 4 being tested currently)</li>
<li><a href="https://learn.adafruit.com/assets/59109">Color sensor option 1 - soldering required, better quality</a></li>
<li><a href="https://www.waveshare.com/color-sensor.htm">Color sensor option 2 - no soldering required</a></li>
<li><a href="https://www.adafruit.com/product/2327?gclid=CjwKCAjw87SHBhBiEiwAukSeUXhnyrBdVb3wdNFaqTztPAIurUUoyuI3_6jCyiNULFe7ilsiTvhqtRoCTJgQAvD_BwE">Servo motor hat option 1 - soldering required</a></li>
<li><a href="https://www.waveshare.com/product/raspberry-pi/hats/servo-driver-hat.htm">Servo motor hat option 2 - no soldering required</a></li>
  <li><a href="https://www.adafruit.com/product/276">Power supply</a></li>
<li><a href="https://www.adafruit.com/product/2223">Raspberry Pi stacking headers (for option 2)</a></li>
</ul>
</details>
  
  
<h2> Build Candy Sorting Machine (using AR work instructions)</h2>
<details><summary><b>Building Steps</b></summary>
<br>
  <ol>
<li>3D print and laser cut all components </li>
<li>Assmeble the base with motors (do not attach hubs yet)</li>
<li>Press fit or hot glue servo hubs into the feeder disk and ramp (do not attach hubs yet)</li>
<li>Solder motor shield and sensor, and connect wires</li>
  </ol>
</details>

## Set up Raspberry Pi
<details><summary><b>Set up steps</b></summary>
<ol>
<li>
  
  Flash clean image of raspian to an SD card, boot up pi, and connect to internet. Setup instructions can be found on [this page](https://www.raspberrypi.org/documentation/setup/).
    </li>
<li>Connect to pi over vnc (recommended) or headless with ssh</li>
<li>
  
  Enable I2C pins and remote GPIO control from the "Interfaces" menu after typing `sudo raspi-config`</li>
<li>Clone this repo
  
`
git clone https://github.com/PTC-Education/Candy-Sorter
`
    </li>
<li>
  
  Run the following commands from within the CandySorter folder in the terminal on the Raspberry Pi (run `cd CandySorter` from terminal to get into the CandySorter folder on the pi)
```
sudo pip3 install adafruit-circuitpython-servokit
sudo pip3 install adafruit-circuitpython-tcs34725
sudo apt-get install python3-pandas
```
  </li>
    
  </ol>
  
</details>

## Test and Calibrate Motors and Sensor
<details><summary><b>Steps for testing and calibrating</b></summary>

  <ol>
<li>Start a python repl from the CandySorter folder on your Raspberry Pi by typing python3 into a terminal

`python3`
</li>
<li>
  
  Import the candysorter python library
`import candysorter`
    </li>
<li>
  
  Run the test scripts
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
    </li>
<li>
  
  Once everything looks good, run the full motor test script. Motors will end at 90 degrees.
```
candysorter.fullServoTest()
```
    </li>
<li>Attach feeder disk to the servo so that the candy hole is lined up with where the sensor goes and the ramp so it is pointing toward the middle color bin.<br>
  <img src="./Resources/CandySorterServoAlignment.jpg" alt="MotorPosition" width="50%"/></li>
</ol>
</details>
  
  
## Set up ThingWorx Entities and Test REST API Connection
<details><summary><b>OPTION 1 - Import DataTable Thing</b></summary>

1. Download the files named "DataShapes_CandySorterDataShape.xml" and "Things_CandySorter.xml" from this repo, then upload them following [these instructions](https://support.ptc.com/help/thingworx_hc/thingworx_8_hc/en/index.html#page/ThingWorx/Help/Getting_Started/ImportingandExportinginThingWorx/ImportingandExportingDataEntitiesandExtensions.html). You should start by uploading the DataShapes file, then uploading the Things file. You should then see a DataTable Thing in your ThingWorx instance which has the properties and services listed below.
2. Create an AppKey that has permisions to interact with the Data Table thing, then run the following script from your python repl
`candysorter.setThingWorxCreds()`
3. Run the following script from the python repl to test the connection to ThingWorx `candysorter.testConnection()` and ensure you see a 200 response status code.

  </details>
  

<details><summary><b>OPTION 2 - Create Entities Yourself</b></summary>

1. Create a new Data Shape with the following field definitions
<img src="./Resources/DataShapeFields.png" alt="DataShape"/>
2. Create a new Data Table Thing with the following template and select the data shape you've just made for the data shape
<img src="./Resources/DataTableTemplate.png" alt="DataTable" width="50%"/>
3. Add the following properties to the data table thing
<img src="./Resources/DataTableProperties.png" alt="DataTableProperties"/>
4. Created four custom services in the data table that are named the same as the .js files in the <a href="https://github.com/PTC-Education/Candy-Sorter/tree/main/ThingWorx%20Services">ThingWorx Services folder</a> in this repo. Make sure you also add the inputs from the screenshot below and specify the data type for the output.
<img src="./Resources/DataTableServices.png" alt="DataTableServices"/>
5. Create an AppKey that has permisions to interact with the Data Table thing, then run the following script from your python repl
`candysorter.setThingWorxCreds()`
6. Run the following script from the python repl to test the connection to ThingWorx `candysorter.testConnection()` and ensure you see a 200 response status code.

  </details>
  
## Train Model
<details><summary><b>How to train a model</b></summary>

* Now you are ready to train your model. You 

