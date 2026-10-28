from models.manutencao import Manutencao
from services import data_manager, car_service

MAINTENANCES_FILE = 'manutencoes.json'


def get_manutencoes_by_car_id(car_id: int) -> list[dict]:
    if car_id is None:
        return []
    target_car_id = int(car_id)
    raw = data_manager.read_data(MAINTENANCES_FILE)
    items = [
        Manutencao.from_dict(m).to_dict()
        for m in raw
        if m.get('car_id') is not None and int(m.get('car_id')) == target_car_id
    ]
    # Ordena da mais recente para a mais antiga (por data e KM)
    items.sort(key=lambda x: (x.get('data', ''), x.get('km', 0)), reverse=True)
    return items


def get_manutencoes_by_user(user_id: int, car_id: int = None, tipo: str = None, busca: str = None) -> list[dict]:
    user_cars = car_service.get_cars_by_user_id(user_id)
    cars_map = {c['id']: c for c in user_cars}
    if not cars_map:
        return []

    raw = data_manager.read_data(MAINTENANCES_FILE)
    result = []
    busca_clean = (busca or "").strip().lower()
    tipo_clean = (tipo or "").strip().lower()

    for m in raw:
        c_id = m.get('car_id')
        if c_id is None or int(c_id) not in cars_map:
            continue
        if car_id and int(c_id) != int(car_id):
            continue

        item = Manutencao.from_dict(m).to_dict()
        if tipo_clean and item['tipo'].lower() != tipo_clean:
            continue
        if busca_clean:
            haystack = f"{item['descricao']} {item['oficina']} {item['observacoes']} {item['tipo']}".lower()
            if busca_clean not in haystack:
                continue

        car = cars_map[int(c_id)]
        item['car_nome'] = f"{car['marca']} {car['modelo']}"
        item['car_placa'] = car['placa']
        result.append(item)

    result.sort(key=lambda x: (x.get('data', ''), x.get('km', 0)), reverse=True)
    return result


def get_manutencao_by_id(maintenance_id: int) -> dict | None:
    if maintenance_id is None:
        return None
    target_id = int(maintenance_id)
    raw = data_manager.read_data(MAINTENANCES_FILE)
    for m in raw:
        if int(m.get('id', 0)) == target_id:
            return Manutencao.from_dict(m).to_dict()
    return None


def create_manutencao(
    descricao: str,
    data: str,
    custo: float,
    tipo: str,
    km: int,
    car_id: int,
    oficina: str = "",
    garantia_meses: int = 0,
    observacoes: str = "",
    atualizar_km_carro: bool = True,
) -> dict:
    all_maintenances = data_manager.read_data(MAINTENANCES_FILE)
    new_id = data_manager.next_id(all_maintenances)

    maint_obj = Manutencao(
        id=new_id,
        car_id=car_id,
        descricao=descricao,
        data=data,
        custo=custo,
        tipo=tipo,
        km=km,
        oficina=oficina,
        garantia_meses=garantia_meses,
        observacoes=observacoes,
    )
    maint_dict = maint_obj.to_dict()
    all_maintenances.append(maint_dict)
    data_manager.write_data(MAINTENANCES_FILE, all_maintenances)

    if atualizar_km_carro:
        car_service.update_car_km(car_id, maint_dict['km'], force=False)

    return maint_dict


def update_manutencao(
    maintenance_id: int,
    descricao: str,
    data: str,
    custo: float,
    tipo: str,
    km: int,
    oficina: str = "",
    garantia_meses: int = 0,
    observacoes: str = "",
) -> dict | None:
    all_maintenances = data_manager.read_data(MAINTENANCES_FILE)
    target_id = int(maintenance_id)

    for i, m in enumerate(all_maintenances):
        if int(m.get('id', 0)) == target_id:
            updated = Manutencao(
                id=target_id,
                car_id=m.get('car_id'),
                descricao=descricao,
                data=data,
                custo=custo,
                tipo=tipo,
                km=km,
                oficina=oficina,
                garantia_meses=garantia_meses,
                observacoes=observacoes,
            ).to_dict()
            all_maintenances[i] = updated
            data_manager.write_data(MAINTENANCES_FILE, all_maintenances)
            car_service.update_car_km(updated['car_id'], updated['km'], force=False)
            return updated
    return None


def delete_manutencao(maintenance_id: int) -> bool:
    all_maintenances = data_manager.read_data(MAINTENANCES_FILE)
    target_id = int(maintenance_id)
    to_keep = [m for m in all_maintenances if int(m.get('id', 0)) != target_id]
    if len(to_keep) < len(all_maintenances):
        data_manager.write_data(MAINTENANCES_FILE, to_keep)
        return True
    return False
