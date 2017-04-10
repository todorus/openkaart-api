from init import api
from flask import jsonify, request
from lib.authorization import login_required
import json

@api.route("/organizations", methods=["POST"])
def organizations():
    return organizations_create()

@login_required
def organizations_create():
    from organizations.create import execute

    # extract parameters
    params = request.get_json()

    result = execute(params.get("name"), params.get("contact_data"))

    # present result as json
    if result is None:
        return ('', 400)
    return jsonify(**result)
