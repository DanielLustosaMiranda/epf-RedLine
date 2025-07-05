from bottle import Bottle
from controllers.user_controller import user_routes
from controllers.auth_controller import AuthController

def init_controllers(app: Bottle):
    app.merge(user_routes)
    auth = AuthController()
    
    app.route('/login', method=['GET', 'POST'], callback=auth.login)
    app.route('/signup', method=['GET', 'POST'], callback=auth.signup)

    print("✅ Rotas de autenticação carregadas!")
