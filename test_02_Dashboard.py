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
    page.wait_for_load_state('networkidle')
    page.goto("https://connect.neodove.com/marketplace")
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
    page.wait_for_load_state('networkidle')
    page.goto("https://connect.neodove.com/sms-automation")
    page.wait_for_load_state('networkidle')
    print("Navigated to SMS Automation page")
    page.goto("https://connect.neodove.com/home")
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(3000)

    # Verify the Workflow
    workflow_text_selector = "span.mat-button-wrapper.pl-7.ng-trigger.ng-trigger-animateText"
    workflow_locator = page.locator(workflow_text_selector).locator('text=Workflow')
    workflow_locator.wait_for(timeout=20000)
    workflow_text = workflow_locator.text_content().strip()
    assert workflow_text == "Workflow", f"Expected text 'Workflow' but got '{workflow_text}'"
    print(f"Verified workflow text: {workflow_text}")

    # Navigate to Workflow page and then back to Home page
    page.click("span.mat-button-wrapper.pl-7.ng-trigger.ng-trigger-animateText:has-text('Workflow')")
    page.wait_for_load_state('networkidle')
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
    page.wait_for_load_state('networkidle')
    page.goto('https://connect.neodove.com/settings/user')
    page.wait_for_load_state('networkidle')
    print("Navigated to Settings page")
    page.goto("https://connect.neodove.com/home")
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(3000)
