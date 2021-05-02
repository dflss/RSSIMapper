from src.model.program_data import ProgramData

RSSI_CHOICE = 0
PERCENT_CHOICE = 1
CONFIG_FILE_PATH = "config.ini"
DEFAULT_PROGRAM_DATA = ProgramData(
    "input_data/example-data.csv",
    "input_data/input_map",
    "output_data/output_results",
    "output_data/map",
    "output_data/plot_rssi",
    "output_data/plot_perc",
    "/dev/pts/2",
    115200,
    10,
    100,
    100,
    10
)
