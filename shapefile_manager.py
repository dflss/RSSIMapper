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
        r = shp.Reader(input_shapefile)
        with shp.Writer(output_shapefile, shapeType=shp.POLYGON) as w:
            w.field('ID', 'N')
            w.field('RSSI', 'N')
            w.field('PERC', 'N')
            print(w.fields)
            for shaperec in r.iterShapeRecords():
                w.record(shaperec.record['ID'], 0, 0)
                w.shape(shaperec.shape)

    def read(self, filename: str) -> List[int]:
        sf = shp.Reader(filename)
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

    def read_output(self, filename: str):
        sf = shp.Reader(filename)
        plt.figure()
        for shape in sf.shapeRecords():
            x = [i[0] for i in shape.shape.points[:]]
            y = [i[1] for i in shape.shape.points[:]]
            plt.plot(x, y)
        for rec in sf.records():
            print(rec['ID'])
            print(rec['RSSI'])
            print(rec['PERC'])
        plt.show()

    def update_map_with_rssi_data(self, shapefile: str, id: int, rssi: int, perc: int):
        print(f"Update id {id} with RSSI {rssi} and {perc}%")
