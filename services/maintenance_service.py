from models.maintenance import MaintenanceModel, Maintenance
from bottle import request

class MaintenanceService:
    def __init__(self):
        self.model = MaintenanceModel()

    def get_by_user(self, user_id):
        return self.model.get_by_user(user_id)

    def add(self, user_id):
        vehicle = request.forms.get('vehicle')
        description = request.forms.get('description')
        date = request.forms.get('date')
        cost = request.forms.get('cost')
        mtype = request.forms.get('maintenance_type')

        last_id = max([m.id for m in self.model.maintenances], default=0)
        new_maintenance = Maintenance(id=last_id + 1, user_id=user_id,
                                      vehicle=vehicle, description=description,
                                      date=date, cost=cost, maintenance_type=mtype)
        self.model.add(new_maintenance)