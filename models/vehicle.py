import os
import json

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

class Vehicle:
    def __init__(self, user_id, name, health):
        self.user_id = user_id
        self.name = name
        self.health = health

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Vehicle(**data)

class VehicleModel:
    FILE_PATH = os.path.join(DATA_DIR, 'vehicles.json')

    def __init__(self):
        self.vehicles = self._load()

    def _load(self):
        if not os.path.exists(self.FILE_PATH):
            return []
        with open(self.FILE_PATH, 'r', encoding='utf-8') as f:
            return [Vehicle.from_dict(item) for item in json.load(f)]

    def get_by_user(self, user_id):
        return next((v for v in self.vehicles if v.user_id == user_id), None)