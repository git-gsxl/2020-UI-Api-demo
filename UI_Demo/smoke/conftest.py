import pytest
import time
from pages.page_login import Login
from common.driver import is_driver
browser = None


def screenshot():
    screen_img = browser.get_screenshot_as_base64()
    now_time = str(time.strftime('%Y-%m-%d %H-%M-%S'))
    browser.save_screenshot("../report/screenshot/" + now_time + ".jpg")
    return screen_img


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".jpg"
            screen_img = screenshot()
            if file_name:
                html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:600px;height:300px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % screen_img
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


@pytest.fixture(scope='session', autouse=True)
def driver(request):
    global browser
    if browser is None:
        browser = is_driver()

    def end():
        print("\n全部用例执行完后 teardown quit dirver")
        browser.quit()
    request.addfinalizer(end)
    return browser


@pytest.fixture(scope="session")
def login(driver):
    Login(driver).login_page()
    return driver


@pytest.fixture(scope="session")
def login1(driver):
    Login(driver).login_page(user="admin", pwd="123456")
    return driver


@pytest.fixture(scope="session")
def login2(driver):
    Login(driver).login_page(user="admin", pwd="123456")
    return driver
