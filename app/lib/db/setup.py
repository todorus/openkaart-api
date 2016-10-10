import app.lib.db.config as config
from py2neo import Graph

# example config
# "test": {
#   "secure" : False,
#   "host": "localhost",
#   "http_port": 7474,
#   "https_port": 7474,
#
#   "user" : "user",
#   "password" : "pass"
# }


def init_graph(environment):
    used_config = config.db_configs[environment]
    graph = Graph(**used_config)
    return graph
