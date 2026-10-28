from datetime import date
from bottle import route, request, redirect
from config import (
    TIPOS_MANUTENCAO,
    TIPOS_COMBUSTIVEL,
    PRESETS_MANUTENCAO_PROGRAMADA,
    KIT_PADRAO_VIDA_UTIL,
)
from services import (
    car_service,
    manutencao_service,
    programada_service,
    vida_util_service,
    abastecimento_service,
)
from utils.auth_decorator import login_required, get_session, set_flash
from utils.view_helper import render_page


# ==============================================================================
# 1. HISTÓRICO DE MANUTENÇÕES REALIZADAS
# ==============================================================================

@route('/manutencoes')
@login_required
def list_all_user_manutencoes():
    session = get_session()
    user_id = session.get('user_id')
    car_id_param = request.query.get('car_id', '').strip()
    tipo_param = request.query.get('tipo', '').strip()
    busca_param = request.query.get('q', '').strip()

    selected_car_id = int(car_id_param) if car_id_param.isdigit() else None
    car = car_service.get_car_by_id(selected_car_id, user_id=user_id) if selected_car_id else None
    cars = car_service.get_cars_by_user_id(user_id)

    manutencoes = manutencao_service.get_manutencoes_by_user(
        user_id=user_id,
        car_id=selected_car_id,
        tipo=tipo_param,
        busca=busca_param,
    )
    total_custo = round(sum(m['custo'] for m in manutencoes), 2)

    return render_page(
        'manutencao_list',
        car=car,
        cars=cars,
        manutencoes=manutencoes,
        total_custo=total_custo,
        tipos_manutencao=TIPOS_MANUTENCAO,
        filtro_car_id=selected_car_id,
        filtro_tipo=tipo_param,
        filtro_busca=busca_param,
    )


@route('/car/<car_id:int>/manutencoes')
@login_required
def list_car_manutencoes(car_id):
    session = get_session()
    user_id = session.get('user_id')
    car = car_service.get_car_by_id(car_id, user_id=user_id)
    if not car:
        set_flash("Veículo não encontrado.", "danger")
        return redirect('/carros')

    cars = car_service.get_cars_by_user_id(user_id)
    manutencoes = manutencao_service.get_manutencoes_by_user(user_id=user_id, car_id=car_id)
    total_custo = round(sum(m['custo'] for m in manutencoes), 2)

    return render_page(
        'manutencao_list',
        car=car,
        cars=cars,
        manutencoes=manutencoes,
        total_custo=total_custo,
        tipos_manutencao=TIPOS_MANUTENCAO,
        filtro_car_id=car_id,
        filtro_tipo='',
        filtro_busca='',
    )


@route('/car/<car_id:int>/manutencoes/add', method='GET')
@login_required
def show_add_manutencao_form(car_id):
    session = get_session()
    user_id = session.get('user_id')
    car = car_service.get_car_by_id(car_id, user_id=user_id)
    if not car:
        set_flash("Veículo não encontrado.", "danger")
        return redirect('/carros')

    return render_page(
        'manutencao_form',
        car=car,
        manutencao=None,
        tipos_manutencao=TIPOS_MANUTENCAO,
        hoje=date.today().isoformat(),
    )


@route('/car/<car_id:int>/manutencoes/add', method='POST')
@login_required
def process_add_manutencao(car_id):
    session = get_session()
    user_id = session.get('user_id')
    car = car_service.get_car_by_id(car_id, user_id=user_id)
    if not car:
        return redirect('/carros')

    descricao = request.forms.get('descricao', '').strip()
    data = request.forms.get('data', date.today().isoformat())
    custo = request.forms.get('custo', 0.0)
    tipo = request.forms.get('tipo', 'Preventiva')
    km = request.forms.get('km', car['km_atual'])
    oficina = request.forms.get('oficina', '').strip()
    garantia_meses = request.forms.get('garantia_meses', 0)
    observacoes = request.forms.get('observacoes', '').strip()

    manutencao_service.create_manutencao(
        descricao=descricao,
        data=data,
        custo=custo,
        tipo=tipo,
        km=km,
        car_id=car_id,
        oficina=oficina,
        garantia_meses=garantia_meses,
        observacoes=observacoes,
        atualizar_km_carro=True,
    )
    set_flash("Manutenção registrada com sucesso!", "success")
    return redirect(f"/carros/{car_id}?tab=historico")


@route('/manutencao/edit/<maintenance_id:int>', method='GET')
@login_required
def show_edit_manutencao_form(maintenance_id):
    session = get_session()
    user_id = session.get('user_id')
    maintenance = manutencao_service.get_manutencao_by_id(maintenance_id)
    if not maintenance:
        set_flash("Manutenção não encontrada.", "danger")
        return redirect('/manutencoes')

    car = car_service.get_car_by_id(maintenance['car_id'], user_id=user_id)
    if not car:
        return redirect('/carros')

    return render_page(
        'manutencao_form',
        car=car,
        manutencao=maintenance,
        tipos_manutencao=TIPOS_MANUTENCAO,
        hoje=date.today().isoformat(),
    )


@route('/manutencao/edit/<maintenance_id:int>', method='POST')
@login_required
def process_edit_manutencao(maintenance_id):
    session = get_session()
    user_id = session.get('user_id')
    maintenance = manutencao_service.get_manutencao_by_id(maintenance_id)
    if not maintenance:
        return redirect('/manutencoes')

    car = car_service.get_car_by_id(maintenance['car_id'], user_id=user_id)
    if not car:
        return redirect('/carros')

    descricao = request.forms.get('descricao', '').strip()
    data = request.forms.get('data', '')
    custo = request.forms.get('custo', 0.0)
    tipo = request.forms.get('tipo', 'Preventiva')
    km = request.forms.get('km', 0)
    oficina = request.forms.get('oficina', '').strip()
    garantia_meses = request.forms.get('garantia_meses', 0)
    observacoes = request.forms.get('observacoes', '').strip()

    manutencao_service.update_manutencao(
        maintenance_id=maintenance_id,
        descricao=descricao,
        data=data,
        custo=custo,
        tipo=tipo,
        km=km,
        oficina=oficina,
        garantia_meses=garantia_meses,
        observacoes=observacoes,
    )
    set_flash("Registro de manutenção atualizado!", "success")
    return redirect(f"/carros/{car['id']}?tab=historico")


@route('/manutencao/delete/<maintenance_id:int>', method=['GET', 'POST'])
@login_required
def process_delete_manutencao(maintenance_id):
    session = get_session()
    user_id = session.get('user_id')
    maintenance = manutencao_service.get_manutencao_by_id(maintenance_id)
    if maintenance:
        car = car_service.get_car_by_id(maintenance['car_id'], user_id=user_id)
        if car:
            manutencao_service.delete_manutencao(maintenance_id)
            set_flash("Manutenção excluída.", "info")
            return redirect(f"/carros/{car['id']}?tab=historico")
    return redirect('/manutencoes')


# ==============================================================================
# 2. MANUTENÇÕES PROGRAMADAS (REVISÕES AGENDADAS POR DATA E KM)
# ==============================================================================

@route('/car/<car_id:int>/programadas/add', method='GET')
@login_required
def show_add_programada_form(car_id):
    session = get_session()
    user_id = session.get('user_id')
    car = car_service.get_car_by_id(car_id, user_id=user_id)
    if not car:
        return redirect('/carros')

    return render_page(
        'programada_form',
        car=car,
        programada=None,
        presets=PRESETS_MANUTENCAO_PROGRAMADA,
        hoje=date.today().isoformat(),
    )


@route('/car/<car_id:int>/programadas/add', method='POST')
@login_required
def process_add_programada(car_id):
    session = get_session()
    user_id = session.get('user_id')
    car = car_service.get_car_by_id(car_id, user_id=user_id)
    if not car:
        return redirect('/carros')

    descricao = request.forms.get('descricao', '').strip()
    frequencia_dias = request.forms.get('frequencia_dias', 180)
    ultima_data = request.forms.get('ultima_data', date.today().isoformat())
    frequencia_km = request.forms.get('frequencia_km', 10000)
    ultimo_km = request.forms.get('ultimo_km', car['km_atual'])
    custo_estimado = request.forms.get('custo_estimado', 0.0)
    observacoes = request.forms.get('observacoes', '').strip()

    programada_service.create_programada(
        id_veiculo=car_id,
        descricao=descricao,
        frequencia_dias=frequencia_dias,
        ultima_data=ultima_data,
        frequencia_km=frequencia_km,
        ultimo_km=ultimo_km,
        custo_estimado=custo_estimado,
        observacoes=observacoes,
    )
    set_flash("Manutenção programada cadastrada com sucesso!", "success")
    return redirect(f"/carros/{car_id}?tab=programadas")


@route('/programada/edit/<prog_id:int>', method='GET')
@login_required
def show_edit_programada_form(prog_id):
    session = get_session()
    user_id = session.get('user_id')
    prog = programada_service.get_programada_by_id(prog_id)
    if not prog:
        return redirect('/carros')

    car = car_service.get_car_by_id(prog['id_veiculo'], user_id=user_id)
    if not car:
        return redirect('/carros')

    return render_page(
        'programada_form',
        car=car,
        programada=prog,
        presets=PRESETS_MANUTENCAO_PROGRAMADA,
        hoje=date.today().isoformat(),
    )


@route('/programada/edit/<prog_id:int>', method='POST')
@login_required
def process_edit_programada(prog_id):
    session = get_session()
    user_id = session.get('user_id')
    prog = programada_service.get_programada_by_id(prog_id)
    if not prog:
        return redirect('/carros')

    car = car_service.get_car_by_id(prog['id_veiculo'], user_id=user_id)
    if not car:
        return redirect('/carros')

    descricao = request.forms.get('descricao', '').strip()
    frequencia_dias = request.forms.get('frequencia_dias', 180)
    ultima_data = request.forms.get('ultima_data', '')
    frequencia_km = request.forms.get('frequencia_km', 10000)
    ultimo_km = request.forms.get('ultimo_km', 0)
    custo_estimado = request.forms.get('custo_estimado', 0.0)
    observacoes = request.forms.get('observacoes', '').strip()

    programada_service.update_programada(
        prog_id=prog_id,
        descricao=descricao,
        frequencia_dias=frequencia_dias,
        ultima_data=ultima_data,
        frequencia_km=frequencia_km,
        ultimo_km=ultimo_km,
        custo_estimado=custo_estimado,
        observacoes=observacoes,
    )
    set_flash("Agendamento atualizado!", "success")
    return redirect(f"/carros/{car['id']}?tab=programadas")


@route('/programada/concluir/<prog_id:int>', method=['GET', 'POST'])
@login_required
def process_concluir_programada(prog_id):
    session = get_session()
    user_id = session.get('user_id')
    prog = programada_service.get_programada_by_id(prog_id)
    if not prog:
        return redirect('/carros')

    car = car_service.get_car_by_id(prog['id_veiculo'], user_id=user_id)
    if not car:
        return redirect('/carros')

    updated = programada_service.concluir_programada(prog_id)
    if updated:
        set_flash(
            f"'{prog['descricao']}' registrada no histórico e agendada para o próximo ciclo!",
            "success",
        )
    return redirect(f"/carros/{car['id']}?tab=programadas")


@route('/programada/delete/<prog_id:int>', method=['GET', 'POST'])
@login_required
def process_delete_programada(prog_id):
    session = get_session()
    user_id = session.get('user_id')
    prog = programada_service.get_programada_by_id(prog_id)
    if prog:
        car = car_service.get_car_by_id(prog['id_veiculo'], user_id=user_id)
        if car:
            programada_service.delete_programada(prog_id)
            set_flash("Manutenção programada removida.", "info")
            return redirect(f"/carros/{car['id']}?tab=programadas")
    return redirect('/carros')


# ==============================================================================
# 3. ITENS DE VIDA ÚTIL (PEÇAS E COMPONENTES MONITORADOS)
# ==============================================================================

@route('/car/<car_id:int>/vida-util/add', method='GET')
@login_required
def show_add_vida_util_form(car_id):
    session = get_session()
    user_id = session.get('user_id')
    car = car_service.get_car_by_id(car_id, user_id=user_id)
    if not car:
        return redirect('/carros')

    return render_page(
        'vida_util_form',
        car=car,
        item=None,
        sugestoes=KIT_PADRAO_VIDA_UTIL,
        hoje=date.today().isoformat(),
    )


@route('/car/<car_id:int>/vida-util/add', method='POST')
@login_required
def process_add_vida_util(car_id):
    session = get_session()
    user_id = session.get('user_id')
    car = car_service.get_car_by_id(car_id, user_id=user_id)
    if not car:
        return redirect('/carros')

    nome_item = request.forms.get('nome_item', '').strip()
    data_instalacao = request.forms.get('data_instalacao', date.today().isoformat())
    validade_anos = request.forms.get('validade_anos', 1.0)
    km_instalacao = request.forms.get('km_instalacao', car['km_atual'])
    validade_km = request.forms.get('validade_km', 10000)
    marca_peca = request.forms.get('marca_peca', '').strip()
    observacoes = request.forms.get('observacoes', '').strip()

    vida_util_service.create_item(
        id_veiculo=car_id,
        nome_item=nome_item,
        data_instalacao=data_instalacao,
        validade_anos=validade_anos,
        km_instalacao=km_instalacao,
        validade_km=validade_km,
        marca_peca=marca_peca,
        observacoes=observacoes,
    )
    set_flash(f"Componente '{nome_item}' adicionado ao monitoramento!", "success")
    return redirect(f"/carros/{car_id}?tab=vida-util")


@route('/car/<car_id:int>/vida-util/kit-padrao', method='POST')
@login_required
def process_gerar_kit_padrao(car_id):
    session = get_session()
    user_id = session.get('user_id')
    car = car_service.get_car_by_id(car_id, user_id=user_id)
    if not car:
        return redirect('/carros')

    criados = vida_util_service.gerar_kit_padrao_para_veiculo(car_id)
    if criados > 0:
        set_flash(f"{criados} componentes essenciais foram adicionados ao monitoramento!", "success")
    else:
        set_flash("Todos os componentes do kit essencial já estão cadastrados neste veículo.", "info")
    return redirect(f"/carros/{car_id}?tab=vida-util")


@route('/vida-util/edit/<item_id:int>', method='GET')
@login_required
def show_edit_vida_util_form(item_id):
    session = get_session()
    user_id = session.get('user_id')
    item = vida_util_service.get_item_by_id(item_id)
    if not item:
        return redirect('/carros')

    car = car_service.get_car_by_id(item['id_veiculo'], user_id=user_id)
    if not car:
        return redirect('/carros')

    return render_page(
        'vida_util_form',
        car=car,
        item=item,
        sugestoes=KIT_PADRAO_VIDA_UTIL,
        hoje=date.today().isoformat(),
    )


@route('/vida-util/edit/<item_id:int>', method='POST')
@login_required
def process_edit_vida_util(item_id):
    session = get_session()
    user_id = session.get('user_id')
    item = vida_util_service.get_item_by_id(item_id)
    if not item:
        return redirect('/carros')

    car = car_service.get_car_by_id(item['id_veiculo'], user_id=user_id)
    if not car:
        return redirect('/carros')

    nome_item = request.forms.get('nome_item', '').strip()
    data_instalacao = request.forms.get('data_instalacao', '')
    validade_anos = request.forms.get('validade_anos', 1.0)
    km_instalacao = request.forms.get('km_instalacao', 0)
    validade_km = request.forms.get('validade_km', 10000)
    marca_peca = request.forms.get('marca_peca', '').strip()
    observacoes = request.forms.get('observacoes', '').strip()

    vida_util_service.update_item(
        item_id=item_id,
        nome_item=nome_item,
        data_instalacao=data_instalacao,
        validade_anos=validade_anos,
        km_instalacao=km_instalacao,
        validade_km=validade_km,
        marca_peca=marca_peca,
        observacoes=observacoes,
    )
    set_flash("Dados do componente atualizados!", "success")
    return redirect(f"/carros/{car['id']}?tab=vida-util")


@route('/vida-util/renovar/<item_id:int>', method=['GET', 'POST'])
@login_required
def process_renovar_vida_util(item_id):
    session = get_session()
    user_id = session.get('user_id')
    item = vida_util_service.get_item_by_id(item_id)
    if not item:
        return redirect('/carros')

    car = car_service.get_car_by_id(item['id_veiculo'], user_id=user_id)
    if not car:
        return redirect('/carros')

    vida_util_service.renovar_item(item_id, registrar_historico=True)
    set_flash(
        f"Peça '{item['nome_item']}' renovada para 100% de vida útil e registrada no histórico!",
        "success",
    )
    return redirect(f"/carros/{car['id']}?tab=vida-util")


@route('/vida-util/delete/<item_id:int>', method=['GET', 'POST'])
@login_required
def process_delete_vida_util(item_id):
    session = get_session()
    user_id = session.get('user_id')
    item = vida_util_service.get_item_by_id(item_id)
    if item:
        car = car_service.get_car_by_id(item['id_veiculo'], user_id=user_id)
        if car:
            vida_util_service.delete_item(item_id)
            set_flash("Componente removido do monitoramento.", "info")
            return redirect(f"/carros/{car['id']}?tab=vida-util")
    return redirect('/carros')


# ==============================================================================
# 4. CONTROLE DE ABASTECIMENTOS E CONSUMO
# ==============================================================================

@route('/car/<car_id:int>/abastecimentos/add', method='GET')
@login_required
def show_add_abastecimento_form(car_id):
    session = get_session()
    user_id = session.get('user_id')
    car = car_service.get_car_by_id(car_id, user_id=user_id)
    if not car:
        return redirect('/carros')

    return render_page(
        'abastecimento_form',
        car=car,
        tipos_combustivel=TIPOS_COMBUSTIVEL,
        hoje=date.today().isoformat(),
    )


@route('/car/<car_id:int>/abastecimentos/add', method='POST')
@login_required
def process_add_abastecimento(car_id):
    session = get_session()
    user_id = session.get('user_id')
    car = car_service.get_car_by_id(car_id, user_id=user_id)
    if not car:
        return redirect('/carros')

    data = request.forms.get('data', date.today().isoformat())
    km = request.forms.get('km', car['km_atual'])
    combustivel = request.forms.get('combustivel', car.get('combustivel', 'Gasolina'))
    litros = request.forms.get('litros', 1.0)
    valor_total = request.forms.get('valor_total', 0.0)
    posto = request.forms.get('posto', '').strip()
    tanque_cheio = request.forms.get('tanque_cheio') == 'on'

    abastecimento_service.create_abastecimento(
        car_id=car_id,
        data=data,
        km=km,
        combustivel=combustivel,
        litros=litros,
        valor_total=valor_total,
        posto=posto,
        tanque_cheio=tanque_cheio,
    )
    set_flash("Abastecimento registrado com sucesso!", "success")
    return redirect(f"/carros/{car_id}?tab=abastecimentos")


@route('/abastecimento/delete/<abast_id:int>', method=['GET', 'POST'])
@login_required
def process_delete_abastecimento(abast_id):
    session = get_session()
    user_id = session.get('user_id')
    abast = abastecimento_service.get_abastecimento_by_id(abast_id)
    if abast:
        car = car_service.get_car_by_id(abast['car_id'], user_id=user_id)
        if car:
            abastecimento_service.delete_abastecimento(abast_id)
            set_flash("Registro de abastecimento removido.", "info")
            return redirect(f"/carros/{car['id']}?tab=abastecimentos")
    return redirect('/carros')
