from models.user import User
from services import data_manager
from utils.security import generate_password_hash, check_password_hash

USERS_FILE = 'users.json'


def get_all_users() -> list[dict]:
    raw = data_manager.read_data(USERS_FILE)
    return [User.from_dict(u).to_dict() for u in raw]


def get_user_by_id(user_id) -> dict | None:
    if user_id is None:
        return None
    target_id = int(user_id)
    for u in get_all_users():
        if u['id'] == target_id:
            return u
    return None


def get_user_by_email(email: str) -> dict | None:
    if not email:
        return None
    email_clean = email.strip().lower()
    for u in get_all_users():
        if u['email'].strip().lower() == email_clean:
            return u
    return None


def create_user(name: str, email: str, birthdate: str, password: str, telefone: str = "") -> dict | None:
    if get_user_by_email(email):
        return None

    all_users = data_manager.read_data(USERS_FILE)
    new_id = data_manager.next_id(all_users)

    user_obj = User(
        id=new_id,
        name=name,
        email=email,
        birthdate=birthdate,
        password_hash=generate_password_hash(password),
        telefone=telefone,
    )
    user_dict = user_obj.to_dict()
    all_users.append(user_dict)
    data_manager.write_data(USERS_FILE, all_users)
    return user_dict


def authenticate_user(email: str, password: str) -> dict | None:
    user = get_user_by_email(email)
    if user and check_password_hash(user.get('password_hash', ''), password):
        return user
    return None


def update_user(user_id, name: str, email: str, birthdate: str, telefone: str = "", new_password: str = None) -> dict | None:
    all_users = data_manager.read_data(USERS_FILE)
    target_id = int(user_id)
    email_clean = (email or "").strip().lower()

    # Verifica se outro usuário já utiliza este e-mail
    for u in all_users:
        if int(u.get('id', 0)) != target_id and u.get('email', '').strip().lower() == email_clean:
            return None

    for i, u in enumerate(all_users):
        if int(u.get('id', 0)) == target_id:
            u['name'] = (name or "").strip()
            u['email'] = email_clean
            u['birthdate'] = birthdate
            u['telefone'] = (telefone or "").strip()
            if new_password and new_password.strip():
                u['password_hash'] = generate_password_hash(new_password.strip())
            all_users[i] = User.from_dict(u).to_dict()
            data_manager.write_data(USERS_FILE, all_users)
            return all_users[i]
    return None


def delete_user(user_id) -> bool:
    all_users = data_manager.read_data(USERS_FILE)
    target_id = int(user_id)
    users_to_keep = [u for u in all_users if int(u.get('id', 0)) != target_id]
    if len(users_to_keep) < len(all_users):
        data_manager.write_data(USERS_FILE, users_to_keep)
        return True
    return False
