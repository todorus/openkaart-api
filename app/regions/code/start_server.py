from flask import Flask
app = Flask("regions")


@app.route('/')
def hello_root():
    return 'Hello World!'


@app.route("/fetch")
def hello_fetch():
    return "Hello Fetch old!"


@app.route("/regions/fetch")
def hello_fetch_new():
    return "Hello Fetch!"

app.run(host="0.0.0.0", debug=True)
