import argparse
from dataclasses import dataclass

from measurements import Measurements
from serial_connection import SerialConnection


@dataclass
class ProgramData:
    input_file: str
    output_file: str
    map_output_file: str
    port: str
    baudrate: int
    serial_timeout: int
    measurement_timeout: int
    n_points: int


def parse_cmd_args():
    parser = argparse.ArgumentParser()
    optional = parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    required.add_argument("-i", "--input_file", help="input shapefile", required=True)
    required.add_argument("-o", "--output_file", help="text file for saving results", required=True)
    required.add_argument("-m", "--map_output_file", help="file for saving colored map", required=True)
    required.add_argument("-p", "--port", help="port where board is connected", required=True)
    required.add_argument("-b", "--baudrate", help="baudrate for serial connection", required=True)
    required.add_argument("-st", "--serial_timeout", help="timeout for serial connection", required=True)
    required.add_argument("-mt", "--measurement_timeout", help="timeout for measurement point", required=True)
    required.add_argument("-n", "--n_points", help="number of measurements taken for 1 point", required=True)
    parser._action_groups.append(optional)
    args = parser.parse_args()
    return \
        ProgramData(
            args.input_file,
            args.output_file,
            args.map_output_file,
            args.port,
            int(args.baudrate),
            int(args.serial_timeout),
            int(args.measurement_timeout),
            int(args.n_points),
        )


def main():
    program_data = parse_cmd_args()
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


if __name__ == '__main__':
    main()