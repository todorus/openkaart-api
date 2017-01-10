import lib.model.user as user
import lib.db.setup as db
import lib.jwt as jwt

def execute(token):
    if token is None:
        return None

    graph = db.init_graph("local")
    data = jwt.decode(token)

    return user.find(graph, {"uuid": data["sub"]})
