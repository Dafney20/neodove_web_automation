import pytest
from constants import browser_setup, login, close_browser

@pytest.fixture(scope='module')
def browser_handle():
    browser, playwright = browser_setup()
    yield browser
    close_browser(browser, playwright)


@pytest.fixture(scope='function')
def page_handle(browser_handle):
    page = browser_handle.new_page()
    yield page
    page.close()


def test_login(page_handle):
    page = page_handle

    # Use the common function to log in and navigate to the home page
    login(page)

    # Verify the owner's name
    account_name_selector = "span.nd-logo-text"
    page.wait_for_selector(account_name_selector, timeout=20000)
    account_name = page.text_content(account_name_selector).strip()
    assert account_name == "Stalin Test", f"Expected account name 'Stalin Test' but got '{account_name}'"
    print(f"Verified account name: {account_name}")

    # Verify the dashboard
    dashboard_text_selector = "span.mat-button-wrapper.pl-7.ng-trigger.ng-trigger-animateText"
    page.wait_for_selector(dashboard_text_selector, timeout=20000)
    dashboard_text = page.text_content(dashboard_text_selector).strip()
    assert dashboard_text == "Dashboard", f"Expected text 'Dashboard' but got '{dashboard_text}'"
    print(f"Verified dashboard text: {dashboard_text}")

    # Verify the contacts
    contacts_text_selector = "span.mat-button-wrapper.pl-7.ng-trigger.ng-trigger-animateText"
    contacts_locator = page.locator(contacts_text_selector).locator('text=Contacts')
    contacts_locator.wait_for(timeout=20000)
    contacts_text = contacts_locator.text_content().strip()
    assert contacts_text == "Contacts", f"Expected text 'Contacts' but got '{contacts_text}'"
    print(f"Verified contacts text: {contacts_text}")

    # Navigate to Contacts page and then back to Home page
    page.goto("https://connect.neodove.com/contacts")
    page.wait_for_load_state('networkidle')
    print("Navigated to contacts page")
    page.goto("https://connect.neodove.com/home")
    page.wait_for_load_state('networkidle')

    # Verify the Pipeline
    pipeline_text_selector = "span.mat-button-wrapper.pl-7.mb-2.ng-trigger.ng-trigger-animateText"
    pipeline_locator = page.locator(pipeline_text_selector).locator('text=Pipeline')
    pipeline_locator.wait_for(timeout=20000)
    pipeline_text = pipeline_locator.text_content().strip()
    assert pipeline_text == "Pipeline", f"Expected text 'Pipeline' but got '{pipeline_text}'"
    print(f"Verified pipeline text: {pipeline_text}")

    # Verify the Integrations
    integrations_text_selector = "span.mat-button-wrapper.pl-7.ng-trigger.ng-trigger-animateText"
    integrations_locator = page.locator(integrations_text_selector).locator('text=Integrations')
    integrations_locator.wait_for(timeout=20000)
    integrations_text = integrations_locator.text_content().strip()
    assert integrations_text == "Integrations", f"Expected text 'Integrations' but got '{integrations_text}'"
    print(f"Verified integrations text: {integrations_text}")
