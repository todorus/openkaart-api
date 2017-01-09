from flask import Flask, jsonify, request, abort
import lib.model.user as user
import lib.db.setup as db

api = Flask("openkaart")
api.secret_key = "development"

@api.errorhandler(401)
def custom_401(error):
    return('', 401)
