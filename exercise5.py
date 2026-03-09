with open("servers.txt", "w") as f:
    f.write("nginx\nmysql\ndocker")

for line in open("servers.txt"):
    line = line.strip()
    print(f"Server: {line}")
