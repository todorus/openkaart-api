from init import api
from flask import jsonify, request

@api.route("/login", methods=["POST"])
def login():
    from authentication.login import execute

    # extract parameters
    params = request.args.to_dict()

    # execute
    result = execute(params)

    if result is None:
        return('', 401)

    # present result as json
    return jsonify(**result)
