import logging
from typing import List

import matplotlib.pyplot as plt
import shapefile as shp  # type: ignore


class MeasurementsMap:
    def __init__(self, shapeRecords: List[shp.ShapeRecord]):
        self.shapeRecords = shapeRecords
        self.ids = self._get_shapefile_ids()

    def _get_shapefile_ids(self) -> List[int]:
        ids = []
        for shaperec in self.shapeRecords:
            ids.append(shaperec.record['ID'])
        return ids

    def update_map_with_rssi_values(self, id: int, rssi: int, perc: int) -> shp.ShapeRecord:
        logging.debug(f"Update id {id} with RSSI {rssi} and {perc}%")
        for shaperec in self.shapeRecords:
            if shaperec.record['ID'] == id:
                shaperec.record['RSSI'] = rssi
                shaperec.record['PERC'] = perc
                return shaperec

    def display_map(self):
        plt.figure()
        for shape in self.shapeRecords:
            x = [i[0] for i in shape.shape.points[:]]
            y = [i[1] for i in shape.shape.points[:]]
            plt.plot(x, y)
        plt.show()

    def display_map_with_rssi_values(self):
        def get_color(rssi):
            if rssi < -90:
                return 'blue'
            elif rssi < -70:
                return 'green'
            elif rssi < -50:
                return 'yellow'
            else:
                return 'red'

        plt.figure()
        for shaperec in self.shapeRecords:
            x = [i[0] for i in shaperec.shape.points[:]]
            y = [i[1] for i in shaperec.shape.points[:]]
            plt.fill_between(x, y, color=get_color(shaperec.record['RSSI']))
            print(shaperec.record['ID'], shaperec.record['RSSI'], shaperec.record['PERC'])
        plt.show()

    def display_map_with_percent_values(self):
        def get_color(perc):
            if perc < 40:
                return 'blue'
            elif perc < 60:
                return 'green'
            elif perc < 80:
                return 'yellow'
            else:
                return 'red'

        plt.figure()
        for shaperec in self.shapeRecords:
            x = [i[0] for i in shaperec.shape.points[:]]
            y = [i[1] for i in shaperec.shape.points[:]]
            plt.fill_between(x, y, color=get_color(shaperec.record['PERC']))
            print(shaperec.record['ID'], shaperec.record['RSSI'], shaperec.record['PERC'])
        plt.show()
