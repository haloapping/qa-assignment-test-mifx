import os

import allure
import httpx
from dotenv import load_dotenv

load_dotenv()
BASE_URL = "https://reqres.in/api/users?page=2"


def test_get_users_with_header():
    with allure.step("Hit endpoint"):
        x_api_key = os.getenv("X_API_KEY")
        resp = httpx.get(
            url=BASE_URL,
            headers={"x-api-key": x_api_key},
        )

    with allure.step("Check header response"):
        assert resp.status_code == 200
        assert resp.headers["content-type"] == "application/json; charset=utf-8"

    with allure.step("Check body response"):
        data = resp.json()
        assert data["page"] == 2
        assert data["per_page"] == 6
        assert data["total"] == 12
        assert data["total_pages"] == 2
        assert len(data["data"]) == data["per_page"]
        assert "id" in data["data"][0]
        assert "email" in data["data"][0]
        assert "first_name" in data["data"][0]
        assert "last_name" in data["data"][0]
        assert "avatar" in data["data"][0]
        assert data["support"] == {
            "url": "https://contentcaddy.io?utm_source=reqres&utm_medium=json&utm_campaign=referral",
            "text": "Tired of writing endless social media content? Let Content Caddy generate it for you.",
        }
        assert data["_meta"] == {
            "powered_by": "ReqRes",
            "docs_url": "https://app.reqres.in/documentation",
            "upgrade_url": "https://app.reqres.in/upgrade",
            "example_url": "https://app.reqres.in/examples/notes-app",
            "variant": "v1_b",
            "message": "Need more than fake data? Projects give you real CRUD + auth in minutes.",
            "cta": {"label": "Get started", "url": "https://app.reqres.in/upgrade"},
            "context": "legacy_success",
        }


def test_get_users_without_header():
    with allure.step("Hit endpoint"):
        resp = httpx.get(
            url=BASE_URL,
        )

    with allure.step("Check header and body response"):
        assert resp.status_code == 403
        assert resp.headers["content-type"] == "text/html; charset=UTF-8"
        assert "Just a moment..." in resp.text
        assert "Enable JavaScript and cookies to continue" in resp.text
