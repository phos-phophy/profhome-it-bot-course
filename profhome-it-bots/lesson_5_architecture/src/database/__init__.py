from ..schemas import User


fake_db = {}


async def get_user(username: str, role: str = None) -> User | None:
    user = fake_db.get(username)

    if not role or not user:
        return user

    return user if user.role == role else None


async def add_user(user: User):
    fake_db[user.username] = user
