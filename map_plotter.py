import matplotlib.pyplot as plt

from measurements_map import MeasurementsMap


class MapPlotter:
    def __init__(self, map: MeasurementsMap):
        self.map = map

    def create_raw_map(self) -> plt.Figure:
        fig = plt.figure()
        for shape in self.map.shape_records:
            x = [i[0] for i in shape.shape.points[:]]
            y = [i[1] for i in shape.shape.points[:]]
            plt.plot(x, y)
        return fig

    def create_map_with_rssi_values(self) -> plt.Figure:
        def get_color(rssi: int) -> str:
            if rssi == 0:
                return 'white'
            elif rssi < -90:
                return 'blue'
            elif rssi < -70:
                return 'green'
            elif rssi < -50:
                return 'yellow'
            else:
                return 'red'

        fig = plt.figure()
        for shaperec in self.map.shape_records:
            x = [i[0] for i in shaperec.shape.points[:]]
            y = [i[1] for i in shaperec.shape.points[:]]
            plt.fill_between(x, y, color=get_color(shaperec.record['RSSI']), lw=0.5, edgecolor='black')
        return fig

    def create_map_with_percent_values(self) -> plt.Figure:
        def get_color(perc: int) -> str:
            if perc == 0:
                return 'white'
            elif perc < 40:
                return 'blue'
            elif perc < 60:
                return 'green'
            elif perc < 80:
                return 'yellow'
            else:
                return 'red'

        fig = plt.figure()
        for shaperec in self.map.shape_records:
            x = [i[0] for i in shaperec.shape.points[:]]
            y = [i[1] for i in shaperec.shape.points[:]]
            plt.fill_between(x, y, color=get_color(shaperec.record['PERC']), lw=0.5, edgecolor='black')
        return fig
