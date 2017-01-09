from jose import jwt
import time

valid_period = 15 * 60 #15 minutes
algorithm = 'HS256'
secret_key = "development"


def encode(data):
    now = time.time()
    payload = {
        "iat": now,
        "exp": now + valid_period,
        "data": data
    }
    return jwt.encode(payload, secret_key, algorithm=algorithm)


def decode(token):
    options = {
        'verify_sub': False
    }
    decoded = jwt.decode(token, secret_key, algorithms=algorithm, options=options)

    return decoded["data"]
