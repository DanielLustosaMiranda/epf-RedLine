from bottle import run, route, view, static_file, TEMPLATE_PATH, default_app, request, template, redirect
from beaker.middleware import SessionMiddleware
from services import user_service
from controllers import car_controller
import controllers.manutencao_controller 

TEMPLATE_PATH.insert(0, './views/')

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 3600, # 1 hora
    'session.data_dir': './data/sessions',
    'session.auto': True
}

import controllers.user_controller
import controllers.auth_controller

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')

@route('/')
def index():
    session = request.environ.get('beaker.session')
    
    if session.get('user_id'):
        redirect('/carros')
    else:
        redirect('/login')
# Pega a aplicação padrão do Bottle e a "envelopa" com o middleware de sessão
app_with_sessions = SessionMiddleware(default_app(), session_opts)


if __name__ == '__main__':
    run(app=app_with_sessions, host='0.0.0.0', port=8080, reloader=True, debug=True)