from bottle import route, request, redirect
from services import user_service
from utils.auth_decorator import get_session, set_flash
from utils.view_helper import render_page


@route('/login', method='GET')
def show_login_form():
    session = get_session()
    if session.get('user_id'):
        return redirect('/dashboard')
    return render_page('login', error=None)


@route('/login', method='POST')
def process_login():
    session = get_session()
    email = request.forms.get('email', '').strip()
    password = request.forms.get('password', '')

    user = user_service.authenticate_user(email, password)
    if user:
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        session['user_email'] = user['email']
        if hasattr(session, 'save'):
            session.save()
        set_flash(f"Bem-vindo de volta, {user['name']}!", "success")
        return redirect('/dashboard')

    return render_page('login', error="E-mail ou senha inválidos. Verifique suas credenciais.")


@route('/login/demo', method='POST')
def process_demo_login():
    """Login rápido com 1 clique na conta de demonstração."""
    session = get_session()
    user = user_service.get_user_by_email('demo@redline.com')
    if user:
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        session['user_email'] = user['email']
        if hasattr(session, 'save'):
            session.save()
        set_flash("Sessão iniciada no modo Demonstração RedLine!", "info")
        return redirect('/dashboard')
    return redirect('/login')


@route('/logout')
def process_logout():
    session = get_session()
    if hasattr(session, 'delete'):
        session.delete()
    else:
        session.clear()
    return redirect('/login')


@route('/signup', method='GET')
def show_signup_form():
    session = get_session()
    if session.get('user_id'):
        return redirect('/dashboard')
    return render_page('signup', error=None)


@route('/signup', method='POST')
def process_signup():
    name = request.forms.get('name', '').strip()
    email = request.forms.get('email', '').strip()
    birthdate = request.forms.get('birthdate', '').strip()
    telefone = request.forms.get('telefone', '').strip()
    password = request.forms.get('password', '')
    confirm_password = request.forms.get('confirm_password', '')

    if not name or not email or not password:
        return render_page('signup', error="Preencha todos os campos obrigatórios.")

    if len(password) < 4:
        return render_page('signup', error="A senha deve ter pelo menos 4 caracteres.")

    if password != confirm_password:
        return render_page('signup', error="As senhas informadas não coincidem.")

    user = user_service.create_user(name, email, birthdate, password, telefone=telefone)
    if user:
        session = get_session()
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        session['user_email'] = user['email']
        if hasattr(session, 'save'):
            session.save()
        set_flash("Conta criada com sucesso! Bem-vindo ao RedLine.", "success")
        return redirect('/dashboard')

    return render_page('signup', error="Este endereço de e-mail já está cadastrado.")
