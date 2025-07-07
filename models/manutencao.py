class Manutencao:
    def __init__(self, descricao, data, custo, tipo, km, car_id, id=None):
        self.id = id
        self.car_id = car_id
        self.descricao = descricao
        self.data = data
        self.custo = custo
        self.tipo = tipo
        self.km = km