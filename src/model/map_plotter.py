import matplotlib.pyplot as plt
from matplotlib import ticker  # type: ignore

from src.model.measurements_map import MeasurementsMap


class MapPlotter:
    def __init__(self, map: MeasurementsMap, tick_spacing: int):
        self.map = map
        self.tick_spacing = tick_spacing

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
                return "lightgrey"
            elif rssi < -90:
                return "blue"
            elif rssi < -70:
                return "green"
            elif rssi < -50:
                return "yellow"
            else:
                return "red"

        fig = plt.figure(dpi=150, figsize=(20, 20))
        ax = fig.add_subplot(111)
        ax.set_aspect("equal", adjustable="box")  # type: ignore
        ax.xaxis.set_major_locator(ticker.MultipleLocator(self.tick_spacing))  # type: ignore
        ax.yaxis.set_major_locator(ticker.MultipleLocator(self.tick_spacing))  # type: ignore
        for shaperec in self.map.shape_records:
            x = [i[0] for i in shaperec.shape.points[:]]
            y = [i[1] for i in shaperec.shape.points[:]]
            rssi = shaperec.record["RSSI"]
            plt.fill_between(x, y, color=get_color(rssi), lw=0.5, edgecolor="white")
            if rssi:
                plt.annotate(  # type: ignore
                    rssi,
                    ((max(x) + min(x)) / 2, (max(y) + min(y)) / 2),
                    ha="center",
                    va="center",
                )
        return fig

    def create_map_with_percent_values(self) -> plt.Figure:
        def get_color(perc: int) -> str:
            if perc == 0:
                return "lightgrey"
            elif perc < 40:
                return "blue"
            elif perc < 60:
                return "green"
            elif perc < 80:
                return "yellow"
            else:
                return "red"

        fig = plt.figure(dpi=150, figsize=(20, 20))
        ax = fig.add_subplot(111)
        ax.set_aspect("equal", adjustable="box")  # type: ignore
        ax.xaxis.set_major_locator(ticker.MultipleLocator(self.tick_spacing))  # type: ignore
        ax.yaxis.set_major_locator(ticker.MultipleLocator(self.tick_spacing))  # type: ignore
        for shaperec in self.map.shape_records:
            x = [i[0] for i in shaperec.shape.points[:]]
            y = [i[1] for i in shaperec.shape.points[:]]
            perc = shaperec.record["PERC"]
            plt.fill_between(x, y, color=get_color(perc), lw=0.5, edgecolor="white")
            if perc:
                plt.annotate(f"{perc}%", ((max(x) + min(x)) / 2, (max(y) + min(y)) / 2), ha="center")  # type: ignore
        return fig
