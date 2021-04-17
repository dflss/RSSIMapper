import logging
import time
from typing import Optional

import serial  # type: ignore


class SerialConnection:
    def __init__(self, port: str, baudrate: int, timeout: int):
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.baudrate = baudrate
        self.ser.timeout = timeout
        self.ser.setDTR(1)
        try:
            self.ser.open()
            # self.ser.write(b'\r\n')
            self.ser.flushInput()
            self.ser.flushOutput()
            time.sleep(0.1)
        except Exception as e:
            logging.error(f"Exception occurred: {e}", exc_info=True)
        logging.info(self.ser)

    def __del__(self):
        self.ser.close()

    def read(self) -> Optional[str]:
        if not self.ser.is_open:
            logging.warning("Serial is closed. Is the device connected?")
            raise serial.SerialException
        bytes_to_read = self.ser.inWaiting()
        text_read = self.ser.read(bytes_to_read).decode(encoding="utf-8")
        return text_read
