from typing import List

import matplotlib.pyplot as plt
import shapefile as shp  # type: ignore
# import seaborn as sns  # type: ignore
import pandas as pd


class ShapefileManager:

    def write(self, csv: str, shapefile: str):
        data = pd.read_csv(csv)
        with shp.Writer(shapefile, shapeType=shp.POLYGON) as w:
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
