import logging
from typing import List

import shapefile as shp  # type: ignore


class MeasurementsMap:
    def __init__(self, shape_records: List[shp.ShapeRecord]):
        self.shape_records = shape_records
        self.ids = self._get_shapefile_ids()

    def _get_shapefile_ids(self) -> List[int]:
        ids = []
        for shaperec in self.shape_records:
            ids.append(shaperec.record['ID'])
        return ids

    def update_map_with_rssi_values(self, id: int, rssi: int, perc: int) -> shp.ShapeRecord:
        logging.debug(f"Update id {id} with RSSI {rssi} and {perc}%")
        for shaperec in self.shape_records:
            if shaperec.record['ID'] == id:
                shaperec.record['RSSI'] = rssi
                shaperec.record['PERC'] = perc
                return shaperec
