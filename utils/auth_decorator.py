from functools import wraps
from bottle import request, redirect


def get_session():
    """Retorna a sessão atual do usuário."""
    return request.environ.get('beaker.session', {})


def set_flash(message: str, category: str = 'success'):
    """Define uma mensagem de feedback (flash) na sessão para exibição na próxima página."""
    session = get_session()
    session['flash_message'] = {'text': message, 'category': category}
    if hasattr(session, 'save'):
        session.save()


def pop_flash():
    """Recupera e remove a mensagem de feedback (flash) da sessão."""
    session = get_session()
    msg = session.pop('flash_message', None)
    if msg and hasattr(session, 'save'):
        session.save()
    return msg


def login_required(fn):
    """Decorator que exige que o usuário esteja autenticado para acessar a rota."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        session = get_session()
        if session and session.get('user_id'):
            return fn(*args, **kwargs)
        return redirect('/login')
    return wrapper
