import configparser
import os

from src.log import logger
from src.model.program_data import ProgramData



DEFAULT_PROGRAM_DATA = ProgramData('input_data/example-data.csv', 'input_data/input_map', 'output_data/output_results',
                                   'output_data/map', 'output_data/plot', '/dev/pts/2', 115200, 10, 100, 100)


class ConfigManager:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path

    def read(self):
        parser = configparser.ConfigParser()
        if os.path.isfile(self.config_file_path):
            parser.read(self.config_file_path)
            program_data = ProgramData(**parser._sections['Settings'])
        else:
            logger.debug(f"Config file not found. Creating file {self.config_file_path}")
            self.update(DEFAULT_PROGRAM_DATA)
            program_data = DEFAULT_PROGRAM_DATA
        return program_data

    def update(self, program_data: ProgramData):
        parser = configparser.ConfigParser()
        parser.add_section('Settings')
        parser.set('Settings', 'input_csv', program_data.input_csv)
        parser.set('Settings', 'input_shapefile', program_data.input_shapefile)
        parser.set('Settings', 'output_results', program_data.output_results)
        parser.set('Settings', 'output_shapefile', program_data.output_shapefile)
        parser.set('Settings', 'output_plot', program_data.output_plot)
        parser.set('Settings', 'port', program_data.port)
        parser.set('Settings', 'baudrate', str(program_data.baudrate))
        parser.set('Settings', 'serial_timeout', str(program_data.serial_timeout))
        parser.set('Settings', 'measurement_timeout', str(program_data.measurement_timeout))
        parser.set('Settings', 'n_measurements_per_point', str(program_data.n_measurements_per_point))
        print("update config")
        print(parser._sections['Settings'])
        with open(self.config_file_path, 'w') as fp:
            parser.write(fp)