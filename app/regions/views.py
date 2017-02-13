from init import api
from flask import jsonify, request
from lib.authorization import login_required

@api.route("/regions/<uuid>", methods=["GET", "DELETE"])
def region(uuid):
    if request.method == 'GET':
        return regions_read(uuid)
    elif request.method == 'DELETE':
        return regions_destroy(uuid)
    else:
        return '', 401


@api.route("/regions", methods=["GET", "POST"])
def regions():
    if request.method == 'GET':
        return regions_index()
    elif request.method == 'POST':
        return regions_create()
    else:
        return '', 401


def regions_read(uuid):
    from regions.read import execute

    # execute
    result = execute(uuid)
    if result is None:
        return ('', 404)

    # present result as json
    return jsonify(**result)


def regions_index():
    from regions.index import execute

    # extract parameters
    params = request.args.to_dict()

    # execute
    result = execute(params)

    # present result as json
    return jsonify(**result)


@login_required
def regions_create():
    from regions.create import execute

    # extract parameters
    params = request.get_json()

    # execute
    # api.logger.info('''
    #     "name": %s,
    #     "type": %s,
    #     "children": %s ''' % (params.get("name"), params.get("type"), params.get("children")))
    result = execute(params.get("name"), params.get("type"), params.get("children"))

    # present result as json
    if result is None:
        return ('', 400)
    return jsonify(**result)


@login_required
def regions_destroy(uuid):
    from regions.destroy import execute

    # extract parameters
    result = execute({"uuid": uuid})

    # present result as json
    if result is None:
        return ('', 404)
    return ('', 200)
