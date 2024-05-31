from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(key_func=get_remote_address, storage_uri="memory://") # key_func indicates what type of method we will perform to limit. in this case, by IP Address
