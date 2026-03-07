import csv
import os

FILE_PATH = "data/users.csv"

def read_users():
    users = []
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                users.append(row)
    return users


def save_user(username, password):
    users = read_users()
    new_id = len(users) + 1

    with open(FILE_PATH, mode="a", newline="") as file:
        writer = csv.writer(file)

        if os.stat(FILE_PATH).st_size == 0:
            writer.writerow(["id", "username", "password"])

        writer.writerow([new_id, username, password])

def find_user(username):
    users = read_users()

    for user in users:
        if user["username"] == username:
            return user

    return None