class Carro:
    """Representa um veículo cadastrado pelo usuário."""

    def __init__(
        self,
        marca,
        modelo,
        ano,
        placa,
        km_atual,
        user_id,
        id=None,
        combustivel="Flex",
        cor="",
        apelido="",
        observacoes="",
    ):
        self.id = int(id) if id is not None else None
        self.user_id = int(user_id) if user_id is not None else None
        self.marca = (marca or "").strip().title()
        self.modelo = (modelo or "").strip()
        self.ano = int(ano or 2020)
        self.placa = (placa or "").strip().upper()
        self.km_atual = max(0, int(float(km_atual or 0)))
        self.combustivel = (combustivel or "Flex").strip()
        self.cor = (cor or "").strip().title()
        self.apelido = (apelido or "").strip()
        self.observacoes = (observacoes or "").strip()

    @property
    def nome_completo(self) -> str:
        base = f"{self.marca} {self.modelo}".strip()
        if self.apelido:
            return f"{base} ({self.apelido})"
        return base

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "marca": self.marca,
            "modelo": self.modelo,
            "ano": self.ano,
            "placa": self.placa,
            "km_atual": self.km_atual,
            "combustivel": self.combustivel,
            "cor": self.cor,
            "apelido": self.apelido,
            "observacoes": self.observacoes,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Carro":
        return cls(
            id=data.get("id"),
            user_id=data.get("user_id"),
            marca=data.get("marca", ""),
            modelo=data.get("modelo", ""),
            ano=data.get("ano", 2020),
            placa=data.get("placa", ""),
            km_atual=data.get("km_atual", 0),
            combustivel=data.get("combustivel", "Flex"),
            cor=data.get("cor", ""),
            apelido=data.get("apelido", ""),
            observacoes=data.get("observacoes", ""),
        )

    def __repr__(self) -> str:
        return f"Carro(id={self.id}, modelo='{self.marca} {self.modelo}', placa='{self.placa}')"
