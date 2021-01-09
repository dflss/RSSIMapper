import matplotlib.pyplot as plt

from src.model.map_plotter import MapPlotter
from src.model.measurements_manager import MeasurementsManager
from src.model.measurements_map import MeasurementsMap
from src.model.program_data import ProgramData
from src.model.serial_connection import SerialConnection
from src.model.shapefile_manager import ShapefileManager


class Model:
    def set_program_data(self, program_data: ProgramData):
        self.program_data = program_data
        self.serial_conn = \
            SerialConnection(
                port=self.program_data.port,
                baudrate=self.program_data.baudrate,
                timeout=self.program_data.serial_timeout
            )
        self.measurements_mgr = \
            MeasurementsManager(
                serial_conn=self.serial_conn,
                points_number=self.program_data.n_measurements_per_point,
                timeout=self.program_data.measurement_timeout
            )
        self.shapefile_mgr = \
            ShapefileManager(
                self.program_data.input_shapefile,
                self.program_data.output_shapefile,
                self.program_data.input_csv
            )
        self.measurements_map = MeasurementsMap(self.shapefile_mgr.read_shapefile())
        self.map_plotter = MapPlotter(self.measurements_map)

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
