class Manutencao:

    def __init__(self, descricao_servico, data, custo, tipo_manutencao, id_veiculo):
        self._descricao_do_servico = descricao_servico
        self._data = data
        self._custo = custo
        self._tipo_manutencao = tipo_manutencao
        self._id_veiculo = id_veiculo

    def __str__(self):
        return (
            f"Descrição do Serviço: {self._descricao_do_servico}\n"
            f"Data: {self._data}\n"
            f"Custo: R${self._custo}\n"
            f"Tipo de Manutenção: {self._tipo_manutencao}\n"
        )

    def detalhar_servico(self):
        return str(self)
