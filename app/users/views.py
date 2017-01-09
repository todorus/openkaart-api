from init import api
from flask import jsonify, request
from lib.authorization import login_required, current_user

@api.route("/users/login", methods=["POST"])
def login():
    from users.login import execute
    import lib.jwt as jwt

    # extract body
    body = request.get_json(force=True)

    # execute
    result = execute(body)

    if result is None:
        return('', 401)

    token_data = {
        "sub": result.uuid
    }
    token = jwt.encode(token_data)

    # present result as json
    user = {"username": result.username}
    response = jsonify({"user": user})
    response.headers["JWT"] = token
    return response


@api.route("/users/me", methods=["GET"])
@login_required
def me():
    from users.me import execute

    result = current_user()

    if result is None:
        return('', 401)

    # present result as json
    return jsonify({"username": result.username})
