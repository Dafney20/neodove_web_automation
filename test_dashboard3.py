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

def test_workflow(page_handle):
    page = page_handle
    page.goto("https://connect.neodove.com/login")

    # Log in
    page.fill("input[name='username']", "9876543211")
    page.fill("input[name='password']", "12345")
    checkbox_label_selector = "label.mat-checkbox-layout span.mat-checkbox-inner-container"
    page.click(checkbox_label_selector)
    page.wait_for_function("() => !document.querySelector('button[type=submit]').disabled")
    page.click("button[type='submit']")
    page.wait_for_load_state('networkidle')

    # Navigate to home page
    page.goto("https://connect.neodove.com/home")
    page.wait_for_load_state('networkidle')

    # Verify the Workflow
    workflow_text_selector = "span.mat-button-wrapper.pl-7.ng-trigger.ng-trigger-animateText"
    workflow_locator = page.locator(workflow_text_selector).locator('text=Workflow')
    workflow_locator.wait_for(timeout=20000)
    workflow_text = workflow_locator.text_content().strip()
    assert workflow_text == "Workflow", f"Expected text 'Workflow' but got '{workflow_text}'"
    print(f"Verified workflow text: {workflow_text}")

    # Navigate to Workflow page and then back to Home page
    page.click("span.mat-button-wrapper.pl-7.ng-trigger.ng-trigger-animateText:has-text('Workflow')")
    page.goto('https://connect.neodove.com/workflow')
    page.wait_for_load_state('networkidle')
    print("Navigated to Workflow page")

    page.goto("https://connect.neodove.com/home")
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(3000)

    # Verify the Settings
    settings_text_selector = "span.mat-button-wrapper.pl-7.ng-trigger.ng-trigger-animateText"
    settings_locator = page.locator(settings_text_selector).locator('text=Settings')
    settings_locator.wait_for(timeout=20000)
    settings_text = settings_locator.text_content().strip()
    assert settings_text == "Settings", f"Expected text 'Settings' but got '{settings_text}'"
    print(f"Verified settings text: {settings_text}")

    # Navigate to Settings page and then back to Home page
    page.click("span.mat-button-wrapper.pl-7.ng-trigger.ng-trigger-animateText:has-text('Settings')")
    page.goto('https://connect.neodove.com/settings/user')
    page.wait_for_load_state('networkidle')
    print("Navigated to Settings page")

    page.goto("https://connect.neodove.com/home")
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(3000)
