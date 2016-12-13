from flask import Flask, jsonify, request, abort
from flask_login import LoginManager
import lib.model.user as user
import lib.db.setup as db

api = Flask("openkaart")
login_manager = LoginManager(api)
api.secret_key = "development"


@login_manager.user_loader
def loadUser(uuid):
    graph = db.init_graph("local")
    result = user.find(graph, {"uuid": uuid})
    result.is_authenticated = True
    return result


@api.errorhandler(401)
def custom_401(error):
    return('', 401)
