import os
import json

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

class Maintenance:
    def __init__(self, id, user_id, vehicle, description, date, cost, maintenance_type):
        self.id = id
        self.user_id = user_id
        self.vehicle = vehicle
        self.description = description
        self.date = date
        self.cost = cost
        self.maintenance_type = maintenance_type

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Maintenance(**data)

class MaintenanceModel:
    FILE_PATH = os.path.join(DATA_DIR, 'maintenances.json')

    def __init__(self):
        self.maintenances = self._load()

    def _load(self):
        if not os.path.exists(self.FILE_PATH):
            return []
        with open(self.FILE_PATH, 'r', encoding='utf-8') as f:
            return [Maintenance.from_dict(item) for item in json.load(f)]

    def _save(self):
        with open(self.FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump([m.to_dict() for m in self.maintenances], f, indent=4)

    def get_by_user(self, user_id):
        return [m for m in self.maintenances if m.user_id == user_id]

    def add(self, maintenance):
        self.maintenances.append(maintenance)
        self._save()