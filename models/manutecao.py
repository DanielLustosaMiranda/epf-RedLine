import os
import json

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
            f"Id Veículo: {self._id_veiculo}\n"
        )

    def detalhar_servico(self):
        return str(self)

    def to_dict(self):
        return {
            "descricao_servico": self._descricao_do_servico,
            "data": self._data,
            "custo": self._custo,
            "tipo_manutencao": self._tipo_manutencao,
            "id_veiculo": self._id_veiculo
        }

DATA_DIR = "./data"

class ManutencaoModel:
    FILE_PATH = os.path.join(DATA_DIR, "manutencoes.json")

    def __init__(self):
        self.manutencoes = self._load()

    def _load(self):
        if not os.path.exists(self.FILE_PATH):
            return []
        with open(self.FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Manutencao(**item) for item in data]

    def _save(self):
        with open(self.FILE_PATH, "w", encoding="utf-8") as f:
            json.dump([m.to_dict() for m in self.manutencoes], f, indent=4, ensure_ascii=False)

    def get_all(self):
        return self.manutencoes

    def get_by_veiculo(self, id_veiculo: int):
        """Retorna todas as manutenções do veículo."""
        return [m for m in self.manutencoes if m._id_veiculo == id_veiculo]

    def add_manutencao(self, manutencao: Manutencao):
        self.manutencoes.append(manutencao)
        self._save()

    def delete_manutencao(self, index: int):
        """Remove manutenção pelo índice na lista."""
        if 0 <= index < len(self.manutencoes):
            del self.manutencoes[index]
            self._save()