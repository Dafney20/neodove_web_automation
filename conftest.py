import pytest

@pytest.hookimpl(tryfirst=True)
def pytest_html_report_title(report):
    report.title = "Neodove Web Automation Report"
