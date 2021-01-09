# RSSIMapper

## Table of contents
* [General info](#general-info)
* [Getting started](#getting-started)
* [Command-line mode](#cli)
* [Graphical interface mode](#gui)
* [Testing](#testing)

## General info
The aim of the project is to provide a tool for measurement of RSSI of the signal sent by IoT devices and visualise the signal strength on a map. This project is developed as a part of a Master thesis.

## Getting started

RSSIMapper works with [Python 3](https://www.python.org/downloads/), on any platform.

To get started with RSSIMapper, create and activate python virtual environment:

```
python3 -m venv venv
source venv/bin/activate
```

Next, install requirements:

```
pip install -r requirements.txt
```

The program can be run in CLI or graphical interface mode. 

## Command-line mode

In order to use the program in the CLI mode, run main.py with the required arguments:

```
usage: main.py [-h] [-ic INPUT_CSV] -is INPUT_SHAPEFILE -or OUTPUT_RESULTS -os OUTPUT_SHAPEFILE -op OUTPUT_PLOT -p PORT -b BAUDRATE -st SERIAL_TIMEOUT -mt MEASUREMENT_TIMEOUT -n N_MEASUREMENTS

required arguments:
  -is INPUT_SHAPEFILE, --input_shapefile INPUT_SHAPEFILE
                        input shapefile
  -or OUTPUT_RESULTS, --output_results OUTPUT_RESULTS
                        text file for saving results
  -os OUTPUT_SHAPEFILE, --output_shapefile OUTPUT_SHAPEFILE
                        file for saving output shapefile
  -op OUTPUT_PLOT, --output_plot OUTPUT_PLOT
                        file for saving colored map
  -p PORT, --port PORT  port where board is connected
  -b BAUDRATE, --baudrate BAUDRATE
                        baudrate for serial connection
  -st SERIAL_TIMEOUT, --serial_timeout SERIAL_TIMEOUT
                        timeout for serial connection
  -mt MEASUREMENT_TIMEOUT, --measurement_timeout MEASUREMENT_TIMEOUT
                        timeout for measurement point
  -n N_MEASUREMENTS, --n_points N_POINTS
                        number of measurements taken for 1 point

optional arguments:
  -h, --help            show this help message and exit
  -ic INPUT_CSV, --input_csv INPUT_CSV
                        input csv to create shapefile
```

Example usage:

```
python main.py -ic example-data.csv -is input_map -or output -os map -op plot -p /dev/pts/2 -b 115200 -st 10 -mt 100 -n 100
```

## Graphical interface mode

In order to use the GUI, run the program without any arguments:

```
python main.py
```
In the "Settings" tab all the program arguments can be configured and updated using the "Save" button.

![alt text](https://user-images.githubusercontent.com/20957781/104109158-f4da1c80-52c2-11eb-993a-81571c7ae772.png)

The "Map" tab will display the current RSSI map.

![alt text](https://user-images.githubusercontent.com/20957781/104104614-23df9680-52a1-11eb-90d4-d21a58842964.png)

After clicking on one of the squares (which represent a polygon with a given ID in the input shapefile), the measurement starts. The device (or device emulator script for testing) can be now run to send frames.

![alt text](https://user-images.githubusercontent.com/20957781/104104754-f2b39600-52a1-11eb-87a1-ad58e8fa4cc1.png)

When the measurement is finished (as a result of receiving n frames which were supposed to be sent during one measurement as configured in the settings, or as a result of a timeout - this can happen if some frames happen to be lost), the respective measurement point will be colored accordingly to the value of RSSI or percent of frames received and the exact value recorded by the program will be displayed on top of it. 

![alt text](https://user-images.githubusercontent.com/20957781/104104760-f810e080-52a1-11eb-920d-b135359e61ff.png)

## Testing

A script for testing the program without physical board can be found in emulate_device.sh.

To use it, first in terminal run:

```
socat -d -d pty,raw,echo=0,b9600 pty,raw,echo=0,b9600
```

The output should be similar to the following:

```
2020/12/18 09:05:37 socat[347564] N PTY is /dev/pts/2
2020/12/18 09:05:37 socat[347564] N PTY is /dev/pts/3
2020/12/18 09:05:37 socat[347564] N starting data transfer loop with FDs [5,5] and [9,9]
```

Then in another terminal run:

```
./emulate_device.sh /dev/pts/3
```
