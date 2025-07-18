from slowapi import Limiter
from slowapi.util import get_remote_address

# 👇 Use in-memory for now
limiter = Limiter(key_func=get_remote_address)
