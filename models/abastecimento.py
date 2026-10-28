class Abastecimento:
    """Representa um registro de abastecimento de combustível."""

    def __init__(
        self,
        car_id,
        data,
        km,
        combustivel,
        litros,
        valor_total,
        id=None,
        posto="",
        tanque_cheio=True,
    ):
        self.id = int(id) if id is not None else None
        self.car_id = int(car_id) if car_id is not None else None
        self.data = (data or "").strip()
        self.km = max(0, int(float(km or 0)))
        self.combustivel = (combustivel or "Gasolina").strip()
        self.litros = round(max(0.01, float(litros or 1.0)), 2)
        self.valor_total = round(max(0.0, float(valor_total or 0.0)), 2)
        self.posto = (posto or "").strip()
        self.tanque_cheio = bool(tanque_cheio)

    @property
    def preco_litro(self) -> float:
        if self.litros <= 0:
            return 0.0
        return round(self.valor_total / self.litros, 2)

    def to_dict(self) -> dict:
        data = {
            "id": self.id,
            "car_id": self.car_id,
            "data": self.data,
            "km": self.km,
            "combustivel": self.combustivel,
            "litros": self.litros,
            "valor_total": self.valor_total,
            "preco_litro": self.preco_litro,
            "posto": self.posto,
            "tanque_cheio": self.tanque_cheio,
        }
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Abastecimento":
        return cls(
            id=data.get("id"),
            car_id=data.get("car_id"),
            data=data.get("data", ""),
            km=data.get("km", 0),
            combustivel=data.get("combustivel", "Gasolina"),
            litros=data.get("litros", 1.0),
            valor_total=data.get("valor_total", 0.0),
            posto=data.get("posto", ""),
            tanque_cheio=data.get("tanque_cheio", True),
        )
