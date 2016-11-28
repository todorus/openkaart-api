from init import api
from flask import jsonify, request

@api.route("/login", methods=["POST"])
def login():
    from users.login import execute

    # extract body
    body = request.get_json(force=True)

    # execute
    result = execute(body)

    if result is None:
        return('', 401)

    # present result as json
    return jsonify(**result)
