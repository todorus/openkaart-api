from flask import Flask, jsonify, request, abort, g
from lib.authorization import login_required, user_for_token, current_user
import lib.model.user as user
import lib.db.setup as db
import lib.jwt as jwt

api = Flask("openkaart")


@api.before_request
def check_token():
    result = None
    if 'Authorization' in request.headers:
        authorization = request.headers['Authorization'].encode('ascii', 'ignore')
        token = str.replace(str(authorization), 'Bearer ', '')
        result = user_for_token(token)

    g.user = result


@api.after_request
def refresh_token(response):
    if g.user is not None:
        token_data = {
            "sub": current_user().uuid
        }
        token = jwt.encode(token_data)
        response.headers["JWT"] = token

    return response


@api.errorhandler(401)
def custom_401(error):
    return('', 401)
