import sys
sys.dont_write_bytecode = True

from bottle import run, route, static_file, TEMPLATE_PATH, default_app, redirect
from config import VIEWS_DIR, STATIC_DIR, SESSION_OPTS, HOST, PORT, DEBUG
from utils.auth_decorator import get_session
from utils.session_middleware import create_session_middleware

if VIEWS_DIR not in TEMPLATE_PATH:
    TEMPLATE_PATH.insert(0, VIEWS_DIR)

# Importa todos os controladores para registrar as rotas
import controllers.auth_controller
import controllers.dashboard_controller
import controllers.car_controller
import controllers.manutencao_controller
import controllers.user_controller


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=STATIC_DIR)


@route('/')
def index():
    session = get_session()
    if session and session.get('user_id'):
        return redirect('/dashboard')
    return redirect('/login')


app_with_sessions = create_session_middleware(default_app(), SESSION_OPTS)

if __name__ == '__main__':
    run(app=app_with_sessions, host=HOST, port=PORT, reloader=DEBUG, debug=DEBUG)
