# RSSIMapper

## Table of contents
* [General info](#general-info)
* [Getting started](#getting-started)
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

Run main.py with the required arguments:

```
usage: main.py [-h] [-ic INPUT_CSV] -is INPUT_SHAPEFILE -or OUTPUT_RESULTS -os OUTPUT_SHAPEFILE -p PORT -b BAUDRATE -st SERIAL_TIMEOUT -mt MEASUREMENT_TIMEOUT -n N_POINTS

required arguments:
  -is INPUT_SHAPEFILE, --input_shapefile INPUT_SHAPEFILE
                        input shapefile
  -or OUTPUT_RESULTS, --output_results OUTPUT_RESULTS
                        text file for saving results
  -os OUTPUT_SHAPEFILE, --output_shapefile OUTPUT_SHAPEFILE
                        file for saving colored map
  -p PORT, --port PORT  port where board is connected
  -b BAUDRATE, --baudrate BAUDRATE
                        baudrate for serial connection
  -st SERIAL_TIMEOUT, --serial_timeout SERIAL_TIMEOUT
                        timeout for serial connection
  -mt MEASUREMENT_TIMEOUT, --measurement_timeout MEASUREMENT_TIMEOUT
                        timeout for measurement point
  -n N_POINTS, --n_points N_POINTS
                        number of measurements taken for 1 point

optional arguments:
  -h, --help            show this help message and exit
  -ic INPUT_CSV, --input_csv INPUT_CSV
                        input csv to create shapefile
```

Example usage:

```
python main.py -ic example-data.csv -is input_map -or output -os map -p /dev/pts/1 -b 115200 -st 10 -mt 100 -n 100
```

## Testing

A script for testing the program without physical board can be found in emulate_device.sh.

To use it, first in terminal run:

```
socat -d -d pty,raw,echo=0,b9600 pty,raw,echo=0,b9600
```

The output should be similar to the following:

```
2020/12/18 09:05:37 socat[347564] N PTY is /dev/pts/3
2020/12/18 09:05:37 socat[347564] N PTY is /dev/pts/4
2020/12/18 09:05:37 socat[347564] N starting data transfer loop with FDs [5,5] and [9,9]
```

Then in another terminal run:

```
./emulate_device.sh /dev/pts/3
```
