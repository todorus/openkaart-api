def init_graph(environment):
    import app.lib.db.config as config
    from py2neo import Graph

    used_config = config.db_configs[environment]
    graph = Graph(**used_config)
    return graph
