from dataclasses import dataclass
from typing import List

import shapefile as shp  # type: ignore

from src.log import logger


@dataclass
class Record:
    id: int
    x: list
    y: list


class MeasurementsMap:
    def __init__(self, shape_records: List[shp.ShapeRecord]):
        self.shape_records = shape_records
        self.ids = self._get_shapefile_ids()
        self.records = self._get_shapefile_records()

    def _get_shapefile_ids(self) -> List[int]:
        ids = []
        for shaperec in self.shape_records:
            ids.append(shaperec.record['ID'])
        return ids

    def _get_shapefile_records(self) -> List[Record]:
        records = []
        for shaperec in self.shape_records:
            x = [i[0] for i in shaperec.shape.points[:]]
            y = [i[1] for i in shaperec.shape.points[:]]
            records.append(Record(shaperec.record['ID'], x, y))
        return records

    def find_point_id(self, x: int, y: int) -> int:
        for record in self.records:
            if min(record.x) < x < max(record.x) and min(record.y) < y < max(record.y):
                return record.id
        raise ValueError(f"No id found for given coordinates ({x},{y})")

    def update_map_with_rssi_values(self, id: int, rssi: float, perc: float) -> shp.ShapeRecord:
        logger.debug(f"Update id {id} with RSSI {rssi} and {perc}%")
        for shaperec in self.shape_records:
            if shaperec.record['ID'] == id:
                shaperec.record['RSSI'] = rssi
                shaperec.record['PERC'] = perc
                return shaperec
        raise IndexError(f"Given id ({id}) was not found")
