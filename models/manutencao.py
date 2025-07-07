class Manutencao:
    def __init__(self, descricao, data, custo, tipo, veiculo_placa, user_id=None):
        self.descricao = descricao
        self.data = data
        self.custo = custo
        self.tipo = tipo
        self.veiculo_placa = veiculo_placa
        self.user_id = user_id
        
    def to_dict(self):
        return {
            'descricao': self.descricao,
            'data': self.data,
            'custo': self.custo,
            'tipo': self.tipo,
            'veiculo_placa': self.veiculo_placa,
            'user_id': self.user_id
        }