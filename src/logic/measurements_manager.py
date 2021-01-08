import statistics
import time
from typing import Optional, Tuple, List

from src.utils.log import logger
from src.logic.serial_connection import SerialConnection


class MeasurementsManager:
    def __init__(self, serial_conn: SerialConnection, points_number: int, timeout: int):
        self.serial_conn = serial_conn
        self.points_number = points_number
        self.timeout = timeout

    def measure_point(self) -> Optional[Tuple[float, float]]:
        rssi_values: List[int] = []
        start = time.time()
        while time.time() - start < self.timeout and len(rssi_values) < self.points_number:
            bytes_to_read = self.serial_conn.ser.inWaiting()
            text_read = self.serial_conn.ser.read(bytes_to_read).decode(encoding='utf-8')
            if text_read:
                args = text_read.split(" ")
                for arg in args:
                    if "RSSI" in arg:
                        rssi = arg.split("=")[1].strip()
                        logger.debug(f"Read RSSI value from serial: {rssi}")
                        try:
                            rssi_values.append(int(rssi))
                        except Exception as ex:
                            print(ex)
            time.sleep(0.1)
        try:
            return statistics.mean(rssi_values), (len(rssi_values)/self.points_number)*100
        except statistics.StatisticsError:
            return None
