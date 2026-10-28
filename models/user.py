class User:
    """Representa um usuário do sistema RedLine."""

    def __init__(
        self,
        id,
        name,
        email,
        birthdate,
        password_hash=None,
        username=None,
        telefone="",
    ):
        self.id = int(id) if id is not None else None
        self.name = (name or "").strip()
        self.email = (email or "").strip().lower()
        self.birthdate = birthdate or ""
        self.password_hash = password_hash or ""
        self.username = username or self.email.split("@")[0]
        self.telefone = (telefone or "").strip()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "birthdate": self.birthdate,
            "username": self.username,
            "telefone": self.telefone,
            "password_hash": self.password_hash,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(
            id=data.get("id"),
            name=data.get("name", ""),
            email=data.get("email", ""),
            birthdate=data.get("birthdate", ""),
            password_hash=data.get("password_hash") or data.get("password", ""),
            username=data.get("username"),
            telefone=data.get("telefone", ""),
        )

    def __repr__(self) -> str:
        return f"User(id={self.id}, name='{self.name}', email='{self.email}')"
