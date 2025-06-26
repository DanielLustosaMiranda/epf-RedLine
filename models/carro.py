class Carro:
    def __init__(self, usuario, marca, modelo, ano, placa, km_atual) -> None:
        self._usuario = usuario
        self._marca = marca
        self._modelo = modelo
        self._ano = ano
        self._placa = placa
        self._km_atual = km_atual
     
    def __str__(self):
        """Retorna todas as infos em texto formatado para print direto."""
        return (f"Usuario: {self._usuario}, "
                f"Marca: {self._marca}, "
                f"Modelo: {self._modelo}, "
                f"Ano: {self._ano}, "
                f"Placa: {self._placa}, "
                f"KM atual: {self._km_atual}")

    def get_info_completa(self): 
        """Retorna todas as infos (usando __str__)"""
        return str(self)

