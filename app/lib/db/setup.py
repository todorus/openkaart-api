def init_graph(environment="local"):
    from py2neo import Graph
    from py2neo import watch

    used_config = {
        "secure": False,
        "host": "database",
        "http_port": 7474,
        "https_port": 7474
    }
    graph = Graph(**used_config)
    # watch("neo4j.bolt")
    # watch("neo4j.http")

    return graph
