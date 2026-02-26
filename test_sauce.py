import os
import tkinter as tk

import allure
from playwright.sync_api import Browser, expect

SCREEN_WIDTH = tk.Tk().winfo_screenwidth() if os.getenv("DISPLAY") is not None else 1920
SCREEN_HEIGHT = (
    tk.Tk().winfo_screenheight() if os.getenv("DISPLAY") is not None else 1080
)
BASE_URL = "https://www.saucedemo.com/"


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
        record_video_dir="videos/",
        record_video_size={"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT},
    )
    page = context.new_page()

    with allure.step("Open link https://www.saucedemo.com/"):
        page.goto(BASE_URL)

    for username in usernames:
        with allure.step(f"Login with username: {username}"):
            with allure.step("Verify username field"):
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

    context.close()
    os.rename(page.video.path(), "videos/tc001_user_login_correct.webm")


@allure.id("TC002")
@allure.severity("HIGH")
@allure.label("positive case")
@allure.feature("Humbergur Menu")
@allure.title("All link on humbergur menu is valid")
@allure.description("Check all list menu")
def test_humbergur_menu(browser: Browser):
    with allure.step("Login"):
        context, page = login(browser)

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

    video_path = page.video.path()
    context.close()
    os.rename(video_path, "videos/tc002_menu.webm")


@allure.id("TC003")
@allure.severity("HIGH")
@allure.label("positive case")
@allure.feature("Menu")
@allure.title("Reset App State")
@allure.description("Add some items to cart and reload page")
def test_reset_app_state_menu(browser: Browser):
    with allure.step("Login"):
        context, page = login(browser)

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

    video_path = page.video.path()
    context.close()
    os.rename(video_path, "videos/tc003_reset_app_state.webm")


# ERROR! number of badge not equal
@allure.id("TC004")
@allure.severity("HIGH")
@allure.label("positive case")
@allure.feature("Cart")
@allure.title("Add to cart")
@allure.description("Add some items to cart and validate number of item")
def test_add_to_cart_icon(browser: Browser):
    with allure.step("Login"):
        context, page = login(browser)

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

    # remove all item from cart
    for i in range(len(selectors) - 1, -1, -1):
        with allure.step(f"Remove item {i} from cart"):
            before_add_cart_first_item = page.screenshot(full_page=True)
            allure.attach(
                before_add_cart_first_item,
                name=f"Remove item {i} from cart",
                attachment_type=allure.attachment_type.PNG,
            )

            page.locator(selectors[i][1]).click()

            if i != 0:
                expect(page.locator("[data-test='shopping-cart-badge']")).to_have_text(
                    str(i)
                )

            after_remove_first_item = page.screenshot(full_page=True)
            allure.attach(
                after_remove_first_item,
                name=f"Remove item {i} from cart",
                attachment_type=allure.attachment_type.PNG,
            )

    video_path = page.video.path()
    context.close()
    os.rename(video_path, "videos/tc004_add_to_cart.webm")


@allure.id("TC005")
@allure.severity("HIGH")
@allure.label("positive case")
@allure.feature("Checkout")
@allure.title("Checkout item")
@allure.description("Add some items to cart and checkout")
def test_checkout(browser: Browser):
    with allure.step("Login"):
        context, page = login(browser)

    with allure.step("Add item to cart"):
        item_name = (
            page.locator("[data-test='inventory-item-name']").nth(0).inner_text()
        )
        item_desc = (
            page.locator("[data-test='inventory-item-desc']").nth(0).inner_text()
        )
        item_price = (
            page.locator("[data-test='inventory-item-price']").nth(0).inner_text()
        )

        expect(page.locator("#add-to-cart-sauce-labs-backpack")).to_have_text(
            "Add to cart"
        )
        page.locator("#add-to-cart-sauce-labs-backpack").click()
        expect(page.locator("#remove-sauce-labs-backpack")).to_have_text("Remove")
        expect(page.locator("[data-test='shopping-cart-badge']")).to_have_text("1")

    with allure.step("Click Cart Menu"):
        page.locator("[data-test='shopping-cart-link']").click()
        expect(page.locator("[data-test='inventory-item-name']").nth(0)).to_have_text(
            item_name
        )
        expect(page.locator("[data-test='inventory-item-desc']").nth(0)).to_have_text(
            item_desc
        )
        expect(page.locator("[data-test='inventory-item-price']").nth(0)).to_have_text(
            item_price
        )

    with allure.step("Checkout item"):
        page.locator("#checkout").click()

        page.locator("#first-name").fill("Budiono")
        page.locator("#last-name").fill("Siregar")
        page.locator("#postal-code").fill("12890")

        page.locator("#continue").click()

    with allure.step("Finish checkout"):
        page.locator("#finish").click()

    with allure.step("Checkout complete"):
        expect(page.locator("[data-test='complete-header']")).to_have_text(
            "Thank you for your order!"
        )

    video_path = page.video.path()
    context.close()
    os.rename(video_path, "videos/tc005_checkout.webm")


@allure.id("TC006")
@allure.severity("HIGH")
@allure.label("negative case")
@allure.feature("Wrong password")
@allure.title("Login with wrong password")
@allure.description("Use wrong password when login")
def test_login_wrong_password(browser: Browser):
    context = browser.new_context(
        viewport={"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT},
        record_video_dir="videos/",
        record_video_size={"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT},
    )
    page = context.new_page()
    page.goto(BASE_URL)

    with allure.step("Verify username field"):
        page.locator("#user-name").fill("standard_user")

    with allure.step("Verify password field"):
        page.locator("#password").fill("wr0ngP4ssword!")

    before_click_login_btn_img = page.screenshot(full_page=True)
    allure.attach(
        before_click_login_btn_img,
        name="Before click login button",
        attachment_type=allure.attachment_type.PNG,
    )

    with allure.step("Verify login button"):
        page.locator("#login-button").click()

    with allure.step("Verify error message"):
        expect(page.locator("[data-test='error']")).to_have_text(
            "Epic sadface: Username and password do not match any user in this service"
        )

    after_click_login_btn_img = page.screenshot(full_page=True)
    allure.attach(
        after_click_login_btn_img,
        name="After click login button",
        attachment_type=allure.attachment_type.PNG,
    )

    video_path = page.video.path()
    context.close()
    os.rename(video_path, "videos/tc006_login_wrong_password.webm")


@allure.id("TC007")
@allure.severity("HIGH")
@allure.label("negative case")
@allure.feature("SQL Injection")
@allure.title("Login with password using sql injection")
@allure.description("Use sql injection when login")
def test_login_sql_injection(browser: Browser):
    context = browser.new_context(
        viewport={"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT},
        record_video_dir="videos/",
        record_video_size={"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT},
    )
    page = context.new_page()
    page.goto(BASE_URL)

    with allure.step("Verify username field"):
        page.locator("#user-name").fill("standard_user")

    with allure.step("Verify password field"):
        page.locator("#password").fill("' OR 1=1--")

    before_click_login_btn_img = page.screenshot(full_page=True)
    allure.attach(
        before_click_login_btn_img,
        name="Before click login button",
        attachment_type=allure.attachment_type.PNG,
    )

    with allure.step("Verify login button"):
        page.locator("#login-button").click()

    with allure.step("Verify error message"):
        expect(page.locator("[data-test='error']")).to_have_text(
            "Epic sadface: Username and password do not match any user in this service"
        )

    after_click_login_btn_img = page.screenshot(full_page=True)
    allure.attach(
        after_click_login_btn_img,
        name="After click login button",
        attachment_type=allure.attachment_type.PNG,
    )

    video_path = page.video.path()
    context.close()
    os.rename(video_path, "videos/tc007_login_sql_injection.webm")


@allure.id("TC008")
@allure.severity("HIGH")
@allure.label("negative case")
@allure.feature("Login")
@allure.title("Login with password using XSS Attempt")
@allure.description("Use XSS Attempt when login")
def test_login_xss_attempt(browser: Browser):
    context = browser.new_context(
        viewport={"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT},
        record_video_dir="videos/",
        record_video_size={"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT},
    )
    page = context.new_page()
    page.goto(BASE_URL)

    with allure.step("Verify username field"):
        page.locator("#user-name").fill("<script>alert(1)</script>")

    with allure.step("Verify password field"):
        page.locator("#password").fill("<script>alert(1)</script>")

    before_click_login_btn_img = page.screenshot(full_page=True)
    allure.attach(
        before_click_login_btn_img,
        name="Before click login button",
        attachment_type=allure.attachment_type.PNG,
    )

    with allure.step("Verify login button"):
        page.locator("#login-button").click()

    with allure.step("Verify error message"):
        expect(page.locator("[data-test='error']")).to_have_text(
            "Epic sadface: Username and password do not match any user in this service"
        )

    after_click_login_btn_img = page.screenshot(full_page=True)
    allure.attach(
        after_click_login_btn_img,
        name="After click login button",
        attachment_type=allure.attachment_type.PNG,
    )

    video_path = page.video.path()
    context.close()
    os.rename(video_path, "videos/tc008_login_xss_attempt.webm")


@allure.id("TC009")
@allure.severity("HIGH")
@allure.label("negative case")
@allure.feature("Login")
@allure.title("Login with username or password empty")
@allure.description("Use username or password empty ")
def test_login_empty_field(browser: Browser):
    context = browser.new_context(
        viewport={"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT},
        record_video_dir="videos/",
        record_video_size={"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT},
    )
    page = context.new_page()
    page.goto(BASE_URL)

    credentials = [
        {"username": "", "password": ""},
        {"username": "standard_user", "password": ""},
        {"username": "", "password": "secret_sauce"},
    ]

    for i, credential in enumerate(credentials):
        with allure.step("Verify username field"):
            page.locator("#user-name").fill(credential["username"])

        with allure.step("Verify password field"):
            page.locator("#password").fill(credential["password"])

        before_click_login_btn_img = page.screenshot(full_page=True)
        allure.attach(
            before_click_login_btn_img,
            name="Before click login button",
            attachment_type=allure.attachment_type.PNG,
        )

        with allure.step("Verify login button"):
            page.locator("#login-button").click()

        if i == 0 or i == 2:
            with allure.step("Verify error message"):
                expect(page.locator("[data-test='error']")).to_have_text(
                    "Epic sadface: Username is required"
                )
        else:
            with allure.step("Verify error message"):
                expect(page.locator("[data-test='error']")).to_have_text(
                    "Epic sadface: Password is required"
                )

        after_click_login_btn_img = page.screenshot(full_page=True)
        allure.attach(
            after_click_login_btn_img,
            name="After click login button",
            attachment_type=allure.attachment_type.PNG,
        )

        page.reload()

    video_path = page.video.path()
    context.close()
    os.rename(video_path, "videos/tc009_login_user_password_empty.webm")


@allure.id("TC010")
@allure.severity("HIGH")
@allure.label("negative case")
@allure.feature("Inventory Menu")
@allure.title("Access inventory page after logout")
@allure.description("")
def test_inventory_page(browser: Browser):
    with allure.step("Login"):
        context, page = login(browser)

    with allure.step("Click humbergur button and logout menu"):
        page.locator("#react-burger-menu-btn").click()
        page.get_by_text("Logout").click()

    page.goto("https://www.saucedemo.com/inventory.html")

    with allure.step("Verify error message"):
        expect(page.locator("[data-test='error']")).to_have_text(
            "Epic sadface: You can only access '/inventory.html' when you are logged in."
        )

    video_path = page.video.path()
    context.close()
    os.rename(video_path, "videos/tc010_access_inventory_page_after_logout.webm")


@allure.issue("BUG-123", "The number of cart items is the same for all users.")
@allure.id("TC011")
@allure.severity("HIGH")
@allure.label("positive case")
@allure.feature("Inventory Menu")
@allure.title("Access inventory page after logout")
@allure.description(
    "Add item cart using standard user and logout. Login again with another user and check state is reset or not."
)
def test_add_cart_other_user(browser: Browser):
    context = browser.new_context(
        viewport={"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT},
        record_video_dir="videos/",
        record_video_size={"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT},
    )
    page = context.new_page()
    page.goto(BASE_URL)

    with allure.step("Login with username: standard_user"):
        with allure.step("Verify username field"):
            page.locator("#user-name").fill("standard_user")

        with allure.step("Verify password field"):
            page.locator("#password").fill("secret_sauce")

        with allure.step("Verify login button"):
            page.locator("#login-button").click()

        with allure.step("Add 2 items to cart"):
            page.locator("#add-to-cart-sauce-labs-backpack").click()
            page.locator("#add-to-cart-sauce-labs-bike-light").click()

        standard_user = page.screenshot(full_page=True)
        allure.attach(
            standard_user,
            name="Homepage standard user",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Logout"):
        page.locator("#react-burger-menu-btn").click()
        page.get_by_text("Logout").click()

    with allure.step("Login with username: visual_user"):
        with allure.step("Verify username field"):
            page.locator("#user-name").fill("visual_user")

        with allure.step("Verify password field"):
            page.locator("#password").fill("secret_sauce")

        with allure.step("Verify login button"):
            page.locator("#login-button").click()

        visual_user = page.screenshot(full_page=True)
        allure.attach(
            visual_user,
            name="Homepage visual user",
            attachment_type=allure.attachment_type.PNG,
        )

        with allure.step("Verify state is reset"):
            expect(page.locator("#remove-sauce-labs-backpack")).not_to_be_visible()
            expect(page.locator("#remove-sauce-labs-bike-light")).not_to_be_visible()

    video_path = page.video.path()
    context.close()
    os.rename(video_path, "videos/tc011_cart_items_is_the_same_for_all_users.webm")


def login(browser: Browser):
    context = browser.new_context(
        viewport={"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT},
        record_video_dir="videos/",
        record_video_size={"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT},
    )
    page = context.new_page()
    page.goto(BASE_URL)
    with allure.step("Verify username field"):
        page.locator("#user-name").fill("standard_user")

    with allure.step("Verify password field"):
        page.locator("#password").fill("secret_sauce")

    with allure.step("Verify login button"):
        page.locator("#login-button").click()

    return context, page
