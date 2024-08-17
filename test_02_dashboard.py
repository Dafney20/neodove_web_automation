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

def test_dashboard(page_handle):
    page = page_handle


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

    # Verify contacts
    contacts_button_selector = "a[title='Contacts'] span.mat-button-wrapper:has-text('Contacts')"
    page.wait_for_selector(contacts_button_selector, timeout=20000)
    contacts_button = page.query_selector(contacts_button_selector)
    if contacts_button:
        contacts_button.click()
    else:
        raise Exception("Contacts button element not found.")
    page.wait_for_load_state('networkidle')  # Ensure the network is idle which implies page has loaded
    current_url = page.url
    assert current_url == "https://connect.neodove.com/contacts", f"Expected URL 'https://connect.neodove.com/contacts' but got '{current_url}'"
    print(f"Verified URL after clicking Contacts: {current_url}")
    page.wait_for_timeout(3000)

    # Verify the Pipeline
    pipeline_text_selector = "span.mat-button-wrapper.pl-7.mb-2.ng-trigger.ng-trigger-animateText"
    pipeline_locator = page.locator(pipeline_text_selector).locator('text=Pipeline')
    pipeline_locator.wait_for(timeout=20000)
    pipeline_text = pipeline_locator.text_content().strip()
    assert pipeline_text == "Pipeline", f"Expected text 'Pipeline' but got '{pipeline_text}'"
    print(f"Verified pipeline text: {pipeline_text}")

    # Verify the Integrations
    integrations_button_selector = "a[title='Integrations'] span.mat-button-wrapper:has-text('Integrations')"
    page.wait_for_selector(integrations_button_selector, timeout=20000)
    integrations_button = page.query_selector(integrations_button_selector)

    if integrations_button:
        integrations_button.click()
    else:
        raise Exception("Integrations button element not found.")

    page.wait_for_load_state('networkidle')
    current_url = page.url
    assert current_url == "https://connect.neodove.com/integration", f"Expected URL 'https://connect.neodove.com/integration' but got '{current_url}'"
    print(f"Verified URL after clicking Integrations: {current_url}")
    page.wait_for_timeout(3000)

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


    #Verify MarketPlace
    marketplace_button_selector = "a[title='Marketplace'] span.mat-button-wrapper:has-text('Marketplace')"
    page.wait_for_selector(marketplace_button_selector, timeout=20000)
    marketplace_button = page.query_selector(marketplace_button_selector)

    if marketplace_button:
        marketplace_button.click()
    else:
        raise Exception("Marketplace button element not found.")

    page.wait_for_load_state('networkidle')
    current_url = page.url
    assert current_url == "https://connect.neodove.com/marketplace", f"Expected URL 'https://connect.neodove.com/marketplace' but got '{current_url}'"
    print(f"Verified URL after clicking Marketplace: {current_url}")
    page.wait_for_timeout(3000)


    #Verify SMS Automation
    sms_automation_button_selector = "a[title='SMS Automation'] span.mat-button-wrapper:has-text('SMS Automation')"
    page.wait_for_selector(sms_automation_button_selector, timeout=20000)
    sms_automation_button = page.query_selector(sms_automation_button_selector)

    if sms_automation_button:
        sms_automation_button.click()
    else:
        raise Exception("SMS Automation button element not found.")

    page.wait_for_load_state('networkidle')
    current_url = page.url
    assert current_url == "https://connect.neodove.com/sms-automation", f"Expected URL 'https://connect.neodove.com/sms-automation' but got '{current_url}'"
    print(f"Verified URL after clicking SMS Automation: {current_url}")
    page.wait_for_timeout(3000)


    #Verify Workflow
    workflow_button_selector = "a[routerlink='/workflow'] span.mat-button-wrapper:has-text('Workflow')"
    page.wait_for_selector(workflow_button_selector, timeout=20000)
    workflow_button = page.query_selector(workflow_button_selector)

    if workflow_button:
        workflow_button.click()
    else:
        raise Exception("Workflow button element not found.")

    page.wait_for_load_state('networkidle')
    current_url = page.url
    assert current_url == "https://connect.neodove.com/workflow", f"Expected URL 'https://connect.neodove.com/workflow' but got '{current_url}'"
    print(f"Verified URL after clicking Workflow: {current_url}")
    page.wait_for_timeout(3000)


    #Verify Settings
    settings_button_selector = "a[title='Settings'] span.mat-button-wrapper:has-text('Settings')"
    page.wait_for_selector(settings_button_selector, timeout=20000)
    settings_button = page.query_selector(settings_button_selector)
    if settings_button:
        settings_button.click()
    else:
        raise Exception("Settings button element not found.")
    page.wait_for_load_state('networkidle')
    current_url = page.url
    assert current_url == "https://connect.neodove.com/settings/user", f"Expected URL 'https://connect.neodove.com/settings/user' but got '{current_url}'"
    print(f"Verified URL after clicking Settings: {current_url}")

    page.wait_for_timeout(3000)


