from flask import Flask, jsonify, request
api = Flask("regions")

@api.route('/info')
def project_root():
    return __name__

@api.route("/")
def index():
    from regions.index import execute

    # extract parameters
    params = request.args.to_dict()

    # execute
    result = execute(params)

    # present result as json
    return jsonify(**result)


api.run(host="0.0.0.0", debug=True)
