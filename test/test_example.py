import allure
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def api_context():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        api_context = context.request
        yield api_context
        browser.close()


@allure.feature("API Tests")
@allure.story("GET /posts/1")
@allure.title("Verify GET /posts/1 returns correct data")
def test_get_example(api_context):
    with allure.step("Send GET request to /posts/1"):
        response = api_context.get("https://jsonplaceholder.typicode.com/posts/1")
        assert response.status == 200, f"Expected 200, got {response.status}"

    with allure.step("Parse and validate response JSON"):
        json_data = response.json()
        allure.attach(str(json_data), name="Response JSON", attachment_type=allure.attachment_type.JSON)
        assert json_data["id"] == 1, "Expected 'id' to be 1"
        assert json_data["userId"] == 1, "Expected 'userId' to be 1"