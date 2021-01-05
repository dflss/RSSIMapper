from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # type: ignore

import tkinter as tk


class View:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.canvas = None
        tk.Button(master, text="Quit", command=master.quit).pack()
        tk.Button(master, text="Upload csv", command=self.upload_csv).pack()
        tk.Button(master, text="Upload shapefile", command=self.upload_shapefile).pack()
        self.progress_label = tk.Label(master)
        self.progress_label.pack()

    def refresh_plot(self, fig, on_click):
        try:
            self.canvas.get_tk_widget().pack_forget()
        except AttributeError:
            pass
        self.canvas = FigureCanvasTkAgg(fig, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.mpl_connect('button_press_event', on_click)

    def update_measurement_progress_label(self, id):
        self.progress_label.config(text=f"Measurement started for point {id}")

    def clear_measurement_progress_label(self):
        self.progress_label.config(text="")

    def upload_csv(self):
        # TODO
        pass

    def upload_shapefile(self):
        # TODO
        pass
