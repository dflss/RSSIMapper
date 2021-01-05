import argparse
import sys

from controller import Controller
from map_plotter import MapPlotter
from measurements_manager import MeasurementsManager
from measurements_map import MeasurementsMap

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


def perform_measurements(program_data: ProgramData, measurements_map: MeasurementsMap):
    serial_conn = \
        SerialConnection(
            port=program_data.port,
            baudrate=program_data.baudrate,
            timeout=program_data.serial_timeout
        )
    measurements_mgr = \
        MeasurementsManager(
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
            if mp_id in measurements_map.ids:
                result = measurements_mgr.measure_point()
                if result:
                    rssi, perc = result
                    measurements_map.update_map_with_rssi_values(mp_id, int(rssi), int(perc))
            else:
                print("This id does not exist in the given shapefile.")
        except ValueError:
            print("Measurement point id must be an integer value.")


def run_gui():
    Controller()


def run_cli():
    program_data = parse_cmd_args()
    shapefile_mgr = \
        ShapefileManager(
            program_data.input_shapefile,
            program_data.output_shapefile,
            program_data.input_csv
        )
    measurements_map = MeasurementsMap(shapefile_mgr.read_shapefile())
    map_plotter = MapPlotter(measurements_map)
    map_plotter.display_with_rssi_values()  # display initial output map
    perform_measurements(program_data, measurements_map)
    map_plotter.display_with_rssi_values()  # display output map with the results of measurements
    shapefile_mgr.update_shapefile(measurements_map.shape_records)


def main():
    if not len(sys.argv) > 1:
        run_gui()
    else:
        run_cli()


if __name__ == '__main__':
    main()
