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

    # Verify the Trends
    trends_text_selector = "span.mat-button-wrapper.pl-7.mb-2.ng-trigger.ng-trigger-animateText"
    trends_locator = page.locator(trends_text_selector).locator('text=Trends')
    trends_locator.wait_for(timeout=20000)
    trends_text = trends_locator.text_content().strip()
    assert trends_text == "Trends", f"Expected text 'Trends' but got '{trends_text}'"
    print(f"Verified trends text: {trends_text}")

    # Verify the Reports
    reports_text_selector = "span.mat-button-wrapper.pl-7.mb-2.ng-trigger.ng-trigger-animateText"
    reports_locator = page.locator(reports_text_selector).locator('text=Reports')
    reports_locator.wait_for(timeout=20000)
    reports_text = reports_locator.text_content().strip()
    assert reports_text == "Reports", f"Expected text 'Reports' but got '{reports_text}'"
    print(f"Verified reports text: {reports_text}")

    # Verify the Marketplace
    marketplace_text_selector = "span.mat-button-wrapper.pl-7.ng-trigger.ng-trigger-animateText"
    marketplace_locator = page.locator(marketplace_text_selector).locator('text=Marketplace')
    marketplace_locator.wait_for(timeout=20000)
    marketplace_text = marketplace_locator.text_content().strip()
    assert marketplace_text == "Marketplace", f"Expected text 'Marketplace' but got '{marketplace_text}'"
    print(f"Verified marketplace text: {marketplace_text}")

    # Navigate to Marketplace page and then back to Home page
    page.click("span.mat-button-wrapper.pl-7.ng-trigger.ng-trigger-animateText:has-text('Marketplace')")
    page.goto('https://connect.neodove.com/marketplace')
    page.wait_for_load_state('networkidle')
    print("Navigated to Marketplace page")

    page.goto("https://connect.neodove.com/home")
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(3000)

    # Verify the SMS Automation
    sms_automation_text_selector = "span.mat-button-wrapper.pl-7.ng-trigger.ng-trigger-animateText"
    sms_automation_locator = page.locator(sms_automation_text_selector).locator('text=SMS Automation')
    sms_automation_locator.wait_for(timeout=20000)
    sms_automation_text = sms_automation_locator.text_content().strip()
    assert sms_automation_text == "SMS Automation", f"Expected text 'SMS Automation' but got '{sms_automation_text}'"
    print(f"Verified SMS Automation text: {sms_automation_text}")

    # Navigate to SMS Automation page and then back to Home page
    page.click("span.mat-button-wrapper.pl-7.ng-trigger.ng-trigger-animateText:has-text('SMS Automation')")
    page.goto('https://connect.neodove.com/sms-automation')
    page.wait_for_load_state('networkidle')
    print("Navigated to SMS Automation page")

    page.goto("https://connect.neodove.com/home")
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(3000)