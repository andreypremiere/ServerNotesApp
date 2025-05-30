from passlib.context import CryptContext
from models.models import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRepository:
    @staticmethod
    async def create(db, user: UserCreate):
        """Create a new user in the database."""
        hashed_password = pwd_context.hash(user.password)
        return await db.fetchrow(
            "INSERT INTO users (nickname, hash_password) VALUES ($1, $2) RETURNING id, nickname",
            user.nickname, hashed_password
        )

    @staticmethod
    async def get_by_nickname(db, nickname: str):
        """Get user by nickname."""
        return await db.fetchrow("SELECT * FROM users WHERE nickname = $1", nickname)