from typing import List

import shapefile as shp  # type: ignore
import pandas as pd


def create_raw_shapefile_from_csv(csv: str, input_shapefile: str):
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


def create_output_shapefile(input_shapefile: str, output_shapefile: str):
    with shp.Reader(input_shapefile) as r:
        with shp.Writer(output_shapefile, shapeType=shp.POLYGON) as w:
            w.field('ID', 'N')
            w.field('RSSI', 'N')
            w.field('PERC', 'N')
            for shaperec in r.iterShapeRecords():
                w.record(shaperec.record['ID'], 0, 0)
                w.shape(shaperec.shape)


def read_shapefile(shapefile: str) -> List[shp.ShapeRecord]:
    with shp.Reader(shapefile) as r:
        return list(r.iterShapeRecords())


def save_shapefile(shapefile: str, shapeRecords: List[shp.ShapeRecord]):
    with shp.Writer(shapefile, shapeType=shp.POLYGON) as w:
        w.field('ID', 'N')
        w.field('RSSI', 'N')
        w.field('PERC', 'N')
        for shaperec in shapeRecords:
            w.record(shaperec.record['ID'], shaperec.record['RSSI'], shaperec.record['PERC'])
            w.shape(shaperec.shape)
