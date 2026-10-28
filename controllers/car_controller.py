from bottle import route, request, redirect
from config import TIPOS_COMBUSTIVEL
from services import (
    car_service,
    dashboard_service,
    abastecimento_service,
    vida_util_service,
)
from utils.auth_decorator import login_required, get_session, set_flash
from utils.view_helper import render_page


@route('/carros')
@login_required
def list_user_cars():
    session = get_session()
    user_id = session.get('user_id')
    raw_cars = car_service.get_cars_by_user_id(user_id)
    cars = [dashboard_service.enriquecer_carro(c) for c in raw_cars]
    return render_page('car_list', cars=cars)


@route('/carros/<car_id:int>')
@login_required
def show_car_detail(car_id):
    session = get_session()
    user_id = session.get('user_id')
    raw_car = car_service.get_car_by_id(car_id, user_id=user_id)
    if not raw_car:
        set_flash("Veículo não encontrado na sua garagem.", "danger")
        return redirect('/carros')

    car = dashboard_service.enriquecer_carro(raw_car)
    abastecimentos = abastecimento_service.get_abastecimentos_by_car_id(car_id)
    combustivel_stats = abastecimento_service.calcular_estatisticas_combustivel(car_id)
    aba_ativa = request.query.get('tab', 'visao-geral')

    return render_page(
        'car_detail',
        car=car,
        manutencoes=car['manutencoes'],
        programadas=car['programadas'],
        itens_vida=car['itens_vida'],
        abastecimentos=abastecimentos,
        combustivel_stats=combustivel_stats,
        aba_ativa=aba_ativa,
    )


@route('/carros/add', method='GET')
@login_required
def show_add_car_form():
    return render_page(
        'car_form',
        car=None,
        action_url='/carros/add',
        tipos_combustivel=TIPOS_COMBUSTIVEL,
    )


@route('/carros/add', method='POST')
@login_required
def process_add_car():
    session = get_session()
    user_id = session.get('user_id')

    marca = request.forms.get('marca', '').strip()
    modelo = request.forms.get('modelo', '').strip()
    ano = request.forms.get('ano', 2020)
    placa = request.forms.get('placa', '').strip()
    km_atual = request.forms.get('km_atual', 0)
    combustivel = request.forms.get('combustivel', 'Flex')
    cor = request.forms.get('cor', '').strip()
    apelido = request.forms.get('apelido', '').strip()
    observacoes = request.forms.get('observacoes', '').strip()
    criar_kit_padrao = request.forms.get('criar_kit_padrao') == 'on'

    new_car = car_service.create_car(
        marca=marca,
        modelo=modelo,
        ano=ano,
        placa=placa,
        km_atual=km_atual,
        user_id=user_id,
        combustivel=combustivel,
        cor=cor,
        apelido=apelido,
        observacoes=observacoes,
    )

    if criar_kit_padrao and new_car:
        vida_util_service.gerar_kit_padrao_para_veiculo(new_car['id'])

    set_flash(f"Veículo {new_car['marca']} {new_car['modelo']} adicionado com sucesso!", "success")
    return redirect(f"/carros/{new_car['id']}")


@route('/carros/edit/<car_id:int>', method='GET')
@login_required
def show_edit_car_form(car_id):
    session = get_session()
    user_id = session.get('user_id')
    car = car_service.get_car_by_id(car_id, user_id=user_id)
    if not car:
        set_flash("Veículo não encontrado.", "danger")
        return redirect('/carros')

    return render_page(
        'car_form',
        car=car,
        action_url=f"/carros/edit/{car_id}",
        tipos_combustivel=TIPOS_COMBUSTIVEL,
    )


@route('/carros/edit/<car_id:int>', method='POST')
@login_required
def process_edit_car(car_id):
    session = get_session()
    user_id = session.get('user_id')

    marca = request.forms.get('marca', '').strip()
    modelo = request.forms.get('modelo', '').strip()
    ano = request.forms.get('ano', 2020)
    placa = request.forms.get('placa', '').strip()
    km_atual = request.forms.get('km_atual', 0)
    combustivel = request.forms.get('combustivel', 'Flex')
    cor = request.forms.get('cor', '').strip()
    apelido = request.forms.get('apelido', '').strip()
    observacoes = request.forms.get('observacoes', '').strip()

    updated = car_service.update_car(
        car_id=car_id,
        marca=marca,
        modelo=modelo,
        ano=ano,
        placa=placa,
        km_atual=km_atual,
        combustivel=combustivel,
        cor=cor,
        apelido=apelido,
        observacoes=observacoes,
        user_id=user_id,
    )
    if updated:
        set_flash("Dados do veículo atualizados com sucesso!", "success")
        return redirect(f"/carros/{car_id}")
    set_flash("Não foi possível atualizar o veículo.", "danger")
    return redirect('/carros')


@route('/carros/<car_id:int>/atualizar-km', method='POST')
@login_required
def process_update_car_km(car_id):
    session = get_session()
    user_id = session.get('user_id')
    novo_km = request.forms.get('km_atual', 0)
    origem = request.forms.get('redirect_to') or f"/carros/{car_id}"

    updated = car_service.update_car_km(car_id, novo_km, user_id=user_id, force=True)
    if updated:
        set_flash(f"Hodômetro atualizado para {updated['km_atual']:,} km!".replace(",", "."), "success")
    else:
        set_flash("Erro ao atualizar a quilometragem.", "danger")
    return redirect(origem)


@route('/carros/delete/<car_id:int>', method=['GET', 'POST'])
@login_required
def process_delete_car(car_id):
    session = get_session()
    user_id = session.get('user_id')
    if car_service.delete_car(car_id, user_id=user_id):
        set_flash("Veículo e seus registros associados foram removidos.", "info")
    else:
        set_flash("Veículo não encontrado.", "danger")
    return redirect('/carros')
