import app.lib.db.config as config
from py2neo import Graph

# example config. Note the hostname should be the same as the database
# containers name in the docker-compose.yaml
# "test": {
#   "secure" : False,
#   "host": "database",
#   "http_port": 7474,
#   "https_port": 7474,
#
#   "user" : "user",
#   "password" : "pass"
# }


def init_graph(environment):
    print "starting db %s" % (environment)
    used_config = config.db_configs[environment]
    graph = Graph(**used_config)
    return graph
