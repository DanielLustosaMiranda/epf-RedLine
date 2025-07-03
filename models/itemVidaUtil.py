import os
import json

class ItemVidaUtil:
    def __init__(self, nome_item, data_instalacao, validade_anos, id_veiculo):
        self._nome_item = nome_item
        self._data_instalacao = data_instalacao
        self._validade_anos = validade_anos
        self._id_veiculo = id_veiculo

    def to_dict(self):
        return {
            "nome_item": self._nome_item,
            "data_instalacao": self._data_instalacao,
            "validade_anos": self._validade_anos,
            "id_veiculo": self._id_veiculo
        }

    def __str__(self):
        return (
            f"{self._nome_item} instalado em {self._data_instalacao} "
            f"(validade: {self._validade_anos} anos)"
        )

DATA_DIR = "./data"

class ItemVidaUtilModel:
    FILE_PATH = os.path.join(DATA_DIR, "itens_vida_util.json")

    def __init__(self):
        self.itens = self._load()

    def _load(self):
        if not os.path.exists(self.FILE_PATH) or os.path.getsize(self.FILE_PATH) == 0:
            return []
        with open(self.FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [ItemVidaUtil(**item) for item in data]

    def _save(self):
        with open(self.FILE_PATH, "w", encoding="utf-8") as f:
            json.dump([i.to_dict() for i in self.itens], f, indent=4, ensure_ascii=False)

    def get_all(self):
        return self.itens

    def get_by_veiculo(self, id_veiculo: str):
        """Retorna todos os itens instalados em um veículo."""
        return [i for i in self.itens if i._id_veiculo == id_veiculo]

    def add_item(self, item: "ItemVidaUtil"):
        self.itens.append(item)
        self._save()

    def delete_item(self, index: int):
        """Remove item pelo índice na lista."""
        if 0 <= index < len(self.itens):
            del self.itens[index]
            self._save()
