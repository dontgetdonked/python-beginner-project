services = [
    ("nginx", "running"),
    ("mysql", "stopped"),
    ("docker", "running"),
    ("redis", "stopped")
]

for name, status in services:
    if status == 'running':
        print(f"The {name} service is running!")
    else:
        print(f"The {name} service is stopped!")