import csv
import os

class CsvUserRepository:

    FILE = "users.csv"

    FIELDNAMES = [
        "nombre",
        "cedula",
        "username",
        "password",
        "provider",
        "provider_id"
    ]

    def read_all(self):

        if not os.path.exists(self.FILE):
            return []

        with open(self.FILE, newline="", encoding="utf-8") as file:
            return list(csv.DictReader(file))

    def find_by_username(self, username: str):

        for user in self.read_all():

            if user.get("username", "").lower() == username.lower():
                return user

        return None

    def find_by_provider(self, provider: str, provider_id: str):

        for user in self.read_all():

            if (
                user.get("provider") == provider
                and user.get("provider_id") == provider_id
            ):
                return user

        return None

    def save(self, user: dict):

        file_exists = os.path.exists(self.FILE)

        with open(self.FILE, "a", newline="", encoding="utf-8") as file:

            writer = csv.DictWriter(
                file,
                fieldnames=self.FIELDNAMES
            )

            if not file_exists or os.stat(self.FILE).st_size == 0:
                writer.writeheader()

            writer.writerow(user)