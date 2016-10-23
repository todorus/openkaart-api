def init_graph(environment="local"):
    from py2neo import Graph

    used_config = {
        "secure": False,
        "host": "database",
        "http_port": 7474,
        "https_port": 7474
    }
    graph = Graph(**used_config)

    return graph
