from typing import Optional

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # type: ignore
from shapefile_manager import ShapefileManager

import tkinter as tk


root = tk.Tk()
canvas = None
rects = []


def refresh_plot(shapefile_man):
    global rects
    rects, fig = shapefile_man.read_output_rssi('map')
    global canvas
    try:
        canvas.get_tk_widget().pack_forget()
    except AttributeError:
        pass
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas.mpl_connect('button_press_event', on_click)


def measure_point(id):
    result = (-50, 90)
    if result:
        rssi, perc = result
        shapefile_man = ShapefileManager()
        shapefile_man.update_map_with_rssi_data('map', id, int(rssi), int(perc))
        refresh_plot(shapefile_man)


def find_point_id(x: int, y: int) -> Optional[int]:
    for rect in rects:
        print(rect)
        if x > min(rect.x) and x < max(rect.x) and y > min(rect.y) and y < max(rect.y):
            return rect.id
    return None


def on_click(event):
    if event.inaxes is not None:
        x = event.xdata
        y = event.ydata
        print(x, y)
        id = find_point_id(x, y)
        if id is not None:
            measure_point(id)
    else:
        print('Clicked ouside axes bounds but inside plot window')


def main():
    shapefile_man = ShapefileManager()
    shapefile_man.write_output_map('input_map', 'map')
    tk.Button(root, text="Quit", command=root.quit).pack()
    refresh_plot(shapefile_man)
    root.mainloop()


if __name__ == '__main__':
    main()