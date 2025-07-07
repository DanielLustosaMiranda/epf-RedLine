from functools import wraps
from bottle import request, redirect

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        session = request.environ.get('beaker.session')

        if session.get('user_id'):
            # Tudo certo, o usuário está logado. Execute a função original.
            return fn(*args, **kwargs)

        # Usuário não está logado, redirecione para a página de login.
        return redirect('/login')

    return wrapper