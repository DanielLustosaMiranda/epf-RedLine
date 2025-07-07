from bottle import route, view, request, redirect
from services import user_service

# Rota para listar todos os usuários
@route('/users')
@view('users')
def list_all_users():
    users = user_service.get_all_users()
    return dict(users=users)

# Rotas para adicionar um novo usuário
@route('/users/add', method='GET')
@view('user_form')
def show_add_user_form():
    # Para o formulário de adição, não há dados de usuário existentes
    return dict(user=None, action_url='/users/add')

@route('/users/add', method='POST')
def process_add_user():
    name = request.forms.get('name')
    email = request.forms.get('email')
    birthdate = request.forms.get('birthdate')
    password = request.forms.get('password')

    user_service.create_user(name, email, birthdate, password)
    redirect('/users')

# Rotas para editar um usuário existente
@route('/users/edit/<user_id>')
@view('user_form')
def show_edit_user_form(user_id):
    user = user_service.get_user_by_id(user_id)
    return dict(user=user, action_url=f'/users/edit/{user_id}')

@route('/users/edit/<user_id>', method='POST')
def process_edit_user(user_id):
    name = request.forms.get('name')
    email = request.forms.get('email')
    birthdate = request.forms.get('birthdate')
    
    user_service.update_user(user_id, name, email, birthdate)
    redirect('/users')

# Rota para deletar um usuário
@route('/users/delete/<user_id>')
def process_delete_user(user_id):
    user_service.delete_user(user_id)
    redirect('/users')