from models.carro import Carro
from services import data_manager

CARS_FILE = 'carros.json'


def get_cars_by_user_id(user_id) -> list[dict]:
    if user_id is None:
        return []
    target_user_id = int(user_id)
    raw = data_manager.read_data(CARS_FILE)
    cars = [Carro.from_dict(c).to_dict() for c in raw if int(c.get('user_id', 0)) == target_user_id]
    return cars


def get_car_by_id(car_id, user_id=None) -> dict | None:
    if car_id is None:
        return None
    target_id = int(car_id)
    raw = data_manager.read_data(CARS_FILE)
    for c in raw:
        if int(c.get('id', 0)) == target_id:
            if user_id is not None and int(c.get('user_id', 0)) != int(user_id):
                return None
            return Carro.from_dict(c).to_dict()
    return None


def create_car(
    marca: str,
    modelo: str,
    ano: int,
    placa: str,
    km_atual: int,
    user_id: int,
    combustivel: str = "Flex",
    cor: str = "",
    apelido: str = "",
    observacoes: str = "",
) -> dict:
    all_cars = data_manager.read_data(CARS_FILE)
    new_id = data_manager.next_id(all_cars)

    car_obj = Carro(
        id=new_id,
        user_id=user_id,
        marca=marca,
        modelo=modelo,
        ano=ano,
        placa=placa,
        km_atual=km_atual,
        combustivel=combustivel,
        cor=cor,
        apelido=apelido,
        observacoes=observacoes,
    )
    car_dict = car_obj.to_dict()
    all_cars.append(car_dict)
    data_manager.write_data(CARS_FILE, all_cars)
    return car_dict


def update_car(
    car_id: int,
    marca: str,
    modelo: str,
    ano: int,
    placa: str,
    km_atual: int,
    combustivel: str = "Flex",
    cor: str = "",
    apelido: str = "",
    observacoes: str = "",
    user_id: int = None,
) -> dict | None:
    all_cars = data_manager.read_data(CARS_FILE)
    target_id = int(car_id)

    for i, c in enumerate(all_cars):
        if int(c.get('id', 0)) == target_id:
            if user_id is not None and int(c.get('user_id', 0)) != int(user_id):
                return None
            updated = Carro(
                id=target_id,
                user_id=c.get('user_id'),
                marca=marca,
                modelo=modelo,
                ano=ano,
                placa=placa,
                km_atual=km_atual,
                combustivel=combustivel,
                cor=cor,
                apelido=apelido,
                observacoes=observacoes,
            ).to_dict()
            all_cars[i] = updated
            data_manager.write_data(CARS_FILE, all_cars)
            return updated
    return None


def update_car_km(car_id: int, novo_km: int, user_id: int = None, force: bool = True) -> dict | None:
    """Atualiza a quilometragem atual do carro. Se force=False, só atualiza se novo_km > km_atual."""
    all_cars = data_manager.read_data(CARS_FILE)
    target_id = int(car_id)
    novo_km_val = max(0, int(float(novo_km or 0)))

    for i, c in enumerate(all_cars):
        if int(c.get('id', 0)) == target_id:
            if user_id is not None and int(c.get('user_id', 0)) != int(user_id):
                return None
            km_atual = int(c.get('km_atual', 0))
            if force or novo_km_val > km_atual:
                c['km_atual'] = novo_km_val
                all_cars[i] = Carro.from_dict(c).to_dict()
                data_manager.write_data(CARS_FILE, all_cars)
            return all_cars[i]
    return None


def delete_car(car_id: int, user_id: int = None) -> bool:
    all_cars = data_manager.read_data(CARS_FILE)
    target_id = int(car_id)
    car = get_car_by_id(target_id, user_id=user_id)
    if not car:
        return False

    cars_to_keep = [c for c in all_cars if int(c.get('id', 0)) != target_id]
    data_manager.write_data(CARS_FILE, cars_to_keep)

    # Limpa registros dependentes (manutenções, agendamentos, itens de vida útil e abastecimentos)
    for filename, key in [
        ('manutencoes.json', 'car_id'),
        ('manutencoes_programadas.json', 'id_veiculo'),
        ('itens_vida_util.json', 'id_veiculo'),
        ('abastecimentos.json', 'car_id'),
    ]:
        items = data_manager.read_data(filename)
        filtered = [item for item in items if int(item.get(key, 0) or 0) != target_id]
        if len(filtered) != len(items):
            data_manager.write_data(filename, filtered)

    return True
