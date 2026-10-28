class Manutencao:
    """Representa um serviço de manutenção realizado em um veículo."""

    def __init__(
        self,
        descricao,
        data,
        custo,
        tipo,
        km,
        car_id,
        id=None,
        oficina="",
        garantia_meses=0,
        observacoes="",
    ):
        self.id = int(id) if id is not None else None
        self.car_id = int(car_id) if car_id is not None else None
        self.descricao = (descricao or "").strip()
        self.data = (data or "").strip()
        self.custo = round(max(0.0, float(custo or 0.0)), 2)
        self.tipo = (tipo or "Preventiva").strip().title()
        self.km = max(0, int(float(km or 0)))
        self.oficina = (oficina or "").strip()
        self.garantia_meses = max(0, int(float(garantia_meses or 0)))
        self.observacoes = (observacoes or "").strip()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "car_id": self.car_id,
            "descricao": self.descricao,
            "data": self.data,
            "custo": self.custo,
            "tipo": self.tipo,
            "km": self.km,
            "oficina": self.oficina,
            "garantia_meses": self.garantia_meses,
            "observacoes": self.observacoes,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Manutencao":
        return cls(
            id=data.get("id"),
            car_id=data.get("car_id"),
            descricao=data.get("descricao") or data.get("descricao_servico", ""),
            data=data.get("data", ""),
            custo=data.get("custo", 0.0),
            tipo=data.get("tipo") or data.get("tipo_manutencao", "Preventiva"),
            km=data.get("km", 0),
            oficina=data.get("oficina", ""),
            garantia_meses=data.get("garantia_meses", 0),
            observacoes=data.get("observacoes", ""),
        )

    def __repr__(self) -> str:
        return f"Manutencao(id={self.id}, car_id={self.car_id}, descricao='{self.descricao}', custo={self.custo})"
