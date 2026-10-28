from datetime import date
from config import KIT_PADRAO_VIDA_UTIL
from models.itemVidaUtil import ItemVidaUtil
from services import data_manager, car_service, manutencao_service

VIDA_UTIL_FILE = 'itens_vida_util.json'


def get_itens_by_car_id(car_id: int, km_atual_veiculo: int = None) -> list[dict]:
    if car_id is None:
        return []
    target_car_id = int(car_id)
    if km_atual_veiculo is None:
        car = car_service.get_car_by_id(target_car_id)
        km_atual_veiculo = car['km_atual'] if car else 0

    raw = data_manager.read_data(VIDA_UTIL_FILE)
    items = []
    for item in raw:
        v_id = item.get('id_veiculo') or item.get('car_id')
        if v_id is not None and int(v_id) == target_car_id:
            iv = ItemVidaUtil.from_dict(item)
            items.append(iv.calcular_vida_util(km_atual_veiculo=km_atual_veiculo))

    # Ordena do mais desgastado (menor saúde_percentual) para o mais novo
    items.sort(key=lambda x: x['saude_percentual'])
    return items


def get_item_by_id(item_id: int) -> dict | None:
    if item_id is None:
        return None
    target_id = int(item_id)
    raw = data_manager.read_data(VIDA_UTIL_FILE)
    for item in raw:
        if int(item.get('id', 0)) == target_id:
            return ItemVidaUtil.from_dict(item).to_dict()
    return None


def create_item(
    id_veiculo: int,
    nome_item: str,
    data_instalacao: str,
    validade_anos: float,
    km_instalacao: int = 0,
    validade_km: int = 10000,
    marca_peca: str = "",
    observacoes: str = "",
) -> dict:
    all_items = data_manager.read_data(VIDA_UTIL_FILE)
    new_id = data_manager.next_id(all_items)

    iv = ItemVidaUtil(
        id=new_id,
        id_veiculo=id_veiculo,
        nome_item=nome_item,
        data_instalacao=data_instalacao,
        validade_anos=validade_anos,
        km_instalacao=km_instalacao,
        validade_km=validade_km,
        marca_peca=marca_peca,
        observacoes=observacoes,
    )
    iv_dict = iv.to_dict()
    all_items.append(iv_dict)
    data_manager.write_data(VIDA_UTIL_FILE, all_items)
    return iv_dict


def update_item(
    item_id: int,
    nome_item: str,
    data_instalacao: str,
    validade_anos: float,
    km_instalacao: int = 0,
    validade_km: int = 10000,
    marca_peca: str = "",
    observacoes: str = "",
) -> dict | None:
    all_items = data_manager.read_data(VIDA_UTIL_FILE)
    target_id = int(item_id)

    for i, item in enumerate(all_items):
        if int(item.get('id', 0)) == target_id:
            updated = ItemVidaUtil(
                id=target_id,
                id_veiculo=item.get('id_veiculo') or item.get('car_id'),
                nome_item=nome_item,
                data_instalacao=data_instalacao,
                validade_anos=validade_anos,
                km_instalacao=km_instalacao,
                validade_km=validade_km,
                marca_peca=marca_peca,
                observacoes=observacoes,
            ).to_dict()
            all_items[i] = updated
            data_manager.write_data(VIDA_UTIL_FILE, all_items)
            return updated
    return None


def renovar_item(item_id: int, custo: float = 0.0, registrar_historico: bool = True) -> dict | None:
    """Renova um componente (data_instalacao = hoje, km_instalacao = km_atual do carro)."""
    item = get_item_by_id(item_id)
    if not item:
        return None
    car = car_service.get_car_by_id(item['id_veiculo'])
    if not car:
        return None

    hoje_str = date.today().isoformat()
    km_atual = int(car['km_atual'])

    if registrar_historico:
        manutencao_service.create_manutencao(
            descricao=f"Substituição: {item['nome_item']}",
            data=hoje_str,
            custo=float(custo or 0.0),
            tipo="Preventiva",
            km=km_atual,
            car_id=car['id'],
            observacoes="Substituição registrada pela gestão de Vida Útil de Peças.",
            atualizar_km_carro=False,
        )

    return update_item(
        item_id=item_id,
        nome_item=item['nome_item'],
        data_instalacao=hoje_str,
        validade_anos=item['validade_anos'],
        km_instalacao=km_atual,
        validade_km=item['validade_km'],
        marca_peca=item.get('marca_peca', ''),
        observacoes=item.get('observacoes', ''),
    )


def gerar_kit_padrao_para_veiculo(car_id: int) -> int:
    """Cria os itens essenciais de monitoramento para o veículo caso ainda não existam."""
    car = car_service.get_car_by_id(car_id)
    if not car:
        return 0

    existentes = {i['nome_item'].lower() for i in get_itens_by_car_id(car_id, car['km_atual'])}
    hoje_str = date.today().isoformat()
    criados = 0

    for padrao in KIT_PADRAO_VIDA_UTIL:
        if padrao['nome_item'].lower() not in existentes:
            create_item(
                id_veiculo=car['id'],
                nome_item=padrao['nome_item'],
                data_instalacao=hoje_str,
                validade_anos=padrao['validade_anos'],
                km_instalacao=car['km_atual'],
                validade_km=padrao['validade_km'],
                observacoes="Adicionado pelo Kit Essencial RedLine",
            )
            criados += 1
    return criados


def delete_item(item_id: int) -> bool:
    all_items = data_manager.read_data(VIDA_UTIL_FILE)
    target_id = int(item_id)
    to_keep = [i for i in all_items if int(i.get('id', 0)) != target_id]
    if len(to_keep) < len(all_items):
        data_manager.write_data(VIDA_UTIL_FILE, to_keep)
        return True
    return False
