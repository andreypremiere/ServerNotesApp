from fastapi import HTTPException, status

from models.models import UserCreate, UserOut
from repositories.userRepository import UserRepository, pwd_context


class UserService:
    @staticmethod
    async def register(db, user: UserCreate) -> UserOut:
        """Register a new user and return user data."""
        user_record = await UserRepository.create(db, user)
        return UserOut(**dict(user_record))

    @staticmethod
    async def authenticate(db, nickname: str, password: str):
        """Authenticate user and return user data if credentials are valid."""
        user = await UserRepository.get_by_nickname(db, nickname)
        if not user or not pwd_context.verify(password, user['hash_password']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect nickname or password"
            )
        return user
