from init import api
from flask import jsonify, request
from flask_login import login_required, login_user, current_user

@api.route("/login", methods=["POST"])
def login():
    from users.login import execute

    # extract body
    body = request.get_json(force=True)

    # execute
    result = execute(body)

    if result is None:
        return('', 401)

    # return jsonify({"username": result.username})

    login_user(result)
    # result = current_user()

    # present result as json
    return jsonify({"username": result.username})


@api.route("/me", methods=["GET"])
@login_required
def current_user():
    result = current_user

    # present result as json
    return jsonify({"username": result.username})
