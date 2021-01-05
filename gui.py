import threading
import logging
from queue import Queue
from typing import Optional

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # type: ignore

from map_plotter import MapPlotter
from measurements_manager import MeasurementsManager
from measurements_map import MeasurementsMap
from program_data import ProgramData
from serial_connection import SerialConnection
from shapefile_manager import ShapefileManager

import tkinter as tk


class GUI:
    def __init__(self):
        self.init_program_data()
        self.init_ui()

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

    def init_ui(self):
        self.root = tk.Tk()
        self.queue = Queue()
        self.canvas = None
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
        shapefile_mgr = \
            ShapefileManager(
                self.program_data.input_shapefile,
                self.program_data.output_shapefile,
                self.program_data.input_csv
            )
        self.measurements_map = MeasurementsMap(shapefile_mgr.read_shapefile())
        self.map_plotter = MapPlotter(self.measurements_map)
        tk.Button(self.root, text="Quit", command=self.root.quit).pack()
        tk.Button(self.root, text="Upload csv", command=self.upload_csv).pack()
        tk.Button(self.root, text="Upload shapefile", command=self.upload_shapefile).pack()
        self.progress_label = tk.Label(self.root, text='text')
        self.progress_label.pack()
        self.refresh_plot()
        self.check_queue()
        self.root.mainloop()

    def process_incoming_queue_messages(self):
        """Handle all messages currently in the queue, if any.
        """
        while self.queue.qsize():
            try:
                msg = self.queue.get()
                self.progress_label.config(text="")
                id, (rssi, perc) = msg
                self.measurements_map.update_map_with_rssi_values(id, int(rssi), int(perc))
                self.refresh_plot()
            except self.queue.empty():
                pass

    def check_queue(self):
        """Check every 200 ms if there is something new in the queue.
        """
        self.process_incoming_queue_messages()
        self.root.after(200, self.check_queue)

    def refresh_plot(self):
        fig = self.map_plotter.display_with_rssi_values()
        try:
            self.canvas.get_tk_widget().pack_forget()
        except AttributeError:
            pass
        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.mpl_connect('button_press_event', self.on_click)

    def measure_point(self, id: int):
        logging.debug(f"Measurement started for point {id}")
        self.progress_label.config(text=f"Measurement started for point {id}")
        result = self.measurements_mgr.measure_point()
        if result:
            self.queue.put((id, result))

    def find_point_id(self, x: int, y: int) -> Optional[int]:
        for record in self.measurements_map.records:
            if x > min(record.x) and x < max(record.x) and y > min(record.y) and y < max(record.y):
                return record.id
        return None

    def upload_csv(self):
        # TODO
        pass

    def upload_shapefile(self):
        # TODO
        pass

    def on_click(self, event):
        if event.inaxes is not None:
            x = event.xdata
            y = event.ydata
            print(x, y)
            id = self.find_point_id(x, y)
            if id is not None:
                self.thread = threading.Thread(target=self.measure_point, args=(id,), daemon=True)
                self.thread.start()
        else:
            logging.debug('Clicked ouside axes bounds but inside plot window')


def main():
    GUI()


if __name__ == '__main__':
    main()
