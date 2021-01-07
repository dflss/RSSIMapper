from typing import List, Optional

import shapefile as shp  # type: ignore
import pandas as pd


class ShapefileManager:
    def __init__(self, input_shapefile_path: str, output_shapefile_path: str, csv_path: Optional[str]):
        self.output_shapefile_path = output_shapefile_path
        if csv_path is not None:
            self._create_raw_shapefile_from_csv(csv_path, input_shapefile_path)
        self._create_output_shapefile(input_shapefile_path)

    def _create_raw_shapefile_from_csv(self, csv_path: str, input_shapefile_path: str):
        data = pd.read_csv(csv_path)
        with shp.Writer(input_shapefile_path, shapeType=shp.POLYGON) as w:
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

    def _create_output_shapefile(self, input_shapefile_path: str):
        with shp.Reader(input_shapefile_path) as r:
            with shp.Writer(self.output_shapefile_path, shapeType=shp.POLYGON) as w:
                w.field('ID', 'N')
                w.field('RSSI', 'N')
                w.field('PERC', 'N')
                for shaperec in r.iterShapeRecords():
                    w.record(shaperec.record['ID'], 0, 0)
                    w.shape(shaperec.shape)

    def read_shapefile(self) -> List[shp.ShapeRecord]:
        with shp.Reader(self.output_shapefile_path) as r:
            return list(r.iterShapeRecords())

    def update_shapefile(self, shape_records: List[shp.ShapeRecord]):
        with shp.Writer(self.output_shapefile_path, shapeType=shp.POLYGON) as w:
            w.field('ID', 'N')
            w.field('RSSI', 'N')
            w.field('PERC', 'N')
            for shaperec in shape_records:
                w.record(shaperec.record['ID'], shaperec.record['RSSI'], shaperec.record['PERC'])
                w.shape(shaperec.shape)
