from bottle import route, request, redirect
from services import user_service
from utils.auth_decorator import login_required, get_session, set_flash
from utils.view_helper import render_page


@route('/perfil', method='GET')
@login_required
def show_profile():
    session = get_session()
    user_id = session.get('user_id')
    user = user_service.get_user_by_id(user_id)
    return render_page('profile', user=user, error=None)


@route('/perfil', method='POST')
@login_required
def update_profile():
    session = get_session()
    user_id = session.get('user_id')
    user = user_service.get_user_by_id(user_id)

    name = request.forms.get('name', '').strip()
    email = request.forms.get('email', '').strip()
    birthdate = request.forms.get('birthdate', '').strip()
    telefone = request.forms.get('telefone', '').strip()
    new_password = request.forms.get('new_password', '').strip()
    confirm_password = request.forms.get('confirm_password', '').strip()

    if new_password and new_password != confirm_password:
        return render_page('profile', user=user, error="A confirmação da nova senha não confere.")

    updated = user_service.update_user(
        user_id=user_id,
        name=name,
        email=email,
        birthdate=birthdate,
        telefone=telefone,
        new_password=new_password if new_password else None,
    )
    if not updated:
        return render_page('profile', user=user, error="E-mail já em uso por outra conta.")

    session['user_name'] = updated['name']
    session['user_email'] = updated['email']
    if hasattr(session, 'save'):
        session.save()

    set_flash("Perfil atualizado com sucesso!", "success")
    return redirect('/perfil')


# Compatibilidade com rotas legadas /users
@route('/users')
@login_required
def redirect_users():
    return redirect('/perfil')


@route('/users/edit/<user_id:int>')
@login_required
def redirect_edit_user(user_id):
    return redirect('/perfil')
