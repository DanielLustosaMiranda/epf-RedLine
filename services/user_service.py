from bottle import request
from models.user import UserModel, User
import json
import os
from models.user import User

class UserService:
    def __init__(self):
        self.user_model = UserModel()


    def get_all(self):
        users = self.user_model.get_all()
        return users


    def save(self):
        last_id = max([u.id for u in self.user_model.get_all()], default=0)
        new_id = last_id + 1
        name = request.forms.get('name')
        email = request.forms.get('email')
        birthdate = request.forms.get('birthdate')

        user = User(id=new_id, name=name, email=email, birthdate=birthdate)
        self.user_model.add_user(user)


    def get_by_id(self, user_id):
        return self.user_model.get_by_id(user_id)


    def edit_user(self, user):
        name = request.forms.get('name')
        email = request.forms.get('email')
        birthdate = request.forms.get('birthdate')

        user.name = name
        user.email = email
        user.birthdate = birthdate

        self.user_model.update_user(user)


    def delete_user(self, user_id):
        self.user_model.delete_user(user_id)

    def create_account(self):
        username = request.forms.get('username')
        password = request.forms.get('password')

        existing = self.user_model.get_by_username(username)
        if existing:
            return False
        
        last_id = max([u.id for u in self.user_model.get_all()], default=0)
        new_user = User(id=last_id + 1, username=username, password=password)
        self.user_model.add_user(new_user)
        return True
    
    def authenticate(self):
        username = request.forms.get('username')
        password = request.forms.get('password')

        user = self.user_model.get_by_username(username)
        if user and user.password == password:
            return user  # sucesso
        return None 
    
    def find_user_by_username(username):
        users = load_users()
        for user in users:
            if user.username == username:
                return user
        return None