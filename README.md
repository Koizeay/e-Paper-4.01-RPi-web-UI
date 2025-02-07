# e-Paper WS web UI for Raspberry Pi
By Koizeay - 2025

## Description
This is a server allowing the control of the WaveShare e-Paper 4.01" 640x400px 7 colors RPi hat display via a web interface.\
https://www.waveshare.com/4.01inch-e-paper-hat-f.htm

## Disclaimer
This is a personal project created in my spare time for fun and learning purposes. It may contain bugs and security vulnerabilities.\
This project is not affiliated with WaveShare or Raspberry Pi in any way.

## Prerequisites
- Raspberry Pi (tested on RPi 4 and RPi 3b+)
- Raspberry Pi e-Paper display (mentioned above)
- Raspberry Pi OS (tested on "Raspberry Pi OS Lite (64 bits) - 2024-11-19"
- Python 3 (tested on Python 3.11.2)

## Tutorial
First, enable SPI (via `sudo raspi-config`) on your Raspberry Pi before running this server.

1. Install the required packages for the server:
```bash
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-pil
sudo apt-get install python3-numpy
sudo apt-get install python3-spidev
sudo apt-get install python3-flask
```
2. Run the server with `python3 app.py`
3. Access the server at `http://X.X.X.X:8080` where `X.X.X.X` is the IP address of your Raspberry Pi.

More information on the e-Paper display can be found [here](https://www.waveshare.com/wiki/4.01inch_e-Paper_HAT_(F)_Manual#Working_With_Raspberry_Pi)

## More
- The folder "_Image converter" contains a script to convert images to the format required by the e-Paper display.
- The folder "_YT Music Cover E-Paper" contains a script to display the cover of the currently playing song on YouTube Music on the e-Paper display using a Firefox extension.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

_**Except for the e-Paper display library (in the `lib` folder), which is property of WaveShare.**_