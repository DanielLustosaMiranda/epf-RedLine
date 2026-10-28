from models.abastecimento import Abastecimento
from services import data_manager, car_service

ABASTECIMENTOS_FILE = 'abastecimentos.json'


def get_abastecimentos_by_car_id(car_id: int) -> list[dict]:
    if car_id is None:
        return []
    target_car_id = int(car_id)
    raw = data_manager.read_data(ABASTECIMENTOS_FILE)
    items = [
        Abastecimento.from_dict(a).to_dict()
        for a in raw
        if a.get('car_id') is not None and int(a.get('car_id')) == target_car_id
    ]
    # Ordena por KM crescente para calcular consumo entre abastecimentos consecutivos
    items.sort(key=lambda x: (x.get('km', 0), x.get('data', '')))
    for i, item in enumerate(items):
        if i > 0 and item['km'] > items[i - 1]['km'] and item['litros'] > 0:
            km_percorrido = item['km'] - items[i - 1]['km']
            item['consumo_kml'] = round(km_percorrido / item['litros'], 2)
        else:
            item['consumo_kml'] = None

    # Retorna do mais recente para o mais antigo para exibição
    items.reverse()
    return items


def get_abastecimento_by_id(abast_id: int) -> dict | None:
    if abast_id is None:
        return None
    target_id = int(abast_id)
    raw = data_manager.read_data(ABASTECIMENTOS_FILE)
    for a in raw:
        if int(a.get('id', 0)) == target_id:
            return Abastecimento.from_dict(a).to_dict()
    return None


def create_abastecimento(
    car_id: int,
    data: str,
    km: int,
    combustivel: str,
    litros: float,
    valor_total: float,
    posto: str = "",
    tanque_cheio: bool = True,
) -> dict:
    all_items = data_manager.read_data(ABASTECIMENTOS_FILE)
    new_id = data_manager.next_id(all_items)

    abast = Abastecimento(
        id=new_id,
        car_id=car_id,
        data=data,
        km=km,
        combustivel=combustivel,
        litros=litros,
        valor_total=valor_total,
        posto=posto,
        tanque_cheio=tanque_cheio,
    )
    abast_dict = abast.to_dict()
    all_items.append(abast_dict)
    data_manager.write_data(ABASTECIMENTOS_FILE, all_items)

    car_service.update_car_km(car_id, abast_dict['km'], force=False)
    return abast_dict


def delete_abastecimento(abast_id: int) -> bool:
    all_items = data_manager.read_data(ABASTECIMENTOS_FILE)
    target_id = int(abast_id)
    to_keep = [a for a in all_items if int(a.get('id', 0)) != target_id]
    if len(to_keep) < len(all_items):
        data_manager.write_data(ABASTECIMENTOS_FILE, to_keep)
        return True
    return False


def calcular_estatisticas_combustivel(car_id: int) -> dict:
    abastecimentos = get_abastecimentos_by_car_id(car_id)
    if not abastecimentos:
        return {
            'total_gasto': 0.0,
            'total_litros': 0.0,
            'preco_medio_litro': 0.0,
            'consumo_medio_kml': 0.0,
            'quantidade': 0,
        }

    total_gasto = round(sum(a['valor_total'] for a in abastecimentos), 2)
    total_litros = round(sum(a['litros'] for a in abastecimentos), 2)
    preco_medio = round(total_gasto / total_litros, 2) if total_litros > 0 else 0.0

    consumos_validos = [a['consumo_kml'] for a in abastecimentos if a.get('consumo_kml')]
    consumo_medio = round(sum(consumos_validos) / len(consumos_validos), 2) if consumos_validos else 0.0

    return {
        'total_gasto': total_gasto,
        'total_litros': total_litros,
        'preco_medio_litro': preco_medio,
        'consumo_medio_kml': consumo_medio,
        'quantidade': len(abastecimentos),
    }
