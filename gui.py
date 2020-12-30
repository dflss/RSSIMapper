import tkinter as tk
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # type: ignore

from shapefile_manager import ShapefileManager


def on_click(event):
    if event.inaxes is not None:
        print(event.xdata, event.ydata)
    else:
        print('Clicked ouside axes bounds but inside plot window')


shapefile_man = ShapefileManager()
shapefile_man.write_output_map('input_map', 'map')
# ids = shapefile_man.read_input('input_map')
fig = shapefile_man.read_output_rssi('map')
root = tk.Tk()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
canvas.mpl_connect('button_press_event', on_click)
tk.Button(root, text="Quit", command=root.quit).pack()
root.mainloop()