from datetime import datetime, date, timedelta


class ItemVidaUtil:
    """Representa um componente/peça monitorada do veículo e seu desgaste estimado."""

    def __init__(
        self,
        nome_item,
        data_instalacao,
        validade_anos,
        id_veiculo,
        id=None,
        km_instalacao=0,
        validade_km=10000,
        marca_peca="",
        observacoes="",
    ):
        self.id = int(id) if id is not None else None
        self._id_veiculo = int(id_veiculo) if id_veiculo is not None else None
        self._nome_item = (nome_item or "").strip()
        self._data_instalacao = (data_instalacao or date.today().isoformat()).strip()
        self._validade_anos = max(0.1, float(validade_anos or 1.0))
        self._km_instalacao = max(0, int(float(km_instalacao or 0)))
        self._validade_km = max(0, int(float(validade_km or 0)))
        self._marca_peca = (marca_peca or "").strip()
        self._observacoes = (observacoes or "").strip()

    @property
    def id_veiculo(self):
        return self._id_veiculo

    @property
    def nome_item(self):
        return self._nome_item

    @property
    def data_instalacao(self):
        return self._data_instalacao

    @property
    def validade_anos(self):
        return self._validade_anos

    @property
    def km_instalacao(self):
        return self._km_instalacao

    @property
    def validade_km(self):
        return self._validade_km

    @property
    def marca_peca(self):
        return self._marca_peca

    @property
    def observacoes(self):
        return self._observacoes

    def calcular_vida_util(self, km_atual_veiculo: int = 0, hoje: date = None) -> dict:
        """Calcula o percentual de vida útil restante por tempo e por KM."""
        hoje = hoje or date.today()
        try:
            dt_inst = datetime.strptime(self._data_instalacao[:10], "%Y-%m-%d").date()
        except ValueError:
            dt_inst = hoje

        validade_dias = max(1, int(round(self._validade_anos * 365)))
        data_vencimento = dt_inst + timedelta(days=validade_dias)
        dias_uso = max(0, (hoje - dt_inst).days)
        dias_restantes = (data_vencimento - hoje).days
        saude_tempo = max(0, min(100, int(round((1 - (dias_uso / validade_dias)) * 100))))

        saude_km = 100
        km_vencimento = None
        km_restantes = None
        if self._validade_km > 0:
            km_vencimento = self._km_instalacao + self._validade_km
            km_rodados = max(0, int(km_atual_veiculo or 0) - self._km_instalacao)
            km_restantes = km_vencimento - int(km_atual_veiculo or 0)
            saude_km = max(0, min(100, int(round((1 - (km_rodados / self._validade_km)) * 100))))

        # A saúde efetiva do componente é o menor valor entre desgaste por tempo e por KM
        saude_final = min(saude_tempo, saude_km)

        if saude_final <= 20:
            status = "critico"
            status_label = "Substituição Urgente"
        elif saude_final <= 45:
            status = "atencao"
            status_label = "Atenção / Planejar Troca"
        else:
            status = "bom"
            status_label = "Em Bom Estado"

        return {
            **self.to_dict(),
            "data_vencimento": data_vencimento.isoformat(),
            "dias_restantes": dias_restantes,
            "km_vencimento": km_vencimento,
            "km_restantes": km_restantes,
            "saude_tempo": saude_tempo,
            "saude_km": saude_km,
            "saude_percentual": saude_final,
            "status": status,
            "status_label": status_label,
        }

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "id_veiculo": self._id_veiculo,
            "nome_item": self._nome_item,
            "data_instalacao": self._data_instalacao,
            "validade_anos": self._validade_anos,
            "km_instalacao": self._km_instalacao,
            "validade_km": self._validade_km,
            "marca_peca": self._marca_peca,
            "observacoes": self._observacoes,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ItemVidaUtil":
        return cls(
            id=data.get("id"),
            id_veiculo=data.get("id_veiculo") or data.get("car_id"),
            nome_item=data.get("nome_item", ""),
            data_instalacao=data.get("data_instalacao", ""),
            validade_anos=data.get("validade_anos", 1.0),
            km_instalacao=data.get("km_instalacao", 0),
            validade_km=data.get("validade_km", 10000),
            marca_peca=data.get("marca_peca", ""),
            observacoes=data.get("observacoes", ""),
        )

    def __str__(self) -> str:
        return (
            f"{self._nome_item} instalado em {self._data_instalacao} "
            f"(validade: {self._validade_anos} anos)"
        )
