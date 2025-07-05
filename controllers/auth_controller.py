from bottle import request, response, template
from models.user import User
import services.user_service as user_service

class AuthController:
    def login(self):
        if request.method == 'GET':
            return template('login')
        elif request.method == 'POST':
            username = request.forms.get('user')
            password = request.forms.get('pass')
            user_service.find_user_by_username(username)
    
            if User and User.password == password:
                return f"Bem vindo, {username}!"
            else:
                return template('login', error="Usuario ou senha não encontrados. Verifique corretamente!")
    
    def signup(selft):
        if request.method == 'GET':
            return template('signup')
        elif request.method == "POST":
            username = request.forms.get('user')
            password = request.forms.get('pass')
            return f"Usuario {username} cadastrado com sucesso!"
        
        if user_service.find_user_by_username(username):
            return template('signup', error="Usuário já existe")
        
        new_user = User(username, password)
        user_service.add_user(new_user)
        redirect('/login')
