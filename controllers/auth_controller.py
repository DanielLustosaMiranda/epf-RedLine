from bottle import route, view, request, redirect
from services import user_service

@route('/login', method='GET')
@view('login')
def show_login_form():
    return dict(error=None)

@route('/login', method='POST')
def process_login():
    session = request.environ.get('beaker.session')
    email = request.forms.get('email')
    password = request.forms.get('password')

    user = user_service.authenticate_user(email, password)

    if user:
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        redirect('/')
    else:
        return view('login', error="Email ou senha inválidos.")

@route('/logout')
def process_logout():
    session = request.environ.get('beaker.session')
    session.delete()
    redirect('/login')

@route('/signup', method='GET')
@view('signup')
def show_signup_form():
    return dict(error=None)

@route('/signup', method='POST')
def process_signup():
    name = request.forms.get('name')
    email = request.forms.get('email')
    birthdate = request.forms.get('birthdate')
    password = request.forms.get('password')
    confirm_password = request.forms.get('confirm_password')

    if password != confirm_password:
        return view('signup', error="As senhas não coincidem.")
    
    user = user_service.create_user(name, email, birthdate, password)

    if user:
        redirect('/login') # Redireciona para o login após o sucesso
    else:
        return view('signup', error="Este email já está em uso.")