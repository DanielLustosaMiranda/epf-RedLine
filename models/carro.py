import os
import json

class Carro:
    def __init__(self, usuario, marca, modelo, ano, placa, km_atual):
        self._usuario = usuario
        self._marca = marca
        self._modelo = modelo
        self._ano = ano
        self._placa = placa
        self._km_atual = km_atual

    def __str__(self):
        return (f"Usuario: {self._usuario}, "
                f"Marca: {self._marca}, "
                f"Modelo: {self._modelo}, "
                f"Ano: {self._ano}, "
                f"Placa: {self._placa}, "
                f"KM atual: {self._km_atual}")

    def get_info_completa(self):
        return str(self)

    def to_dict(self):
        """Transforma o objeto em dicionário compatível com JSON e Carro(**item)"""
        return {
            "usuario": self._usuario,
            "marca": self._marca,
            "modelo": self._modelo,
            "ano": self._ano,
            "placa": self._placa,
            "km_atual": self._km_atual
        }

DATA_DIR = "./data"

class CarroModel:
    FILE_PATH = os.path.join(DATA_DIR, "carros.json")

    def __init__(self):
        self.carros = self._load()
    
    def _load(self):
        if not os.path.exists(self.FILE_PATH):
            return []
        if os.path.getsize(self.FILE_PATH) == 0:
            return []
        with open(self.FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Carro(**item) for item in data]

    def _save(self):
        with open(self.FILE_PATH, "w", encoding="utf-8") as f:
            json.dump([c.to_dict() for c in self.carros], f, indent=4, ensure_ascii=False)

    def get_all(self):
        return self.carros

    def get_by_placa(self, placa: str):
        return next((c for c in self.carros if c._placa == placa), None)

    def add_carro(self, carro: "Carro"):
        self.carros.append(carro)
        self._save()

    def update_carro(self, updated_carro: "Carro"):
        for i, carro in enumerate(self.carros):
            if carro._placa == updated_carro._placa:
                self.carros[i] = updated_carro
                self._save()
                break

    def delete_carro(self, placa: str):
        self.carros = [c for c in self.carros if c._placa != placa]
        self._save()

