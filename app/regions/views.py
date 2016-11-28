from init import api
from flask import jsonify, request

@api.route("/regions/<uuid>", methods=["GET"])
def regions_read(uuid):
    from regions.read import execute

    # execute
    result = execute(uuid)
    if result is None:
        return('', 404)

    # present result as json
    return jsonify(**result)


@api.route("/regions", methods=["GET"])
def regions_index():
    from regions.index import execute

    # extract parameters
    params = request.args.to_dict()

    # execute
    result = execute(params)

    # present result as json
    return jsonify(**result)
