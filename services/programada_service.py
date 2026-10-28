from datetime import date
from models.manutencaoProgramada import ManutencaoProgramada
from services import data_manager, car_service, manutencao_service

PROGRAMADAS_FILE = 'manutencoes_programadas.json'


def get_programadas_by_car_id(car_id: int, km_atual_veiculo: int = None) -> list[dict]:
    if car_id is None:
        return []
    target_car_id = int(car_id)
    if km_atual_veiculo is None:
        car = car_service.get_car_by_id(target_car_id)
        km_atual_veiculo = car['km_atual'] if car else 0

    raw = data_manager.read_data(PROGRAMADAS_FILE)
    items = []
    for item in raw:
        v_id = item.get('id_veiculo') or item.get('car_id')
        if v_id is not None and int(v_id) == target_car_id:
            mp = ManutencaoProgramada.from_dict(item)
            items.append(mp.calcular_status(km_atual_veiculo=km_atual_veiculo))

    # Ordena por urgência (atrasadas primeiro, depois próximas, depois menor dias_restantes)
    ordem_status = {'atrasada': 0, 'proxima': 1, 'em_dia': 2}
    items.sort(key=lambda x: (ordem_status.get(x['status'], 3), x['dias_restantes']))
    return items


def get_programada_by_id(prog_id: int) -> dict | None:
    if prog_id is None:
        return None
    target_id = int(prog_id)
    raw = data_manager.read_data(PROGRAMADAS_FILE)
    for item in raw:
        if int(item.get('id', 0)) == target_id:
            return ManutencaoProgramada.from_dict(item).to_dict()
    return None


def create_programada(
    id_veiculo: int,
    descricao: str,
    frequencia_dias: int,
    ultima_data: str,
    frequencia_km: int = 10000,
    ultimo_km: int = 0,
    custo_estimado: float = 0.0,
    observacoes: str = "",
) -> dict:
    all_items = data_manager.read_data(PROGRAMADAS_FILE)
    new_id = data_manager.next_id(all_items)

    mp = ManutencaoProgramada(
        id=new_id,
        id_veiculo=id_veiculo,
        descricao=descricao,
        frequencia_dias=frequencia_dias,
        ultima_data=ultima_data,
        frequencia_km=frequencia_km,
        ultimo_km=ultimo_km,
        custo_estimado=custo_estimado,
        observacoes=observacoes,
    )
    mp_dict = mp.to_dict()
    all_items.append(mp_dict)
    data_manager.write_data(PROGRAMADAS_FILE, all_items)
    return mp_dict


def update_programada(
    prog_id: int,
    descricao: str,
    frequencia_dias: int,
    ultima_data: str,
    frequencia_km: int = 10000,
    ultimo_km: int = 0,
    custo_estimado: float = 0.0,
    observacoes: str = "",
) -> dict | None:
    all_items = data_manager.read_data(PROGRAMADAS_FILE)
    target_id = int(prog_id)

    for i, item in enumerate(all_items):
        if int(item.get('id', 0)) == target_id:
            updated = ManutencaoProgramada(
                id=target_id,
                id_veiculo=item.get('id_veiculo') or item.get('car_id'),
                descricao=descricao,
                frequencia_dias=frequencia_dias,
                ultima_data=ultima_data,
                frequencia_km=frequencia_km,
                ultimo_km=ultimo_km,
                custo_estimado=custo_estimado,
                observacoes=observacoes,
            ).to_dict()
            all_items[i] = updated
            data_manager.write_data(PROGRAMADAS_FILE, all_items)
            return updated
    return None


def concluir_programada(prog_id: int, custo_real: float = None, km_realizado: int = None, oficina: str = "") -> dict | None:
    """
    Marca uma manutenção programada como realizada hoje:
    1. Registra automaticamente no histórico de manutenções realizadas.
    2. Reinicia o ciclo da manutenção programada (ultima_data = hoje, ultimo_km = km_realizado).
    """
    prog = get_programada_by_id(prog_id)
    if not prog:
        return None

    car = car_service.get_car_by_id(prog['id_veiculo'])
    if not car:
        return None

    hoje_str = date.today().isoformat()
    km_efetivo = int(km_realizado) if km_realizado is not None else int(car['km_atual'])
    custo_efetivo = float(custo_real) if custo_real is not None else float(prog.get('custo_estimado', 0.0))

    # Registra no histórico de manutenções
    manutencao_service.create_manutencao(
        descricao=prog['descricao'],
        data=hoje_str,
        custo=custo_efetivo,
        tipo="Preventiva",
        km=km_efetivo,
        car_id=car['id'],
        oficina=oficina,
        observacoes="Manutenção concluída a partir do agendamento programado.",
        atualizar_km_carro=True,
    )

    # Atualiza o agendamento para o próximo ciclo
    return update_programada(
        prog_id=prog_id,
        descricao=prog['descricao'],
        frequencia_dias=prog['frequencia_dias'],
        ultima_data=hoje_str,
        frequencia_km=prog['frequencia_km'],
        ultimo_km=km_efetivo,
        custo_estimado=custo_efetivo,
        observacoes=prog.get('observacoes', ''),
    )


def delete_programada(prog_id: int) -> bool:
    all_items = data_manager.read_data(PROGRAMADAS_FILE)
    target_id = int(prog_id)
    to_keep = [i for i in all_items if int(i.get('id', 0)) != target_id]
    if len(to_keep) < len(all_items):
        data_manager.write_data(PROGRAMADAS_FILE, to_keep)
        return True
    return False
