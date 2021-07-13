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

```
sudo pip3 install adafruit-circuitpython-servokit
sudo pip3 install adafruit-circuitpython-tcs34725
```
