import data_manager
from werkzeug.security import generate_password_hash, check_password_hash

USERS_FILE = 'users.json'

def get_all_users():
    return data_manager.read_data(USERS_FILE)

def get_user_by_id(user_id):
    all_users = get_all_users()
    for user in all_users:
        if user['id'] == int(user_id):
            return user
    return None

def get_user_by_email(email):
    if not email:
        return None
    
    all_users = get_all_users()
    email = email.strip().lower()
    for user in all_users:
        if user['email'].strip().lower() == email:
            return user
    return None

def create_user(name, email, birthdate, password):
    if get_user_by_email(email):
        print(f"Erro: Email '{email}' já cadastrado.")
        return None

    all_users = get_all_users()
    
    last_id = all_users[-1]['id'] if all_users else 0
    new_id = last_id + 1

    new_user = {
        "id": new_id,
        "name": name,
        "email": email,
        "birthdate": birthdate,
        "password_hash": generate_password_hash(password)
    }

    all_users.append(new_user)
    data_manager.write_data(USERS_FILE, all_users)
    return new_user

def authenticate_user(email, password):
    user = get_user_by_email(email)
    
    if user and check_password_hash(user['password_hash'], password):
        return user
        
    return None


def update_user(user_id, name, email, birthdate):
    """Atualiza os dados de um usuário existente."""
    all_users = get_all_users()
    user_found = False
    
    for i, user in enumerate(all_users):
        if user['id'] == int(user_id):
            all_users[i]['name'] = name
            all_users[i]['email'] = email
            all_users[i]['birthdate'] = birthdate
            user_found = True
            break
            
    if user_found:
        data_manager.write_data(USERS_FILE, all_users)
        return all_users[i] # Retorna o usuário atualizado
    
    return None

def delete_user(user_id):
    all_users = get_all_users()
    users_to_keep = [user for user in all_users if user['id'] != int(user_id)]

    if len(users_to_keep) < len(all_users):
        data_manager.write_data(USERS_FILE, users_to_keep)
        return True 
        
    return False 
