# Candy-Sorter

## Parts
[Color sensor](https://learn.adafruit.com/assets/59109)
[Servo motor hat](https://www.adafruit.com/product/2327?gclid=CjwKCAjw87SHBhBiEiwAukSeUXhnyrBdVb3wdNFaqTztPAIurUUoyuI3_6jCyiNULFe7ilsiTvhqtRoCTJgQAvD_BwE)
[Power supply](https://www.adafruit.com/product/276)
[Raspberry Pi stacking headers](https://www.adafruit.com/product/2223)

### Set up Raspberry Pi
1. Flash clean image of raspian to an SD card, boot up pi, and connect to internet
2. Connect to pi over vnc (recommended) or headless with ssh
3. Enable I2C pins and remote GPIO control
4. Clone this repo into Documents
5. Run the following commands from within the CandySorter folder in the terminal on the Raspberry Pi
```
sudo pip3 install adafruit-circuitpython-servokit
sudo pip3 install adafruit-circuitpython-tcs34725
sudo apt-get install python-pandas
```

### Build Candy Sorting Machine (using AR work instructions)
1. 3D print and laser cut all components 
2. Assmeble the base with motors (do not attach hubs yet)
3. Press fit or hot glue servo hubs into the feeder disk and ramp (do not attach hubs yet)
4. Solder motor shield and sensor, and connect wires
5. Run the motor test script with the following command
```
python3 MotorTest.py
```
5. Motors will end at 90 degrees - attach feeder disk to the servo so that the candy hole is lined up with where the sensor goes and the ramp so it is pointing toward the middle color bin
6. Run the sensor test script with the following command
```
python3 SensorTest.py
```

### Calibrate Machine and Train Model
