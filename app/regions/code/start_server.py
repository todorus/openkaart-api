from flask import Flask, jsonify
api = Flask("regions")


@api.route('/')
def hello_root():
    return 'Hello World!'

@api.route('/root')
def project_root():
    return __name__

@api.route("/fetch")
def hello_fetch():
    from app.index import execute

    result = execute({})
    return jsonify(**result)


api.run(host="0.0.0.0", debug=True)
