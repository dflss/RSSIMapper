import threading
import tkinter as tk
from queue import Queue
from typing import Optional

from log import logger
from map_plotter import MapPlotter
from measurements_manager import MeasurementsManager
from measurements_map import MeasurementsMap
from program_data import ProgramData
from serial_connection import SerialConnection
from shapefile_manager import ShapefileManager
from view import View


class Controller:
    def __init__(self):
        self.init_program_data()
        self.serial_conn = \
            SerialConnection(
                port=self.program_data.port,
                baudrate=self.program_data.baudrate,
                timeout=self.program_data.serial_timeout
            )
        self.measurements_mgr = \
            MeasurementsManager(
                serial_conn=self.serial_conn,
                points_number=self.program_data.n_points,
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
        self.root = tk.Tk()
        self.view = View(self.root)
        self.queue = Queue()
        self.check_queue()
        self.refresh_plot()
        self.root.mainloop()

    def init_program_data(self):
        self.program_data = \
            ProgramData(  # TODO input data from user
                'example-data.csv',
                'input_map',
                'output_results',
                'map',
                '/dev/pts/3',
                115200,
                10,
                100,
                100
            )

    def process_incoming_queue_messages(self):
        """Handle all messages currently in the queue, if any.
        """
        while self.queue.qsize():
            try:
                msg = self.queue.get()
                self.view.clear_measurement_progress_label()
                id, (rssi, perc) = msg
                self.measurements_map.update_map_with_rssi_values(id, int(rssi), int(perc))
                self.refresh_plot()
            except self.queue.empty():
                pass

    def check_queue(self):
        """Check every 200 ms if there is something new in the queue and process incoming messages.
        """
        self.process_incoming_queue_messages()
        self.root.after(200, self.check_queue)

    def refresh_plot(self):
        fig = self.map_plotter.display_with_rssi_values()
        self.view.refresh_plot(fig, self.on_map_click)

    def find_point_id(self, x: int, y: int) -> Optional[int]:
        for record in self.measurements_map.records:
            if x > min(record.x) and x < max(record.x) and y > min(record.y) and y < max(record.y):
                return record.id
        return None

    def measure_point(self, id: int):
        logger.debug(f"Measurement started for point {id}")
        self.view.update_measurement_progress_label(id)
        result = self.measurements_mgr.measure_point()
        if result:
            self.queue.put((id, result))

    def on_map_click(self, event):
        if event.inaxes is not None:
            x = event.xdata
            y = event.ydata
            logger.debug(f"Clicked plot: {x}, {y}")
            id = self.find_point_id(x, y)
            if id is not None:
                self.thread = threading.Thread(target=self.measure_point, args=(id,), daemon=True)
                self.thread.start()
        else:
            logger.debug('Clicked outside axes bounds but inside plot window')
