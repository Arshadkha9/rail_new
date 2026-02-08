from slowapi import Limiter
from slowapi.util import get_remote_address

# Har IP ke liye request count karega
limiter = Limiter(key_func=get_remote_address)