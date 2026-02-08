from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    # bcrypt limit: 72 bytes
    safe = password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    return pwd_context.hash(safe)


def verify_password(password: str, hashed: str) -> bool:
    safe = password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    return pwd_context.verify(safe, hashed)
