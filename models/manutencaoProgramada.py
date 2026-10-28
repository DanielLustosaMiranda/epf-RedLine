from datetime import datetime, date, timedelta


class ManutencaoProgramada:
    """Representa uma manutenção programada (revisão futura por tempo e/ou quilometragem)."""

    def __init__(
        self,
        descricao,
        frequencia_dias,
        ultima_data,
        id_veiculo,
        id=None,
        frequencia_km=10000,
        ultimo_km=0,
        custo_estimado=0.0,
        observacoes="",
    ):
        self.id = int(id) if id is not None else None
        self._id_veiculo = int(id_veiculo) if id_veiculo is not None else None
        self._descricao = (descricao or "").strip()
        self._frequencia_dias = max(1, int(float(frequencia_dias or 180)))
        self._ultima_data = (ultima_data or date.today().isoformat()).strip()
        self._frequencia_km = max(0, int(float(frequencia_km or 0)))
        self._ultimo_km = max(0, int(float(ultimo_km or 0)))
        self._custo_estimado = round(max(0.0, float(custo_estimado or 0.0)), 2)
        self._observacoes = (observacoes or "").strip()

    @property
    def id_veiculo(self):
        return self._id_veiculo

    @property
    def descricao(self):
        return self._descricao

    @property
    def frequencia_dias(self):
        return self._frequencia_dias

    @property
    def ultima_data(self):
        return self._ultima_data

    @property
    def frequencia_km(self):
        return self._frequencia_km

    @property
    def ultimo_km(self):
        return self._ultimo_km

    @property
    def custo_estimado(self):
        return self._custo_estimado

    @property
    def observacoes(self):
        return self._observacoes

    def calcular_status(self, km_atual_veiculo: int = 0, hoje: date = None) -> dict:
        """Calcula datas, KM de vencimento e nível de urgência da manutenção programada."""
        hoje = hoje or date.today()
        try:
            dt_ultima = datetime.strptime(self._ultima_data[:10], "%Y-%m-%d").date()
        except ValueError:
            dt_ultima = hoje

        proxima_data = dt_ultima + timedelta(days=self._frequencia_dias)
        dias_restantes = (proxima_data - hoje).days

        proximo_km = (self._ultimo_km + self._frequencia_km) if self._frequencia_km > 0 else None
        km_restantes = (proximo_km - int(km_atual_veiculo or 0)) if proximo_km is not None else None

        # Determina status ('atrasada', 'proxima', 'em_dia')
        status = "em_dia"
        motivo_alerta = []

        if dias_restantes < 0:
            status = "atrasada"
            motivo_alerta.append(f"Vencida há {abs(dias_restantes)} dias")
        elif dias_restantes <= 20:
            status = "proxima"
            motivo_alerta.append(f"Vence em {dias_restantes} dias")

        if km_restantes is not None:
            if km_restantes <= 0:
                status = "atrasada"
                motivo_alerta.append(f"Excedeu {abs(km_restantes):,} km".replace(",", "."))
            elif km_restantes <= 1000 and status != "atrasada":
                status = "proxima"
                motivo_alerta.append(f"Faltam {km_restantes:,} km".replace(",", "."))

        resumo_status = " • ".join(motivo_alerta) if motivo_alerta else "Dentro do prazo"

        return {
            **self.to_dict(),
            "proxima_data": proxima_data.isoformat(),
            "dias_restantes": dias_restantes,
            "proximo_km": proximo_km,
            "km_restantes": km_restantes,
            "status": status,
            "resumo_status": resumo_status,
        }

    def detalhar_servico(self) -> str:
        return str(self)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "id_veiculo": self._id_veiculo,
            "descricao": self._descricao,
            "frequencia_dias": self._frequencia_dias,
            "ultima_data": self._ultima_data,
            "frequencia_km": self._frequencia_km,
            "ultimo_km": self._ultimo_km,
            "custo_estimado": self._custo_estimado,
            "observacoes": self._observacoes,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ManutencaoProgramada":
        return cls(
            id=data.get("id"),
            id_veiculo=data.get("id_veiculo") or data.get("car_id"),
            descricao=data.get("descricao", ""),
            frequencia_dias=data.get("frequencia_dias", 180),
            ultima_data=data.get("ultima_data", ""),
            frequencia_km=data.get("frequencia_km", 10000),
            ultimo_km=data.get("ultimo_km", 0),
            custo_estimado=data.get("custo_estimado", 0.0),
            observacoes=data.get("observacoes", ""),
        )

    def __str__(self) -> str:
        return (
            f"{self._descricao} - a cada {self._frequencia_dias} dias "
            f"(última: {self._ultima_data})"
        )
