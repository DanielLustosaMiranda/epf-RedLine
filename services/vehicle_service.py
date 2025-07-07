from models.vehicle import VehicleModel

class VehicleService:
    def __init__(self):
        self.model = VehicleModel()

    def get_by_user(self, user_id):
        return self.model.get_by_user(user_id)