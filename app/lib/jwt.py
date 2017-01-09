from jose import jwt
from init import api
import time

valid_period = 15 * 60 #15 minutes
algorithm = 'HS256'


def encode(data):
    now = time.time()
    payload = {
        "iat": now,
        "exp": now + valid_period,
        "data": data
    }
    return jwt.encode(payload, api.secret_key, algorithm='HS256')


def decode(token):
    options = {
        'verify_sub': False
    }
    decoded = jwt.decode(token, api.secret_key, algorithms=algorithm, options=options)

    return decoded["data"]
