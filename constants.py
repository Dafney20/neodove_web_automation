
login_credentials = {
    'username': '9876543211',
    'password': '12345'
}

LOGIN_URL = "https://connect.neodove.com/login"
HOME_URL = "https://connect.neodove.com/home"

from playwright.sync_api import sync_playwright


def browser_setup():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    return browser, playwright


def login(page):
    page.goto(LOGIN_URL)
    page.fill("input[name='username']", login_credentials['username'])
    page.fill("input[name='password']", login_credentials['password'])
    checkbox_label_selector = "label.mat-checkbox-layout span.mat-checkbox-inner-container"
    page.click(checkbox_label_selector)
    page.wait_for_function("() => !document.querySelector('button[type=submit]').disabled")
    page.click("button[type='submit']")

    # Handle the confirm login alert if it appears
    handle_confirm_login_alert(page)

    page.wait_for_load_state('networkidle')
    page.goto(HOME_URL)
    page.wait_for_load_state('networkidle')
    return page


def handle_confirm_login_alert(page):
    try:
        page.wait_for_selector("text=Confirm Login", timeout=10000)
        continue_button_selector = "button:has-text('Continue')"
        page.click(continue_button_selector)
        page.wait_for_timeout(2000)
    except Exception as e:
        print(f"Confirmation popup did not appear or failed to click 'Continue': {e}")


def close_browser(browser, playwright):
    browser.close()
    playwright.stop()
