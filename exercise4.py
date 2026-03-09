servers = [
    {"name": "nginx", "status": "running"},
    {"name": "mysql", "status": "stopped"},
    {"name": "docker", "status": "running"},
]

for server in servers:
    try:
        server["port"]
    except KeyError:
        print(f"{server['name']} does not have a port")