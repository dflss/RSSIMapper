from typing import List

import matplotlib.pyplot as plt
import shapefile as shp  # type: ignore
# import seaborn as sns  # type: ignore
import pandas as pd


class ShapefileManager:

    def write_input_map(self, csv: str, input_shapefile: str):
        data = pd.read_csv(csv)
        with shp.Writer(input_shapefile, shapeType=shp.POLYGON) as w:
            w.field('ID', 'N')
            for i, polygon in data.iterrows():
                w.poly([[
                    [polygon['x1'], polygon['y1']],
                    [polygon['x2'], polygon['y2']],
                    [polygon['x3'], polygon['y3']],
                    [polygon['x4'], polygon['y4']],
                    [polygon['x1'], polygon['y1']],
                ]])
                w.record(polygon['id'])

    def write_output_map(self, input_shapefile: str, output_shapefile: str):
        with shp.Reader(input_shapefile) as r:
            with shp.Writer(output_shapefile, shapeType=shp.POLYGON) as w:
                w.field('ID', 'N')
                w.field('RSSI', 'N')
                w.field('PERC', 'N')
                for shaperec in r.iterShapeRecords():
                    w.record(shaperec.record['ID'], 0, 0)
                    w.shape(shaperec.shape)

    def read_input(self, filename: str) -> List[int]:
        with shp.Reader(filename) as sf:
            ids = []
            plt.figure()
            for shape in sf.shapeRecords():
                x = [i[0] for i in shape.shape.points[:]]
                y = [i[1] for i in shape.shape.points[:]]
                plt.plot(x, y)
            for rec in sf.records():
                ids.append(rec['ID'])
            plt.show()
            return ids

    def read_output_rssi(self, filename: str):
        def get_color(rssi):
            if rssi == 0:
                return 'grey'
            if rssi < -90:
                return 'blue'
            elif rssi < -70:
                return 'green'
            elif rssi < -50:
                return 'yellow'
            else:
                return 'red'

        with shp.Reader(filename) as sf:
            fig = plt.figure()
            for shaperec in sf.shapeRecords():
                x = [i[0] for i in shaperec.shape.points[:]]
                y = [i[1] for i in shaperec.shape.points[:]]
                plt.fill_between(x, y, color=get_color(shaperec.record['RSSI']))
                print(shaperec.record['ID'], shaperec.record['RSSI'], shaperec.record['PERC'])

        return fig

    def read_output_perc(self, filename: str):
        def get_color(perc):
            if perc < 40:
                return 'blue'
            elif perc < 60:
                return 'green'
            elif perc < 80:
                return 'yellow'
            else:
                return 'red'
        with shp.Reader(filename) as sf:
            plt.figure()
            for shaperec in sf.shapeRecords():
                x = [i[0] for i in shaperec.shape.points[:]]
                y = [i[1] for i in shaperec.shape.points[:]]
                plt.fill_between(x, y, color=get_color(shaperec.record['PERC']))
                print(shaperec.record['ID'], shaperec.record['RSSI'], shaperec.record['PERC'])
            plt.show()

    def update_map_with_rssi_data(self, shapefile: str, id: int, rssi: int, perc: int):
        print(f"Update id {id} with RSSI {rssi} and {perc}%")
        with shp.Reader(shapefile) as r:
            records = list(r.iterShapeRecords())
        with shp.Writer(shapefile, shapeType=shp.POLYGON) as w:
            w.field('ID', 'N')
            w.field('RSSI', 'N')
            w.field('PERC', 'N')
            for shaperec in records:
                if shaperec.record['ID'] == id:
                    w.record(id, rssi, perc)
                else:
                    w.record(shaperec.record['ID'], shaperec.record['RSSI'], shaperec.record['PERC'])
                w.shape(shaperec.shape)
