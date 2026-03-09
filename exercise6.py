import os

verificare = os.path.exists("servers.txt")

if verificare:
    with open("servers.txt", "r") as file:
        for line in file:
            line = line.strip()
            print(f"Verificare: {line}")
else:
    print("Fisierul nu exista!")