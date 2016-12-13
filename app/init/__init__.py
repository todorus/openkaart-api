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
    return user.find(graph, {"uuid": uuid})
