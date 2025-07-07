from bottle import route, view, request, redirect
from services import manutencao_service, car_service
from auth_decorator import login_required

@route('/car/<car_id:int>/manutencoes')
@view('manutencao_list')
@login_required
def list_car_manutencoes(car_id):
    car = car_service.get_car_by_id(car_id)
    manutencoes = manutencao_service.get_manutencoes_by_car_id(car_id)
    return dict(car=car, manutencoes=manutencoes)

@route('/car/<car_id:int>/manutencoes/add', method='GET')
@view('manutencao_form')
@login_required
def show_add_manutencao_form(car_id):
    car = car_service.get_car_by_id(car_id)
    return dict(car=car)

@route('/car/<car_id:int>/manutencoes/add', method='POST')
@login_required
def process_add_manutencao(car_id):
    descricao = request.forms.get('descricao')
    data = request.forms.get('data')
    custo = request.forms.get('custo')
    tipo = request.forms.get('tipo')
    km = request.forms.get('km')

    manutencao_service.create_manutencao(descricao, data, custo, tipo, km, car_id)
    redirect(f'/car/{car_id}/manutencoes')

@route('/manutencao/delete/<maintenance_id:int>')
@login_required
def process_delete_manutencao(maintenance_id):
    manutencao_service.delete_manutencao(maintenance_id)
    redirect('/carros')

# Em controllers/manutencao_controller.py

@route('/manutencao/edit/<maintenance_id:int>', method='GET')
@view('manutencao_form')
@login_required
def show_edit_manutencao_form(maintenance_id):
    maintenance = manutencao_service.get_manutencao_by_id(maintenance_id)
    car = car_service.get_car_by_id(maintenance['car_id']) if maintenance else None
    return dict(car=car, manutencao=maintenance)


@route('/manutencao/edit/<maintenance_id:int>', method='POST')
@login_required
def process_edit_manutencao(maintenance_id):
    maintenance = manutencao_service.get_manutencao_by_id(maintenance_id)
    if not maintenance:
        return "Manutenção não encontrada."

    descricao = request.forms.get('descricao')
    data = request.forms.get('data')
    custo = request.forms.get('custo')
    tipo = request.forms.get('tipo')
    km = request.forms.get('km')

    manutencao_service.update_manutencao(maintenance_id, descricao, data, custo, tipo, km)
    redirect(f"/car/{maintenance['car_id']}/manutencoes")