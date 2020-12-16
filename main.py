import argparse

from measurements import Measurements
from program_data import ProgramData
from serial_connection import SerialConnection
from shapefile_manager import ShapefileManager


def parse_cmd_args():
    parser = argparse.ArgumentParser()
    optional = parser._action_groups.pop()
    optional.add_argument("-ic", "--input_csv", help="input csv to create shapefile", default=None)
    required = parser.add_argument_group('required arguments')
    required.add_argument("-is", "--input_shapefile", help="input shapefile", required=True)
    required.add_argument("-or", "--output_results", help="text file for saving results", required=True)
    required.add_argument("-os", "--output_shapefile", help="file for saving colored map", required=True)
    required.add_argument("-p", "--port", help="port where board is connected", required=True)
    required.add_argument("-b", "--baudrate", help="baudrate for serial connection", required=True)
    required.add_argument("-st", "--serial_timeout", help="timeout for serial connection", required=True)
    required.add_argument("-mt", "--measurement_timeout", help="timeout for measurement point", required=True)
    required.add_argument("-n", "--n_points", help="number of measurements taken for 1 point", required=True)
    parser._action_groups.append(optional)
    args = parser.parse_args()
    return \
        ProgramData(
            args.input_csv,
            args.input_shapefile,
            args.output_results,
            args.output_shapefile,
            args.port,
            int(args.baudrate),
            int(args.serial_timeout),
            int(args.measurement_timeout),
            int(args.n_points),
        )


def perform_measurements(program_data):
    serial_conn = \
        SerialConnection(
            port=program_data.port,
            baudrate=program_data.baudrate,
            timeout=program_data.serial_timeout
        )
    measurements = \
        Measurements(
            serial_conn=serial_conn,
            points_number=program_data.n_points,
            timeout=program_data.measurement_timeout
        )
    while True:
        if input('Press enter to continue, q + enter to quit ') == 'q':
            exit(0)
        print(measurements.measure_point())


def create_shapefile(program_data):
    shapefile_man = ShapefileManager()
    shapefile_man.write(program_data.input_csv, program_data.input_shapefile)

def read_shapefile(program_data):
    shapefile_man = ShapefileManager()
    shapefile_man.read(program_data.input_shapefile)


def main():
    program_data = parse_cmd_args()
    if program_data.input_csv:
        create_shapefile(program_data)
    read_shapefile(program_data)
    # perform_measurements(program_data)


if __name__ == '__main__':
    main()
