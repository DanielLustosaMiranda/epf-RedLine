import os
import sys

# Impede a criação automática de pastas __pycache__ e arquivos .pyc
sys.dont_write_bytecode = True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
VIEWS_DIR = os.path.join(BASE_DIR, 'views')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
SESSIONS_DIR = os.path.join(DATA_DIR, 'sessions')

HOST = os.environ.get('REDLINE_HOST', '0.0.0.0')
PORT = int(os.environ.get('REDLINE_PORT', 8080))
DEBUG = os.environ.get('REDLINE_DEBUG', 'true').lower() == 'true'

SESSION_OPTS = {
    'session.type': 'file',
    'session.cookie_expires': 86400,  # 24 horas
    'session.data_dir': SESSIONS_DIR,
    'session.auto': True,
}

# Categorias de manutenção suportadas
TIPOS_MANUTENCAO = [
    'Preventiva',
    'Corretiva',
    'Preditiva',
    'Revisão Periódica',
    'Estética / Upgrade',
    'Emergencial',
]

# Tipos de combustível suportados
TIPOS_COMBUSTIVEL = [
    'Flex',
    'Gasolina',
    'Etanol',
    'Diesel',
    'Híbrido',
    'Elétrico',
    'GNV',
]

# Presets rápidos de Manutenção Programada (descrição, frequência em dias, frequência em km, custo estimado)
PRESETS_MANUTENCAO_PROGRAMADA = [
    {
        'descricao': 'Troca de Óleo do Motor e Filtro',
        'frequencia_dias': 180,
        'frequencia_km': 10000,
        'custo_estimado': 280.0,
    },
    {
        'descricao': 'Alinhamento e Balanceamento',
        'frequencia_dias': 180,
        'frequencia_km': 10000,
        'custo_estimado': 150.0,
    },
    {
        'descricao': 'Revisão do Sistema de Freios',
        'frequencia_dias': 365,
        'frequencia_km': 20000,
        'custo_estimado': 350.0,
    },
    {
        'descricao': 'Troca do Filtro de Ar e Cabine (Ar-Condicionado)',
        'frequencia_dias': 365,
        'frequencia_km': 15000,
        'custo_estimado': 120.0,
    },
    {
        'descricao': 'Substituição do Fluido de Arrefecimento',
        'frequencia_dias': 730,
        'frequencia_km': 40000,
        'custo_estimado': 220.0,
    },
    {
        'descricao': 'Troca da Correia Dentada e Tensor',
        'frequencia_dias': 1460,
        'frequencia_km': 60000,
        'custo_estimado': 850.0,
    },
]

# Kit padrão de peças para monitoramento de vida útil (nome, validade_anos, validade_km)
KIT_PADRAO_VIDA_UTIL = [
    {'nome_item': 'Óleo do Motor e Filtro', 'validade_anos': 0.5, 'validade_km': 10000},
    {'nome_item': 'Pastilhas de Freio Dianteiras', 'validade_anos': 2.0, 'validade_km': 30000},
    {'nome_item': 'Bateria 12V', 'validade_anos': 3.0, 'validade_km': 60000},
    {'nome_item': 'Jogo de Pneus', 'validade_anos': 5.0, 'validade_km': 50000},
    {'nome_item': 'Correia Dentada / Acessórios', 'validade_anos': 4.0, 'validade_km': 60000},
    {'nome_item': 'Filtro de Ar e Filtro de Cabine', 'validade_anos': 1.0, 'validade_km': 15000},
    {'nome_item': 'Velas de Ignição', 'validade_anos': 3.0, 'validade_km': 40000},
    {'nome_item': 'Palhetas do Limpador de Para-brisa', 'validade_anos': 1.0, 'validade_km': 20000},
]
