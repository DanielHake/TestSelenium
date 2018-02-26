import pytest
import time
from selenium.common.exceptions import StaleElementReferenceException
from selenium import webdriver
import urllib.request
import json


# notes:
# 1) to run on cmd: pytest test_teams_page_suite.py -v
# 2) all the code before the yield counts as setup
# 3) all the code after the yield counts as teardown
# 4) getting json only once
#




# setup - chrome driver to login page


@pytest.fixture(scope="module")
def core():
    driver = webdriver.Chrome()
    return driver

@pytest.fixture(scope="module")
def login_json():
    url = 'http://soccerstage.motionizeme.com/api/v4'
    path = "/users/login"
    url = url + path

    body = {
        'username': 'elir',
        'password': '123456'
    }
    data = urllib.parse.urlencode(body)
    data = data.encode('ascii')  # data should be bytes
    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as response:
        the_page = response.read()
    myjson = the_page
    parsed = json.loads(myjson)
    return parsed


def waitForLoader(driver):
    element = driver.find_element_by_class_name("fullscreenDiv")
    try:
        i = 0
        while (element.is_displayed() and i < 1000):
            i += 1
    except StaleElementReferenceException:
        print("StaleElementReferenceException occurred")


# compare image url & name for each team in the json to the dashboard
def test_teams_photos(core,login_json):
    core.get("http://dashboard.playermaker.co.uk/login")
    core.find_elements_by_tag_name("input")[0].send_keys("$$_elir")
    core.find_elements_by_tag_name("input")[1].send_keys("123456")
    core.find_element_by_class_name("btn-primary").submit()
    waitForLoader(core)
    url = core.current_url
    if (url != "http://dashboard.playermaker.co.uk/team"):
        assert True == False

    # get images from json
    json_teams = login_json["teams"]
    json_teams_dictionary = {}
    dashboard_teams_dictionary = {}
    index = 0
    for team in json_teams:
        json_teams_dictionary[index] = {team["team_name"],
                                        team["image_url"]}
        index = index + 1
    div = core.find_element_by_class_name("user_teams").find_elements_by_tag_name("li")
    for k in range(0, len(div)):
        dashboard_teams_dictionary[k] = {div[k].find_element_by_tag_name("p").text,
                                         div[k].find_element_by_tag_name("img").get_attribute("src")}
    assert json_teams_dictionary == dashboard_teams_dictionary


def test_coach_name(core,login_json):
    core.get("http://dashboard.playermaker.co.uk/login")
    core.find_elements_by_tag_name("input")[0].send_keys("$$_elir")
    core.find_elements_by_tag_name("input")[1].send_keys("123456")
    core.find_element_by_class_name("btn-primary").submit()
    waitForLoader(core)
    url = core.current_url
    if (url != "http://dashboard.playermaker.co.uk/team"):
        assert True == False
    # get coach name from dash
    coach = core.find_element_by_class_name("coach_profile")
    dashboard_coach_name = coach.find_element_by_tag_name("h1").text
    print("dashboard coach: ", dashboard_coach_name)
    # get coach name from json
    json_coach = login_json["first_name"] + " " + login_json["last_name"]
    print("json coach: ", json_coach)
    assert json_coach == dashboard_coach_name


# compare json teams to dashboard teams
def test_num_of_teams(core,login_json):
    core.get("http://dashboard.playermaker.co.uk/login")
    core.find_elements_by_tag_name("input")[0].send_keys("$$_elir")
    core.find_elements_by_tag_name("input")[1].send_keys("123456")
    core.find_element_by_class_name("btn-primary").submit()
    waitForLoader(core)
    url = core.current_url
    if (url != "http://dashboard.playermaker.co.uk/team"):
        assert True == False

    div = core.find_element_by_class_name("user_teams").find_elements_by_tag_name("li")
    teams = login_json["teams"]
    dashboard_teams = {}
    json_teams = {}
    j=0
    for team in teams:
        json_teams[j] = team["team_name"]
        j = j + 1
    for k in range(0, len(div)):
        dashboard_teams[k] = div.__getitem__(k).find_element_by_tag_name("p").text
    # if (len(json_teams) != len(dashboard_teams)):
    #     assert True == False
    # else:
    #     print("Number of teams: ",len(json_teams))
    assert json_teams == dashboard_teams

# logout test
def test_logout(core):
    core.find_element_by_class_name("dropdown-toggle").click()
    core.find_element_by_class_name("dropdown-menu").find_elements_by_tag_name("a")[3].click()
    waitForLoader(core)
    url = core.current_url
    assert "http://dashboard.playermaker.co.uk/login" == url