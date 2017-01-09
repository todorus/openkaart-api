from jose import jwt
from init import api
import time

valid_period = 15 * 60 #15 minutes

def encode(data):
    now = time.time()
    payload = {
        "iat": now,
        "exp": now + valid_period,
        "data": data
    }
    return jwt.encode(payload, api.secret_key, algorithm='HS256')
