from flask import Flask, jsonify, request, abort
api = Flask("openkaart")

@api.route("/regions/<uuid>")
def regions_read(uuid):
    from regions.read import execute

    # execute
    result = execute(uuid)
    if result is None:
        return('', 404)

    # present result as json
    return jsonify(**result)

@api.route("/regions")
def regions_index():
    from regions.index import execute

    # extract parameters
    params = request.args.to_dict()

    # execute
    result = execute(params)

    # present result as json
    return jsonify(**result)


api.run(host="0.0.0.0", debug=True)