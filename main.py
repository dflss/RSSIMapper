import argparse
from typing import List

import shapefile_manager as shapefile_mgr
from measurements import Measurements
from program_data import ProgramData
from serial_connection import SerialConnection


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
        user_input = input('Type measurement point id and click enter, '
                           'q + enter to quit measurements and show results ')
        if user_input == 'q':
            return
        try:
            mp_id = int(user_input)
            if mp_id in ids:
                result = measurements.measure_point()
                if result:
                    rssi, perc = result
                    shapefile_mgr.update_output_shapefile_map_with_rssi_values(
                        program_data.output_shapefile, mp_id, int(rssi), int(perc)
                    )
            else:
                print("This id does not exist in the given shapefile.")
        except ValueError:
            print("Measurement point id must be an integer value.")


def main():
    program_data = parse_cmd_args()
    if program_data.input_csv:
        shapefile_mgr.create_raw_shapefile_map_from_csv(program_data.input_csv, program_data.input_shapefile)
    shapefile_mgr.create_output_shapefile_map_with_rssi_and_percent_values(
        program_data.input_shapefile, program_data.output_shapefile
    )
    ids = shapefile_mgr.read_raw_shapefile_map(program_data.input_shapefile)
    # display initial map
    shapefile_mgr.read_output_shapefile_map_with_rssi_values(program_data.output_shapefile)
    perform_measurements(program_data, ids)
    # display map with the results of measurements
    shapefile_mgr.read_output_shapefile_map_with_rssi_values(program_data.output_shapefile)


if __name__ == '__main__':
    main()
