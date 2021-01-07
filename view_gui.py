import threading
import tkinter as tk

from queue import Queue
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # type: ignore
import matplotlib.pyplot as plt

from log import logger
from presenter import Presenter
from program_data import ProgramData
from view import View


MAP_UPDATE = 1


class ViewGUI(View):
    def __init__(self, presenter: Presenter):
        super().__init__(presenter)
        self._root = tk.Tk()
        self._queue: Queue = Queue()
        self._check_queue()
        program_data = ProgramData(  # TODO input data from user
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
        self._presenter.set_program_data(program_data)

    def show(self):
        self._root.title("RSSIMapper")
        tabControl = ttk.Notebook(self._root)

        self.tab1 = ttk.Frame(tabControl)
        self.tab2 = ttk.Frame(tabControl)

        tabControl.add(self.tab1, text='Settings')
        tabControl.add(self.tab2, text='Map')
        tabControl.pack(expand=1, fill="both")

        tk.Button(self._root, text="Quit", command=self._root.quit).pack()

        fields = {
            'input_csv': 'example-data.csv',
            'input_shapefile': 'input_map',
            'output_results': 'output_results',
            'output_shapefile': 'map',
            'port': '/dev/pts/3',
            'baudrate': 115200,
            'serial_timeout': 10,
            'measurement_timeout': 100,
            'n_measurements_per_point': 100
        }
        entries = {}
        for field, default_val in fields.items():
            row = tk.Frame(self.tab1)
            lab = tk.Label(row, width=22, text=field, anchor='w')
            ent = tk.Entry(row)
            ent.insert(0, default_val)
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            lab.pack(side=tk.LEFT)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            entries[field] = ent

        print(entries)

        # tk.Button(self.tab1, text="Upload csv", command=self._upload_csv).pack()
        # tk.Button(self.tab1, text="Upload shapefile", command=self._upload_shapefile).pack()

        tk.Button(self.tab1, text="Save", command=self._save_settings).pack()
        # print(port_entry.get())
        self._progress_label = tk.Label(self.tab2)
        self._progress_label.pack()
        self._presenter.update_map()
        self._root.mainloop()

    def render_map(self, figure: plt.Figure):
        try:
            self.canvas.get_tk_widget().pack_forget()
        except AttributeError:
            pass
        self._clear_measurement_progress_label()
        self.canvas: FigureCanvasTkAgg = FigureCanvasTkAgg(figure, master=self.tab2)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.mpl_connect('button_press_event', self._on_map_click)

    def notify_map_updated(self):
        self._queue.put(MAP_UPDATE)

    def _process_incoming_queue_messages(self):
        """Handle all messages currently in the queue, if any.
        """
        while self._queue.qsize():
            try:
                msg = self._queue.get()
                if msg == MAP_UPDATE:
                    self._clear_measurement_progress_label()
                    self._presenter.update_map()
            except self._queue.empty():
                pass

    def _check_queue(self):
        """Check every 200 ms if there is something new in the queue and process incoming messages.
        """
        self._process_incoming_queue_messages()
        self._root.after(200, self._check_queue)

    def _on_map_click(self, event):
        if event.inaxes is not None:
            x = event.xdata
            y = event.ydata
            logger.debug(f"Clicked plot: {x}, {y}")
            self._update_measurement_progress_label()
            self.thread = threading.Thread(
                target=self._presenter.measure_point_by_coordinates,
                args=(x, y,),
                daemon=True
            )
            self.thread.start()
        else:
            logger.debug('Clicked outside axes bounds but inside plot window')

    def _update_measurement_progress_label(self):
        self._progress_label.config(text="Measurement in progress...")

    def _clear_measurement_progress_label(self):
        self._progress_label.config(text="")

    def _upload_csv(self):
        raise NotImplementedError

    def _upload_shapefile(self):
        raise NotImplementedError

    def _save_settings(self):
        raise NotImplementedError
