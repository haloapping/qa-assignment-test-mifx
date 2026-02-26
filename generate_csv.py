import csv
import os

import httpx
from dotenv import load_dotenv

load_dotenv()
BASE_URL = "https://reqres.in/api/users?page=2"


def generate_csv(filename: str = "output"):
    x_api_key = os.getenv("X_API_KEY")
    resp = httpx.get(
        url=BASE_URL,
        headers={"x-api-key": x_api_key},
    )

    data = resp.json()["data"]
    columns = {
        "first_name": "First Name",
        "last_name": "Last Name",
        "email": "Email",
    }

    with open(f"{filename}.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(columns.values())
        for row in data:
            writer.writerow([row.get(key, "") for key in columns.keys()])


generate_csv()
