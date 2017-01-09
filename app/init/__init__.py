from flask import Flask, jsonify, request, abort
from lib.authorization import login_required
import lib.model.user as user
import lib.db.setup as db

api = Flask("openkaart")

@api.errorhandler(401)
def custom_401(error):
    return('', 401)
