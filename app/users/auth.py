from passlib.context import CryptContext


pdw_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return pdw_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pdw_context.verify(plain_password, hashed_password)