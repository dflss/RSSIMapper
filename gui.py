from typing import Optional

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # type: ignore
from shapefile_manager import ShapefileManager

import tkinter as tk


class Gui:
    def __init__(self):
        self.root = tk.Tk()
        self.canvas = None
        self.polygons = []
        self.shapefile_man = ShapefileManager()
        self.shapefile_man.write_output_map('input_map', 'map')
        tk.Button(self.root, text="Quit", command=self.root.quit).pack()
        tk.Button(self.root, text="Upload csv", command=self.upload_csv).pack()
        tk.Button(self.root, text="Upload shapefile", command=self.upload_shapefile).pack()
        self.refresh_plot()
        self.root.mainloop()

    def refresh_plot(self):
        self.polygons, fig = self.shapefile_man.read_output_rssi('map')
        try:
            self.canvas.get_tk_widget().pack_forget()
        except AttributeError:
            pass
        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.mpl_connect('button_press_event', self.on_click)

    def measure_point(self, id: int):
        result = (-50, 90)
        if result:
            rssi, perc = result
            self.shapefile_man.update_map_with_rssi_data('map', id, int(rssi), int(perc))
            self.refresh_plot()

    def find_point_id(self, x: int, y: int) -> Optional[int]:
        for poly in self.polygons:
            if x > min(poly.x) and x < max(poly.x) and y > min(poly.y) and y < max(poly.y):
                return poly.id
        return None

    def upload_csv(self):
        pass

    def upload_shapefile(self):
        pass

    def on_click(self, event):
        if event.inaxes is not None:
            x = event.xdata
            y = event.ydata
            id = self.find_point_id(x, y)
            if id is not None:
                self.measure_point(id)
        else:
            print('Clicked ouside axes bounds but inside plot window')


def main():
    Gui()


if __name__ == '__main__':
    main()