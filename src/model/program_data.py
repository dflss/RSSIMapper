from dataclasses import dataclass


@dataclass
class ProgramData:
    input_csv: str
    input_shapefile: str
    output_results: str
    output_shapefile: str
    output_plot: str
    port: str
    baudrate: int
    serial_timeout: int
    measurement_timeout: int
    n_measurements_per_point: int
