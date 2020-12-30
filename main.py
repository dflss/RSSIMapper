import argparse
from typing import List

from measurements import Measurements
from program_data import ProgramData
from serial_connection import SerialConnection
from shapefile_manager import ShapefileManager


def parse_cmd_args() -> ProgramData:
    parser = argparse.ArgumentParser()
    optional = parser._action_groups.pop()
    optional.add_argument("-ic", "--input_csv", help="input csv to create shapefile")
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


def perform_measurements(program_data: ProgramData, ids: List[int]):
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
        user_input = input('Type measurement point id and click enter, q + enter to quit ')
        if user_input == 'q':
            exit(0)
        try:
            mp_id = int(user_input)
            if mp_id in ids:
                rssi, perc = measurements.measure_point()
                shapefile_man = ShapefileManager()
                shapefile_man.update_map_with_rssi_data(program_data.output_shapefile, mp_id, rssi, perc)
            else:
                print("This id does not exist in the given shapefile.")
        except ValueError:
            print("Measurement point id must be an integer value.")


def create_shapefile(program_data: ProgramData, shapefile_man: ShapefileManager):
    shapefile_man.write_input_map(program_data.input_csv, program_data.input_shapefile)


def read_input_shapefile(program_data: ProgramData, shapefile_man: ShapefileManager) -> List[int]:
    return shapefile_man.read(program_data.input_shapefile)


def read_output_shapefile(program_data: ProgramData, shapefile_man: ShapefileManager) -> List[int]:
    return shapefile_man.read_output(program_data.output_shapefile)


def main():
    program_data = parse_cmd_args()
    shapefile_man = ShapefileManager()
    if program_data.input_csv:
        create_shapefile(program_data, shapefile_man)
    shapefile_man.write_output_map(program_data.input_shapefile, program_data.output_shapefile)
    # ids = read_input_shapefile(program_data, shapefile_man)
    read_output_shapefile(program_data, shapefile_man)
    # perform_measurements(program_data, ids)


if __name__ == '__main__':
    main()
