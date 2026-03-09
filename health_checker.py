
def check_service(status):
    if status == "running":
        return 'Server is running'
    else:
        return "Server is down"

try:
    with open("servers.txt", "r") as file:
        with open("report.txt", "w") as report:
            for line in file:
                name, status = line.strip().split(",")
                result = check_service(status)
                print(f"Server: {name} | Status: {result}")
                report.write(f"Server: {name} | Status: {result}\n")
except FileNotFoundError:
    print("File not found")
