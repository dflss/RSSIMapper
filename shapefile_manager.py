import matplotlib.pyplot as plt
import shapefile as shp  # type: ignore
import seaborn as sns  # type: ignore
import pandas as pd


class ShapefileManager:

    def write(self, csv: str, shapefile: str):
        data = pd.read_csv(csv)
        with shp.Writer(shapefile) as w:
            w.field('X', 'F', 10, 8)
            w.field('Y', 'F', 10, 8)
            w.field('ID', 'N')
            for i, point in data.iterrows():
                w.point(point.x, point.y)  # type: ignore
                w.record(point.x, point.y, point.id)  # type: ignore

    def read(self, filename: str):
        sf = shp.Reader(filename)
        x_values = []
        y_values = []
        for shape in sf.shapeRecords():
            x = shape.shape.points[0][0]
            y = shape.shape.points[0][1]
            x_values.append(x)
            y_values.append(y)
        data = pd.DataFrame({'x': x_values, 'y': y_values})
        sns.scatterplot(x="x", y="y", data=data, palette="coolwarm")
        plt.show()
