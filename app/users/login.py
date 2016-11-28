import lib.model.user as user
import lib.db.setup as db


def execute(data):
    if data is None:
        return None

    graph = db.init_graph("local")
    username = data["username"]
    password = data["password"]
    return user.login(graph, username, password)
