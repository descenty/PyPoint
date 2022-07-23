from dataclasses import dataclass


@dataclass()
class Coord:
    latitude: float
    longitude: float


vehicle_coords: dict = {}
