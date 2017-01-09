from functools import wraps
from flask import g, request, abort
import lib.model.user as user
import lib.db.setup as db
import lib.jwt as jwt

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if not 'Authorization' in request.headers:
            abort(401)

        authorization = request.headers['Authorization'].encode('ascii', 'ignore')
        token = str.replace(str(authorization), 'Bearer ', '')

        graph = db.init_graph("local")

        user = user_for_token(token)
        if user is None:
            abort(401)

        g.user = user

        return f(*args, **kws)
    return decorated_function

def current_user():
    return g.user

def user_for_token(token):
    if token is None:
        return None

    try:
        data = jwt.decode(token)
    except:
        return None

    graph = db.init_graph("local")
    return user.find(graph, {"uuid": data["sub"]})
