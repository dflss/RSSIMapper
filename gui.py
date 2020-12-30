from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # type: ignore
from shapefile_manager import ShapefileManager

import tkinter as tk


root = tk.Tk()
canvas = None


def refresh_plot(shapefile_man):
    ids, fig = shapefile_man.read_output_rssi('map')
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


def on_click(event):
    if event.inaxes is not None:
        print(event.xdata, event.ydata)
        measure_point(1)
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