from flask import Flask
app = Flask("regions")

@app.route("/fetch")
def hello():
    return "Hello World!"

app.run()
