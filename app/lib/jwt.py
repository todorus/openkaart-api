from jose import jwt
import time

valid_period = 15 * 60 #15 minutes
algorithm = 'HS256'
secret_key = "development"


def encode(data, iat=None, exp=None):
    if iat is None:
        iat = time.time()
    if exp is None:
        exp = iat + valid_period

    payload = {
        "iat": iat,
        "exp": exp,
        "data": data
    }
    
    return jwt.encode(payload, secret_key, algorithm=algorithm)


def decode(token):
    options = {
        'verify_sub': False
    }
    decoded = jwt.decode(token, secret_key, algorithms=algorithm, options=options)

    return decoded["data"]
