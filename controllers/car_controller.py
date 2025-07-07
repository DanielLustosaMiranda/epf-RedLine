from bottle import route, view, request, redirect, template
from services import car_service
from auth_decorator import login_required

# --- Rotas para listar e adicionar carros ---

@route('/carros')
@view('car_list')
@login_required
def list_user_cars():
    session = request.environ.get('beaker.session')
    user_id = session.get('user_id')

    cars = car_service.get_cars_by_user_id(user_id)
    return dict(cars=cars)

@route('/carros/add', method='GET')
@view('car_form')
def show_add_car_form():
    session = request.environ.get('beaker.session')
    if not session.get('user_id'):
        redirect('/login')
        
    return dict(car=None, action_url='/carros/add')

@route('/carros/add', method='POST')
def process_add_car():
    session = request.environ.get('beaker.session')
    user_id = session.get('user_id')

    if not user_id:
        redirect('/login')

    marca = request.forms.get('marca')
    modelo = request.forms.get('modelo')
    ano = request.forms.get('ano')
    placa = request.forms.get('placa')
    km_atual = request.forms.get('km_atual')

    car_service.create_car(marca, modelo, ano, placa, km_atual, user_id)
    redirect('/carros')


@route('/carros/edit/<car_id:int>')
@view('car_form')
def show_edit_car_form(car_id):
    session = request.environ.get('beaker.session')
    if not session.get('user_id'):
        redirect('/login')

    car = car_service.get_car_by_id(car_id)

    return dict(car=car, action_url=f"/carros/edit/{car_id}")

@route('/carros/edit/<car_id:int>', method='POST')
def process_edit_car(car_id):
    marca = request.forms.get('marca')
    modelo = request.forms.get('modelo')
    ano = request.forms.get('ano')
    placa = request.forms.get('placa')
    km_atual = request.forms.get('km_atual')

    car_service.update_car(car_id, marca, modelo, ano, placa, km_atual)

    redirect('/carros')

@route('/carros/delete/<car_id:int>')
def process_delete_car(car_id):
    session = request.environ.get('beaker.session')
    if not session.get('user_id'):
        redirect('/login')

    car_service.delete_car(car_id)

    redirect('/carros')