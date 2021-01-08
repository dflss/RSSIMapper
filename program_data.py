from dataclasses import dataclass


@dataclass
class ProgramData:
    input_csv: str
    input_shapefile: str
    output_results: str
    output_shapefile: str
    port: str
    baudrate: str
    serial_timeout: str
    measurement_timeout: str
    n_measurements_per_point: str
