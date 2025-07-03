import os
import json

class ManutencaoProgramada:
    def __init__(self, descricao, frequencia_dias, ultima_data, id_veiculo):
        self._descricao = descricao
        self._frequencia_dias = frequencia_dias
        self._ultima_data = ultima_data  # Quando foi feita pela última vez
        self._id_veiculo = id_veiculo

    def to_dict(self):
        return {
            "descricao": self._descricao,
            "frequencia_dias": self._frequencia_dias,
            "ultima_data": self._ultima_data,
            "id_veiculo": self._id_veiculo
        }

    def detalhar_servico(self):
        return str(self)

    def __str__(self):
        return (
            f"{self._descricao} - cada {self._frequencia_dias} dias "
            f"(última: {self._ultima_data})"
        )

# Caminho dos dados
DATA_DIR = "./data"

class ManutencaoProgramadaModel:
    FILE_PATH = os.path.join(DATA_DIR, "manutencoes_programadas.json")

    def __init__(self):
        self.manutencoes = self._load()

    def _load(self):
        if not os.path.exists(self.FILE_PATH) or os.path.getsize(self.FILE_PATH) == 0:
            return []
        with open(self.FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [ManutencaoProgramada(**item) for item in data]

    def _save(self):
        with open(self.FILE_PATH, "w", encoding="utf-8") as f:
            json.dump([m.to_dict() for m in self.manutencoes], f, indent=4, ensure_ascii=False)

    def get_all(self):
        return self.manutencoes

    def get_by_veiculo(self, id_veiculo: str):
        """Retorna todas as manutenções programadas de um veículo."""
        return [m for m in self.manutencoes if m._id_veiculo == id_veiculo]

    def add_manutencao(self, manutencao: ManutencaoProgramada):
        self.manutencoes.append(manutencao)
        self._save()

    def delete_manutencao(self, index: int):
        """Remove manutenção pelo índice na lista."""
        if 0 <= index < len(self.manutencoes):
            del self.manutencoes[index]
            self._save()
