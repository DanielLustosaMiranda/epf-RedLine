from bottle import route, view, request, redirect, template
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
        # Corrected line
        session['user_name'] = user['name'] # Use 'name' instead of 'user_name'
        redirect('/')
    else:
        # Use template() here!
        return template('login', error="Email ou senha inválidos.")

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
        # Use template() here!
        return template('signup', error="As senhas não coincidem.")
    
    user = user_service.create_user(name, email, birthdate, password)

    if user:
        redirect('/login') # Redireciona para o login após o sucesso
    else:
        # Use template() here!
        return template('signup', error="Este email já está em uso.")