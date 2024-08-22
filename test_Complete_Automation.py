import pytest
from constants import login_credentials, browser_setup, close_browser, handle_confirm_login_alert, login, LOGIN_URL, HOME_URL

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
    page.goto(LOGIN_URL)

    # Fill in username and password
    page.fill("input[name='username']", login_credentials['username'])
    page.fill("input[name='password']", login_credentials['password'])

    # Check the checkbox
    checkbox_label_selector = "label.mat-checkbox-layout span.mat-checkbox-inner-container"
    page.click(checkbox_label_selector)

    # Ensure the login button is enabled
    page.wait_for_function("() => !document.querySelector('button[type=submit]').disabled")
    button_enabled = page.evaluate("document.querySelector('button[type=submit]').disabled") == False
    assert button_enabled, "Button did not become enabled after clicking the checkbox."

    # Click the login button
    page.click("button[type=submit]")

    # Handle the confirm login alert if it appears
    handle_confirm_login_alert(page)

    # Wait for the navigation to the home page
    page.wait_for_load_state('networkidle')
    current_url = page.url
    assert current_url == HOME_URL, f"Expected URL '{HOME_URL}' but got '{current_url}'"
    page.wait_for_timeout(3000)


def test_login_page_elements(page_handle):
    page = page_handle
    page.goto(LOGIN_URL)

    header_text = page.inner_text("div.title")
    assert header_text == "Log in", f"Expected header text 'Log in' but got '{header_text}'"
    username_placeholder = page.get_attribute("input[name='username']", "placeholder")
    assert username_placeholder == "Email/Phone Number", f"Expected username placeholder 'Email/Phone Number' but got '{username_placeholder}'"
    password_placeholder = page.get_attribute("input[name='password']", "placeholder")
    assert password_placeholder == "Password", f"Expected password placeholder 'Password' but got '{password_placeholder}'"
    button_disabled = page.evaluate("document.querySelector('button[type=submit]').disabled")
    assert button_disabled, "Login button should be disabled by default"
    page.wait_for_timeout(3000)


@pytest.mark.parametrize('valid_username, invalid_password', [(login_credentials['username'], '677777')])
def test_invalid_login_invalid_password(page_handle, valid_username, invalid_password):
    page_handle.goto(LOGIN_URL)

    page_handle.wait_for_selector('//input[@name="username"]').type(valid_username)
    page_handle.wait_for_selector('//input[@name="password"]').type(invalid_password)

    checkbox_label_selector = "label.mat-checkbox-layout span.mat-checkbox-inner-container"
    page_handle.click(checkbox_label_selector)
    checkbox_input_selector = "#mat-checkbox-1-input"
    is_checked = page_handle.is_checked(checkbox_input_selector)
    page_handle.wait_for_selector('//button[@type="submit"]').click()
    page_handle.wait_for_timeout(3000)
    error_message = page_handle.wait_for_selector(
        '//span[contains(text(), "Please enter correct password!")]').text_content().strip()
    assert 'Please enter correct password!' == error_message


@pytest.mark.parametrize('invalid_username, valid_password', [('9999943211', login_credentials['password'])])
def test_invalid_login_invalid_username(page_handle, invalid_username, valid_password):
    page_handle.goto(LOGIN_URL)

    page_handle.wait_for_selector('//input[@name="username"]').type(invalid_username)
    page_handle.wait_for_selector('//input[@name="password"]').type(valid_password)

    checkbox_label_selector = "label.mat-checkbox-layout span.mat-checkbox-inner-container"
    page_handle.click(checkbox_label_selector)
    checkbox_input_selector = "#mat-checkbox-1-input"
    is_checked = page_handle.is_checked(checkbox_input_selector)
    page_handle.wait_for_selector('//button[@type="submit"]').click()
    page_handle.wait_for_timeout(3000)

    error_message = page_handle.wait_for_selector(
        '//span[contains(text(), "You are not verified. Please contact your NeoDove account manager!")]').text_content().strip()
    assert 'You are not verified. Please contact your NeoDove account manager!' == error_message


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

    #Verify contacts
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
    pipeline_button_selector = "span.mat-button-wrapper.pl-7.mb-2.ng-trigger.ng-trigger-animateText"
    page.wait_for_selector(pipeline_button_selector, timeout=20000)
    pipeline_button = page.query_selector(pipeline_button_selector)

    if pipeline_button:
        pipeline_button.click()
        print("Pipeline button clicked.")
    else:
        raise Exception("Pipeline button element not found.")

    page.wait_for_selector("span.mat-ripple.mat-list-item-ripple", timeout=20000)
    page.wait_for_timeout(3000)

    # Verify Sales Subdivision under Pipeline
    sales_button_selector = "span.mat-button-wrapper.pl-7:has-text('Sales')"
    page.wait_for_selector(sales_button_selector, timeout=20000)
    sales_button = page.query_selector(sales_button_selector)
    if sales_button:
        sales_button.click()
    else:
        raise Exception("Sales button element not found.")

    page.wait_for_load_state('networkidle')
    current_url = page.url
    assert current_url == "https://connect.neodove.com/campaign/65aac1b7b7eab91b44e038ff", f"Expected URL 'https://connect.neodove.com/campaign/65aac1b7b7eab91b44e038ff' but got '{current_url}'"
    print(f"Verified URL after clicking Sales: {current_url}")
    page.wait_for_timeout(3000)

    # Click the Pipeline button again to show sub-divisions
    pipeline_button = page.query_selector(pipeline_button_selector)
    if pipeline_button:
        pipeline_button.click()
    else:
        raise Exception("Pipeline button element not found.")

    page.wait_for_timeout(3000)

    # Verify Service Subdivision under Pipeline
    service_button_selector = "span.mat-button-wrapper.pl-7:has-text('Service')"
    page.wait_for_selector(service_button_selector, timeout=20000)
    service_button = page.query_selector(service_button_selector)
    if service_button:
        service_button.click()
    else:
        raise Exception("Service button element not found.")

    page.wait_for_load_state('networkidle')
    current_url = page.url
    assert current_url == "https://connect.neodove.com/campaign/65aac1b7b7eab91b44e03900", f"Expected URL 'https://connect.neodove.com/campaign/65aac1b7b7eab91b44e03900' but got '{current_url}'"
    print(f"Verified URL after clicking Service: {current_url}")
    page.wait_for_timeout(3000)

    # Click the Pipeline button again to show sub-divisions
    pipeline_button = page.query_selector(pipeline_button_selector)
    if pipeline_button:
        pipeline_button.click()
    else:
        raise Exception("Pipeline button element not found.")

    page.wait_for_timeout(3000)

    #Verify Reminder Subdivion under pipline
    reminder_button_selector = "span.mat-button-wrapper.pl-7:has-text('Reminder')"
    page.wait_for_selector(reminder_button_selector, timeout=20000)
    reminder_button = page.query_selector(reminder_button_selector)
    if reminder_button:
        reminder_button.click()
    else:
        raise Exception("Reminder button element not found.")

    page.wait_for_load_state('networkidle')
    current_url = page.url
    assert current_url == "https://connect.neodove.com/campaign/65aac1b7b7eab91b44e03901", f"Expected URL 'https://connect.neodove.com/campaign/65aac1b7b7eab91b44e03901' but got '{current_url}'"
    print(f"Verified URL after clicking Reminder: {current_url}")
    page.wait_for_timeout(3000)

    # Click the Pipeline button again to show sub-divisions
    pipeline_button = page.query_selector(pipeline_button_selector)
    if pipeline_button:
        pipeline_button.click()
    else:
        raise Exception("Pipeline button element not found.")

    page.wait_for_timeout(3000)

    #Verify Feedback
    feedback_button_selector = "span.mat-button-wrapper.pl-7:has-text('Feedback')"
    page.wait_for_selector(feedback_button_selector, timeout=20000)
    feedback_button = page.query_selector(feedback_button_selector)
    if feedback_button:
        feedback_button.click()
    else:
        raise Exception("Feedback button element not found.")

    page.wait_for_load_state('networkidle')
    current_url = page.url
    assert current_url == "https://connect.neodove.com/campaign/65aac1b7b7eab91b44e03902", f"Expected URL 'https://connect.neodove.com/campaign/65aac1b7b7eab91b44e03902' but got '{current_url}'"
    print(f"Verified URL after clicking Feedback: {current_url}")
    page.wait_for_timeout(3000)

    # Click the Pipeline button again to show sub-divisions
    pipeline_button = page.query_selector(pipeline_button_selector)
    if pipeline_button:
        pipeline_button.click()
    else:
        raise Exception("Pipeline button element not found.")

    page.wait_for_timeout(3000)

    #Verify Other
    other_button_selector = "span.mat-button-wrapper.pl-7:has-text('Other')"
    page.wait_for_selector(other_button_selector, timeout=20000)
    other_button = page.query_selector(other_button_selector)
    if other_button:
        other_button.click()
    else:
        raise Exception("Other button element not found.")

    page.wait_for_load_state('networkidle')
    current_url = page.url
    assert current_url == "https://connect.neodove.com/campaign/65aac1b7b7eab91b44e03903", f"Expected URL 'https://connect.neodove.com/campaign/65aac1b7b7eab91b44e03903' but got '{current_url}'"
    print(f"Verified URL after clicking Other: {current_url}")
    page.wait_for_timeout(3000)

    # Click the Pipeline button again to show sub-divisions
    pipeline_button = page.query_selector(pipeline_button_selector)
    if pipeline_button:
        pipeline_button.click()
    else:
        raise Exception("Pipeline button element not found.")

    page.wait_for_timeout(3000)

    #Verify testing pipline
    testing_pipeline_button_selector = "span.mat-button-wrapper.pl-7:has-text('Testing Pipeline')"
    page.wait_for_selector(testing_pipeline_button_selector, timeout=20000)
    testing_pipeline_button = page.query_selector(testing_pipeline_button_selector)
    if testing_pipeline_button:
        testing_pipeline_button.click()
    else:
        raise Exception("Testing Pipeline button element not found.")

    page.wait_for_load_state('networkidle')
    current_url = page.url
    assert current_url == "https://connect.neodove.com/campaign/65dc5b3ae3c28206f4c2dd1b", f"Expected URL 'https://connect.neodove.com/campaign/65dc5b3ae3c28206f4c2dd1b' but got '{current_url}'"
    print(f"Verified URL after clicking Testing Pipeline: {current_url}")

    # Click the Pipeline button again to show sub-divisions
    pipeline_button = page.query_selector(pipeline_button_selector)
    if pipeline_button:
        pipeline_button.click()
    else:
        raise Exception("Pipeline button element not found.")

    page.wait_for_timeout(3000)

    #Verify COKO NOKO
    coko_noko_button_selector = "span.mat-button-wrapper.pl-7:has-text('COKO NOKO')"
    page.wait_for_selector(coko_noko_button_selector, timeout=20000)
    coko_noko_button = page.query_selector(coko_noko_button_selector)
    if coko_noko_button:
        coko_noko_button.click()
    else:
        raise Exception("COKO NOKO button element not found.")

    page.wait_for_load_state('networkidle')
    current_url = page.url
    assert current_url == "https://connect.neodove.com/campaign/65e5c05c5bb80697ca43b2c6", f"Expected URL 'https://connect.neodove.com/campaign/65e5c05c5bb80697ca43b2c6' but got '{current_url}'"
    print(f"Verified URL after clicking COKO NOKO: {current_url}")
    page.wait_for_timeout(3000)

    # Click the Pipeline button again to show sub-divisions
    pipeline_button = page.query_selector(pipeline_button_selector)
    if pipeline_button:
        pipeline_button.click()
    else:
        raise Exception("Pipeline button element not found.")

    page.wait_for_timeout(3000)


    #Verify the new pipeline
    new_pipeline_button_selector = "span.mat-button-wrapper.pl-7:has-text('New Pipeline')"
    page.wait_for_selector(new_pipeline_button_selector, timeout=20000)
    new_pipeline_button = page.query_selector(new_pipeline_button_selector)
    if new_pipeline_button:
        new_pipeline_button.click()
    else:
        raise Exception("New Pipeline button element not found.")

    page.wait_for_load_state('networkidle')
    current_url = page.url
    assert current_url == "https://connect.neodove.com/campaign/66348838f22612dcb0b6651c", f"Expected URL 'https://connect.neodove.com/campaign/66348838f22612dcb0b6651c' but got '{current_url}'"
    print(f"Verified URL after clicking New Pipeline: {current_url}")
    page.wait_for_timeout(3000)

    # Click the Pipeline button again to show sub-divisions
    pipeline_button = page.query_selector(pipeline_button_selector)
    if pipeline_button:
        pipeline_button.click()
    else:
        raise Exception("Pipeline button element not found.")

    page.wait_for_timeout(3000)

    #Verify View all
    try:
        view_all_button_selector = "b:has-text('View all')"
        page.wait_for_selector(view_all_button_selector, timeout=20000)
        view_all_button = page.query_selector(view_all_button_selector)
        if view_all_button:
            view_all_button.click()
            print("View all button clicked.")
        else:
            raise Exception("View all button element not found.")
    except Exception as e:
        print("Error during View all button click:", e)
        raise

    page.wait_for_load_state('networkidle')
    current_url = page.url
    assert current_url == "https://connect.neodove.com/campaign/all", f"Expected URL 'https://connect.neodove.com/campaign/all' but got '{current_url}'"
    print(f"Verified URL after clicking View all: {current_url}")
    page.wait_for_timeout(3000)

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

    # Click the Trends button to display its subdivisions
    trends_locator.click()
    print("Trends button clicked.")
    page.wait_for_timeout(3000)  # Wait for the subdivisions to load

    # Verify and Click the Business Trend button
    business_trend_selector = "span.mat-button-wrapper.pl-7:has-text('Business Trend')"
    page.wait_for_selector(business_trend_selector, timeout=20000)
    business_trend_button = page.query_selector(business_trend_selector)
    if business_trend_button:
        business_trend_button.click()
        print("Business Trend button clicked.")
    else:
        raise Exception("Business Trend button element not found.")

    # Wait for navigation to the Business Trend URL
    page.wait_for_load_state('networkidle')
    current_url = page.url
    expected_url = "https://connect.neodove.com/trends/business"
    assert current_url == expected_url, f"Expected URL '{expected_url}' but got '{current_url}'"
    print(f"Verified URL after clicking Business Trend: {current_url}")
    page.wait_for_timeout(3000)

    # Click the Trends button again
    trends_locator.click()
    print("Trends button clicked again.")
    page.wait_for_timeout(3000)

    # Verify and Click the Users Trend button
    users_trend_selector = "span.mat-button-wrapper.pl-7:has-text('Users Trend')"
    page.wait_for_selector(users_trend_selector, timeout=20000)
    users_trend_button = page.query_selector(users_trend_selector)
    if users_trend_button:
        users_trend_button.click()
        print("Users Trend button clicked.")
    else:
        raise Exception("Users Trend button element not found.")

    # Wait for navigation to the Users Trend URL
    page.wait_for_load_state('networkidle')
    current_url = page.url
    expected_url = "https://connect.neodove.com/trends/user"
    assert current_url == expected_url, f"Expected URL '{expected_url}' but got '{current_url}'"
    print(f"Verified URL after clicking Users Trend: {current_url}")
    page.wait_for_timeout(3000)

    trends_locator.click()
    print("Trends button clicked again.")
    page.wait_for_timeout(3000)

    # Verify Reports

    # 1. Call Report under User
    # Click the Reports button
    reports_button_selector = "span.mat-button-wrapper.pl-7.mb-2:has-text('Reports')"
    page.wait_for_selector(reports_button_selector, timeout=20000)
    reports_button = page.query_selector(reports_button_selector)
    if reports_button:
        reports_button.click()
    else:
        raise Exception("Reports button element not found.")

    # Click the User sub-menu
    user_button_selector = "a#nd-user-report span.mat-button-wrapper.pl-7.mb-2:has-text('User')"
    page.wait_for_selector(user_button_selector, timeout=20000)
    user_button = page.query_selector(user_button_selector)
    if user_button:
        user_button.click()
    else:
        raise Exception("User button element not found.")

    # Click the Call Report button
    call_report_button_selector = "span.mat-button-wrapper.pl-7:has-text('Call Report')"
    page.wait_for_selector(call_report_button_selector, timeout=20000)
    call_report_button = page.query_selector(call_report_button_selector)
    if call_report_button:
        call_report_button.click()
    else:
        raise Exception("Call Report button element not found.")
    page.wait_for_load_state('networkidle')
    assert page.url == "https://connect.neodove.com/reports/user-report", f"Expected URL 'https://connect.neodove.com/reports/user-report' but got '{page.url}'"
    page.wait_for_timeout(2000)

    # 2. Login Report under User
    # Click the Reports button again
    page.goto("https://connect.neodove.com/home")
    page.wait_for_selector(reports_button_selector, timeout=20000)
    reports_button = page.query_selector(reports_button_selector)
    if reports_button:
        reports_button.click()
    else:
        raise Exception("Reports button element not found.")
    page.wait_for_timeout(2000)


    # Click the User sub-menu
    page.wait_for_selector(user_button_selector, timeout=20000)
    user_button = page.query_selector(user_button_selector)
    if user_button:
        user_button.click()
    else:
        raise Exception("User button element not found.")
    page.wait_for_timeout(2000)


    # Click the Login Report button
    login_report_button_selector = "span.mat-button-wrapper.pl-7:has-text('Login Report')"
    page.wait_for_selector(login_report_button_selector, timeout=20000)
    login_report_button = page.query_selector(login_report_button_selector)
    if login_report_button:
        login_report_button.click()
    else:
        raise Exception("Login Report button element not found.")
    page.wait_for_load_state('networkidle')
    assert page.url == "https://connect.neodove.com/reports/login-report", f"Expected URL 'https://connect.neodove.com/reports/login-report' but got '{page.url}'"
    page.wait_for_timeout(2000)

    # 3. Follow-up Report under User
    # Click the Reports button again
    page.goto("https://connect.neodove.com/home")
    page.wait_for_selector(reports_button_selector, timeout=20000)
    reports_button = page.query_selector(reports_button_selector)
    if reports_button:
        reports_button.click()
    else:
        raise Exception("Reports button element not found.")
    page.wait_for_timeout(2000)

    # Click the User sub-menu
    page.wait_for_selector(user_button_selector, timeout=20000)
    user_button = page.query_selector(user_button_selector)
    if user_button:
        user_button.click()
    else:
        raise Exception("User button element not found.")
    page.wait_for_timeout(2000)

    # Click the Follow-up Report button
    follow_up_report_button_selector = "span.mat-button-wrapper.pl-7:has-text('Follow-up Report')"
    page.wait_for_selector(follow_up_report_button_selector, timeout=20000)
    follow_up_report_button = page.query_selector(follow_up_report_button_selector)
    if follow_up_report_button:
        follow_up_report_button.click()
    else:
        raise Exception("Follow-up Report button element not found.")
    page.wait_for_load_state('networkidle')
    assert page.url == "https://connect.neodove.com/reports/follow-up", f"Expected URL 'https://connect.neodove.com/reports/follow-up' but got '{page.url}'"
    page.wait_for_timeout(2000)

    # 4. Campaign Report under Campaign
    # Click the Reports button again
    page.goto("https://connect.neodove.com/home")
    page.wait_for_selector(reports_button_selector, timeout=20000)
    reports_button = page.query_selector(reports_button_selector)
    if reports_button:
        reports_button.click()
    else:
        raise Exception("Reports button element not found.")
    page.wait_for_timeout(2000)

    # Click the Campaign sub-menu
    campaign_button_selector = "span.mat-button-wrapper.pl-5:has-text('Campaign')"
    page.wait_for_selector(campaign_button_selector, timeout=20000)
    campaign_button = page.query_selector(campaign_button_selector)
    if campaign_button:
        campaign_button.click()
    else:
        raise Exception("Campaign button element not found.")
    page.wait_for_timeout(2000)

    # Click the Campaign Report button
    campaign_report_button_selector = "span.mat-button-wrapper.pl-7:has-text('Campaign Report')"
    page.wait_for_selector(campaign_report_button_selector, timeout=20000)
    campaign_report_button = page.query_selector(campaign_report_button_selector)
    if campaign_report_button:
        campaign_report_button.click()
    else:
        raise Exception("Campaign Report button element not found.")
    page.wait_for_load_state('networkidle')
    assert page.url == "https://connect.neodove.com/reports/campaign-report", f"Expected URL 'https://connect.neodove.com/reports/campaign-report' but got '{page.url}'"
    page.wait_for_timeout(2000)

    # 5. Campaign Lead Report under Campaign
    # Click the Reports button again
    page.goto("https://connect.neodove.com/home")
    page.wait_for_selector(reports_button_selector, timeout=20000)
    reports_button = page.query_selector(reports_button_selector)
    if reports_button:
        reports_button.click()
    else:
        raise Exception("Reports button element not found.")
    page.wait_for_timeout(2000)

    # Click the Campaign sub-menu
    page.wait_for_selector(campaign_button_selector, timeout=20000)
    campaign_button = page.query_selector(campaign_button_selector)
    if campaign_button:
        campaign_button.click()
    else:
        raise Exception("Campaign button element not found.")
    page.wait_for_timeout(2000)


    # Click the Campaign Lead Report button
    campaign_lead_report_button_selector = "span.mat-button-wrapper.pl-7:has-text('Campaign Lead Report')"
    page.wait_for_selector(campaign_lead_report_button_selector, timeout=20000)
    campaign_lead_report_button = page.query_selector(campaign_lead_report_button_selector)
    if campaign_lead_report_button:
        campaign_lead_report_button.click()
    else:
        raise Exception("Campaign Lead Report button element not found.")
    page.wait_for_load_state('networkidle')
    assert page.url == "https://connect.neodove.com/reports/campaign-lead-report", f"Expected URL 'https://connect.neodove.com/reports/campaign-lead-report' but got '{page.url}'"
    page.wait_for_timeout(2000)


    # 6. Download Logs
    # Click the Reports button again
    page.goto("https://connect.neodove.com/home")
    page.wait_for_selector(reports_button_selector, timeout=20000)
    reports_button = page.query_selector(reports_button_selector)
    if reports_button:
        reports_button.click()
    else:
        raise Exception("Reports button element not found.")
    page.wait_for_timeout(2000)


    # Click the Download Logs button
    # 6. Download Logs
    # Click the Reports button again
    page.goto("https://connect.neodove.com/home")
    page.wait_for_selector(reports_button_selector, timeout=20000)
    reports_button = page.query_selector(reports_button_selector)
    if reports_button:
        reports_button.click()
    else:
        raise Exception("Reports button element not found.")
    page.wait_for_timeout(2000)


    # Click the Download Logs button
    download_logs_button_selector = "span.mat-button-wrapper.pl-5:has-text('Download Logs')"
    page.wait_for_selector(download_logs_button_selector, timeout=20000)
    download_logs_button = page.query_selector(download_logs_button_selector)
    if download_logs_button:
        download_logs_button.click()
    else:
        raise Exception("Download Logs button element not found.")
    page.wait_for_load_state('networkidle')
    assert page.url == "https://connect.neodove.com/reports/download-async-report", f"Expected URL 'https://connect.neodove.com/reports/download-async-report' but got '{page.url}'"
    page.wait_for_timeout(2000)

    # Verify MarketPlace
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

    # Verify SMS Automation
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

    # Verify Workflow
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

    # Verify Settings
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

