import os
import tkinter as tk

import allure
from playwright.sync_api import Browser, Page, expect

SCREEN_WIDTH = tk.Tk().winfo_screenwidth() if os.getenv("DISPLAY") is not None else 1920
SCREEN_HEIGHT = (
    tk.Tk().winfo_screenheight() if os.getenv("DISPLAY") is not None else 1080
)
BASE_URL = "https://www.saucedemo.com/"


def login(browser: Browser) -> Page:
    context = browser.new_context(
        viewport={"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT},
    )
    page = context.new_page()
    page.goto(BASE_URL)
    with allure.step("Verify email field"):
        page.locator("#user-name").fill("standard_user")

    with allure.step("Verify password field"):
        page.locator("#password").fill("secret_sauce")

    with allure.step("Verify login button"):
        page.locator("#login-button").click()

    return page


@allure.id("TC001")
@allure.severity("HIGH")
@allure.label("positive case")
@allure.feature("Login")
@allure.title("Valid login with list username and password")
@allure.description("Check all list username and password")
def test_user_login(browser: Browser):
    usernames = [
        "standard_user",
        "locked_out_user",
        "problem_user",
        "performance_glitch_user",
        "error_user",
        "visual_user",
    ]

    context = browser.new_context(
        viewport={"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT},
    )
    page = context.new_page()

    with allure.step("Open link https://www.saucedemo.com/"):
        page.goto(BASE_URL)

    for username in usernames:
        with allure.step(f"Login with username: {username}"):
            with allure.step("Verify email field"):
                page.locator("#user-name").fill(username)

            with allure.step("Verify password field"):
                page.locator("#password").fill("secret_sauce")

            before_click_login_btn_img = page.screenshot(full_page=True)
            allure.attach(
                before_click_login_btn_img,
                name="Before click login button",
                attachment_type=allure.attachment_type.PNG,
            )

            with allure.step("Verify login button"):
                page.locator("#login-button").click()

            if username in [
                "standard_user",
                "problem_user",
                "performance_glitch_user",
                "error_user",
                "visual_user",
            ]:
                page.wait_for_url("https://www.saucedemo.com/inventory.html")
                expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

                after_click_login_btn_img = page.screenshot(full_page=True)
                allure.attach(
                    after_click_login_btn_img,
                    name="After click login button",
                    attachment_type=allure.attachment_type.PNG,
                )

                page.locator("#react-burger-menu-btn").click()
                page.get_by_text("Logout").click()
            else:
                expect(page.locator("[data-test='error']")).to_have_text(
                    "Epic sadface: Sorry, this user has been locked out."
                )

                after_click_login_btn_img = page.screenshot(full_page=True)
                allure.attach(
                    after_click_login_btn_img,
                    name="After click login button",
                    attachment_type=allure.attachment_type.PNG,
                )

            page.reload()


@allure.id("TC002")
@allure.severity("HIGH")
@allure.label("positive case")
@allure.feature("Humbergur Menu")
@allure.title("All link on humbergur menu is valid")
@allure.description("Check all list menu")
def test_humbergur_menu(browser: Browser):
    with allure.step("Login"):
        page = login(browser)

    with allure.step("Click humbergur button"):
        page.locator("#react-burger-menu-btn").click()

    with allure.step("Verify text and link All Items menu"):
        expect(page.locator("#inventory_sidebar_link")).to_be_visible()
        expect(page.locator("#inventory_sidebar_link")).to_be_enabled()
        expect(page.locator("#inventory_sidebar_link")).to_have_attribute("href", "#")
        expect(page.locator("#inventory_sidebar_link")).to_have_text("All Items")

    with allure.step("Verify text and link About menu"):
        expect(page.locator("#about_sidebar_link")).to_be_visible()
        expect(page.locator("#about_sidebar_link")).to_be_enabled()
        expect(page.locator("#about_sidebar_link")).to_have_attribute(
            "href", "https://saucelabs.com/"
        )
        expect(page.locator("#about_sidebar_link")).to_have_text("About")

    with allure.step("Verify text and link Logout menu"):
        expect(page.locator("#logout_sidebar_link")).to_be_visible()
        expect(page.locator("#logout_sidebar_link")).to_be_enabled()
        expect(page.locator("#logout_sidebar_link")).to_have_attribute("href", "#")
        expect(page.locator("#logout_sidebar_link")).to_have_text("Logout")

    with allure.step("Verify text and link Reset App State menu"):
        expect(page.locator("#reset_sidebar_link")).to_be_visible()
        expect(page.locator("#reset_sidebar_link")).to_be_enabled()
        expect(page.locator("#reset_sidebar_link")).to_have_attribute("href", "#")
        expect(page.locator("#reset_sidebar_link")).to_have_text("Reset App State")

    img = page.screenshot(full_page=True)
    allure.attach(
        img,
        name="Menu",
        attachment_type=allure.attachment_type.PNG,
    )


@allure.id("TC003")
@allure.severity("HIGH")
@allure.label("positive case")
@allure.feature("Menu")
@allure.title("Reset App State")
@allure.description("Add some items to cart and reload page")
def test_reset_app_state_menu(browser: Browser):
    with allure.step("Login"):
        page = login(browser)

    with allure.step("Before reset app state"):
        with allure.step("Add to cart first item"):
            expect(page.locator("#add-to-cart-sauce-labs-backpack")).to_have_text(
                "Add to cart"
            )
            page.locator("#add-to-cart-sauce-labs-backpack").click()
            expect(page.locator("#remove-sauce-labs-backpack")).to_have_text("Remove")

        with allure.step("Add to cart second item"):
            expect(page.locator("#add-to-cart-sauce-labs-bike-light")).to_have_text(
                "Add to cart"
            )
            page.locator("#add-to-cart-sauce-labs-bike-light").click()
            expect(page.locator("#remove-sauce-labs-bike-light")).to_have_text("Remove")

        before_reset = page.screenshot(full_page=True)
        allure.attach(
            before_reset,
            name="Before reset app state",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Reset app state"):
        page.locator("#react-burger-menu-btn").click()
        page.locator("#reset_sidebar_link").click()
        page.reload()

    with allure.step("After reset app state"):
        with allure.step("Add to cart first item"):
            expect(page.locator("#add-to-cart-sauce-labs-backpack")).to_have_text(
                "Add to cart"
            )

        with allure.step("Add to cart second item"):
            expect(page.locator("#add-to-cart-sauce-labs-bike-light")).to_have_text(
                "Add to cart"
            )

        after_reset = page.screenshot(full_page=True)
        allure.attach(
            after_reset,
            name="After reset app state",
            attachment_type=allure.attachment_type.PNG,
        )

# ERROR! number of badge not equal
@allure.id("TC004")
@allure.severity("HIGH")
@allure.label("positive case")
@allure.feature("Cart")
@allure.title("Add to cart")
@allure.description("Add some items to cart and validate number of item")
def test_add_to_cart_icon(browser: Browser):
    with allure.step("Login"):
        page = login(browser)

    selectors = [
        ["#add-to-cart-sauce-labs-backpack", "#remove-sauce-labs-backpack"],
        ["#add-to-cart-sauce-labs-bike-light", "#remove-sauce-labs-bike-light"],
        ["#add-to-cart-sauce-labs-bolt-t-shirt", "#remove-sauce-labs-bolt-t-shirt"],
        ["#add-to-cart-sauce-labs-fleece-jacket", "#remove-sauce-labs-fleece-jacket"],
    ]

    # add some items to cart
    for i, selector in enumerate(selectors):
        with allure.step(f"Add item {i + 1} to cart"):
            before_add_cart_first_item = page.screenshot(full_page=True)
            allure.attach(
                before_add_cart_first_item,
                name="Add to cart first item",
                attachment_type=allure.attachment_type.PNG,
            )

            expect(page.locator(selector[0])).to_have_text("Add to cart")
            page.locator(selector[0]).click()
            expect(page.locator(selector[1])).to_have_text("Remove")
            expect(page.locator("[data-test='shopping-cart-badge']")).to_have_text(
                str(i + 1)
            )

            after_add_first_item = page.screenshot(full_page=True)
            allure.attach(
                after_add_first_item,
                name=f"Add item {i + 1} to cart",
                attachment_type=allure.attachment_type.PNG,
            )

    # remove some item from cart
    for i, selector in enumerate(selectors, 4):
        with allure.step(f"Remove item {i - 3} from cart"):
            before_add_cart_first_item = page.screenshot(full_page=True)
            allure.attach(
                before_add_cart_first_item,
                name=f"Remote item {i} from cart",
                attachment_type=allure.attachment_type.PNG,
            )

            page.locator(selector[1]).click()
            expect(page.locator("[data-test='shopping-cart-badge']")).to_have_text(
                str(i)
            )

            after_remove_first_item = page.screenshot(full_page=True)
            allure.attach(
                after_remove_first_item,
                name=f"Remove item {i - 3} from cart",
                attachment_type=allure.attachment_type.PNG,
            )


@allure.id("TC005")
@allure.severity("HIGH")
@allure.label("positive case")
@allure.feature("Checkout")
@allure.title("Checkout all item")
@allure.description("Add some items to cart and checkout")
def test_checkout(browser: Browser):
    with allure.step("Login"):
        page = login(browser)

    with allure.step("Add item to cart"):
        item_name = page.locator("[data-test='inventory-item-name']").nth(0).inner_text()
        item_desc = page.locator("[data-test='inventory-item-desc']").nth(0).inner_text()
        item_price = page.locator("[data-test='inventory-item-price']").nth(0).inner_text()

        expect(page.locator("#add-to-cart-sauce-labs-backpack")).to_have_text(
            "Add to cart"
        )
        page.locator("#add-to-cart-sauce-labs-backpack").click()
        expect(page.locator("#remove-sauce-labs-backpack")).to_have_text("Remove")
        expect(page.locator("[data-test='shopping-cart-badge']")).to_have_text("1")

    with allure.step("Click Cart Menu"):
        page.locator("[data-test='shopping-cart-link']").click()
        expect(page.locator("[data-test='inventory-item-name']").nth(0)).to_have_text(item_name)
        expect(page.locator("[data-test='inventory-item-desc']").nth(0)).to_have_text(item_desc)
        expect(page.locator("[data-test='inventory-item-price']").nth(0)).to_have_text(item_price)

    with allure.step("Checkout item"):
        page.locator("#checkout").click()

        page.locator("#first-name").fill("Budiono")
        page.locator("#last-name").fill("Siregar")
        page.locator("#postal-code").fill("12890")

        page.locator("#continue").click()

    with allure.step("Finish checkout"):
        page.locator("#finish").click()

    with allure.step("Checkout complete"):
        expect(page.locator("[data-test='complete-header']")).to_have_text("Thank you for your order!")
