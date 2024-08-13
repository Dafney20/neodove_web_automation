import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope='module')
def browser_handle():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture(scope='function')
def page_handle(browser_handle):
    page = browser_handle.new_page()
    yield page
    page.close()


def test_login(page_handle):
    page = page_handle
    page.goto("https://connect.neodove.com/login")

    page.fill("input[name='username']", "9876543211")
    page.fill("input[name='password']", "12345")

    checkbox_label_selector = "label.mat-checkbox-layout span.mat-checkbox-inner-container"
    page.click(checkbox_label_selector)

    page.wait_for_function("() => !document.querySelector('button[type=submit]').disabled")
    button_enabled = page.evaluate("document.querySelector('button[type=submit]').disabled") == False
    assert button_enabled, "Button did not become enabled after clicking the checkbox."
    page.click("button[type=submit]")

    page.wait_for_load_state('networkidle')
    expected_home_url = "https://connect.neodove.com/home"
    current_url = page.url
    assert current_url == expected_home_url, f"Expected URL '{expected_home_url}' but got '{current_url}'"
    page.wait_for_timeout(3000)



def test_login_page_elements(page_handle):
    page = page_handle
    page.goto("https://connect.neodove.com/login")

    header_text = page.inner_text("div.title")
    assert header_text == "Log in", f"Expected header text 'Log in' but got '{header_text}'"
    username_placeholder = page.get_attribute("input[name='username']", "placeholder")
    assert username_placeholder == "Email/Phone Number", f"Expected username placeholder 'Email/Phone Number' but got '{username_placeholder}'"
    password_placeholder = page.get_attribute("input[name='password']", "placeholder")
    assert password_placeholder == "Password", f"Expected password placeholder 'Password' but got '{password_placeholder}'"
    button_disabled = page.evaluate("document.querySelector('button[type=submit]').disabled")
    assert button_disabled, "Login button should be disabled by default"
    page.wait_for_timeout(3000)

@pytest.mark.parametrize('valid_username, invalid_password', [('9876543211','677777')])
def test_invalid_login_invalid_password(page_handle, valid_username, invalid_password):
    page_handle.goto('https://connect.neodove.com/login')

    page_handle.wait_for_selector('//input[@name="username"]').type(valid_username)
    page_handle.wait_for_selector('//input[@name="password"]').type(invalid_password)

    checkbox_label_selector = "label.mat-checkbox-layout span.mat-checkbox-inner-container"
    page_handle.click(checkbox_label_selector)
    checkbox_input_selector = "#mat-checkbox-1-input"
    is_checked = page_handle.is_checked(checkbox_input_selector)
    page_handle.wait_for_selector('//button[@type="submit"]').click()
    page_handle.wait_for_timeout(3000)
    error_message = page_handle.wait_for_selector('//span[contains(text(), "Please enter correct password!")]').text_content().strip()
    assert 'Please enter correct password!' == error_message


@pytest.mark.parametrize('invalid_username, valid_password', [('9999943211','12345')])
def test_invalid_login_invalid_username(page_handle, invalid_username, valid_password):
    page_handle.goto('https://connect.neodove.com/login')

    page_handle.wait_for_selector('//input[@name="username"]').type(invalid_username)
    page_handle.wait_for_selector('//input[@name="password"]').type(valid_password)

    checkbox_label_selector = "label.mat-checkbox-layout span.mat-checkbox-inner-container"
    page_handle.click(checkbox_label_selector)
    checkbox_input_selector = "#mat-checkbox-1-input"
    is_checked = page_handle.is_checked(checkbox_input_selector)
    page_handle.wait_for_selector('//button[@type="submit"]').click()
    page_handle.wait_for_timeout(3000)

    error_message = page_handle.wait_for_selector('//span[contains(text(), "You are not verified. Please contact your NeoDove account manager!")]').text_content().strip()
    assert 'You are not verified. Please contact your NeoDove account manager!' == error_message
