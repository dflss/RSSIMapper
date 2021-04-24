import matplotlib.pyplot as plt

from src.model.config_manager import ConfigManager
from src.model.map_plotter import MapPlotter
from src.model.measurements_manager import MeasurementsManager
from src.model.measurements_map import MeasurementsMap
from src.model.program_data import ProgramData
from src.model.serial_connection import SerialConnection
from src.model.shapefile_manager import ShapefileManager


CONFIG_FILE_PATH = "config.ini"


class Model:
    def __init__(self):
        self.program_data = None
        self.config_mgr = ConfigManager(CONFIG_FILE_PATH)

    def set_program_data(self, program_data: ProgramData):
        if (
            self.program_data is None
            or self.program_data.port != program_data.port
            or self.program_data.baudrate != int(program_data.baudrate)
            or self.program_data.serial_timeout != int(program_data.serial_timeout)
        ):
            self.serial_conn = SerialConnection(
                port=program_data.port,
                baudrate=int(program_data.baudrate),
                timeout=int(program_data.serial_timeout),
            )
        if (
            self.program_data is None
            or self.program_data.n_measurements_per_point
            != int(program_data.n_measurements_per_point)
            or self.program_data.measurement_timeout
            != int(program_data.measurement_timeout)
        ):
            self.measurements_mgr = MeasurementsManager(
                serial_conn=self.serial_conn,
                points_number=int(program_data.n_measurements_per_point),
                timeout=int(program_data.measurement_timeout),
            )
        if (
            self.program_data is None
            or self.program_data.input_shapefile != program_data.input_shapefile
            or self.program_data.output_shapefile != program_data.output_shapefile
            or self.program_data.input_csv != program_data.input_csv
        ):
            self.shapefile_mgr = ShapefileManager(
                program_data.input_shapefile,
                program_data.output_shapefile,
                program_data.input_csv,
            )
            self.measurements_map = MeasurementsMap(self.shapefile_mgr.read_shapefile())
            self.map_plotter = MapPlotter(self.measurements_map)
        self.program_data = program_data

    def get_program_data(self):
        return self.program_data

    def get_received_status(self):
        return self.measurements_mgr.received

    def measure_point_by_coordinates(self, x: int, y: int):
        id = self.measurements_map.find_point_id(x, y)
        self.measure_point_by_id(id)

    def measure_point_by_id(self, id: int):
        result = self.measurements_mgr.measure_point()
        if result:
            rssi, perc = result
            self.measurements_map.update_map_with_rssi_values(id, rssi, perc)

    def get_map_with_rssi_values(self) -> plt.Figure:
        return self.map_plotter.create_map_with_rssi_values()

    def save_plot(self):
        plt.savefig(self.program_data.output_plot)
