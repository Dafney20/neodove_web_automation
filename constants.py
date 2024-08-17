# constants.py

# Username and Password stored as constants
login_credentials = {
    'username': '9876543211',
    'password': '12345'
}

from playwright.sync_api import sync_playwright

def browser_setup():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    return browser, playwright

def login(page):
    page.goto("https://connect.neodove.com/login")
    page.fill("input[name='username']", login_credentials['username'])
    page.fill("input[name='password']", login_credentials['password'])
    checkbox_label_selector = "label.mat-checkbox-layout span.mat-checkbox-inner-container"
    page.click(checkbox_label_selector)
    page.wait_for_function("() => !document.querySelector('button[type=submit]').disabled")
    page.click("button[type='submit']")
    page.wait_for_load_state('networkidle')
    page.goto("https://connect.neodove.com/home")
    page.wait_for_load_state('networkidle')
    return page

def close_browser(browser, playwright):
    browser.close()
    playwright.stop()

