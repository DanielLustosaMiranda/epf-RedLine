from bottle import request, response, template, route, redirect
from models.user import User
from services.user_service import UserService

user_service = UserService()

class AuthController:

    @route('/login', method=['GET', 'POST'])
    def login(self):
        if request.method == 'GET':
            return template('login')
        elif request.method == 'POST':
            username = request.forms.get('user')
            password = request.forms.get('password')
            user = user_service.authenticate(username, password)
            if user:
                redirect(f"/dashboard/{user.id}")
            else:
                return template('login', error="Usuário ou senha inválidos.")

    @route('/signup', method=['GET', 'POST'])
    def signup(self):
        if request.method == 'GET':
            return template('signup', error=None)

        elif request.method == 'POST':
            name = request.forms.get('name')
            email = request.forms.get('email')
            birthdate = request.forms.get('birthdate')
            username = request.forms.get('username')
            password = request.forms.get('password')

            
            if user_service.find_user_by_username(username):
                return template('signup', error="Usuário já existe.")

           
            last_id = max([u.id for u in user_service.get_all()], default=0)
            new_id = last_id + 1

            new_user = User(
                id=new_id,
                name=name,
                email=email,
                birthdate=birthdate,
                username=username,
                password=password
            )

            user_service.add_user(new_user)
            redirect(f"/dashboard/{new_user.id}")

       