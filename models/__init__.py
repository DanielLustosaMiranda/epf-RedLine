import sys
sys.dont_write_bytecode = True

from models.user import User
from models.carro import Carro
from models.manutencao import Manutencao
from models.manutencaoProgramada import ManutencaoProgramada
from models.itemVidaUtil import ItemVidaUtil
from models.abastecimento import Abastecimento

__all__ = [
    'User',
    'Carro',
    'Manutencao',
    'ManutencaoProgramada',
    'ItemVidaUtil',
    'Abastecimento',
]
