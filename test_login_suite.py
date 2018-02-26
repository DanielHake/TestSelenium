import pytest
from selenium.common.exceptions import StaleElementReferenceException
from selenium import webdriver


# notes:
# 1) to run on cmd: pytest test_login_suite.py -v
# 2) all the code before the yield counts as setup
# 3) all the code after the yield counts as teardown
# 4) valid input gets eli's stage user


# setup - chrome driver to login page
@pytest.fixture()
def core():
    driver = webdriver.Chrome()
    driver.get("http://dashboard.playermaker.co.uk/login")
    yield driver
    driver.close()


# get loader and wait till it isn't displayed anymore || i gets to 1000
def waitForLoader(driver):
    element = driver.find_element_by_class_name("fullscreenDiv")
    try:
        i = 0
        while (element.is_displayed() and i < 1000):
            i += 1
    except StaleElementReferenceException:
        print("StaleElementReferenceException occurred")


# given a exists user - "userName" & "password" and submit
# result == url end should contain "team"
@pytest.mark.parametrize("username,password", [
    ("$$_elir", 123456),
])
def test_valid_inputs(core,username,password):
    core.find_elements_by_tag_name("input")[0].send_keys(username)
    core.find_elements_by_tag_name("input")[1].send_keys(password)
    core.find_element_by_class_name("btn-primary").submit()
    waitForLoader(core)
    url = core.current_url
    assert url == "http://dashboard.playermaker.co.uk/team"


# given an non-exists user - "userName" & "password" and submit
# result == url end should still contain "login"
@pytest.mark.parametrize("username,password", [
    ("$$_elir", 123),
    ("$$_delpiero", 123456),
    ("$$_nedved", 11),
])
def test_invalid_inputs(core,username,password):
    core.find_elements_by_tag_name("input")[0].send_keys(username)
    core.find_elements_by_tag_name("input")[1].send_keys(password)
    core.find_element_by_class_name("btn-primary").submit()
    waitForLoader(core)
    url = core.current_url
    assert url == "http://dashboard.playermaker.co.uk/login"