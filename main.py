from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
import time
import urllib.request
import json
import pytest

# @pytest.fixture()
# def setup():
#     msg = "hello"
#     return msg
#
# @pytest.mark.parametrize("test_input,expected", [
#     ("3+5", 8),
#     ("2+4", 6),
#     ("6*9", 42),
# ])
# def test_eval(setup,test_input, expected):
#     print(setup)
#     assert eval(test_input) == expected



####################################################################
# example of post login
def login():
    url = 'http://soccerstage.motionizeme.com/api/v4'
    path = "/users/login"
    url = url + path

    body = {
            'username': 'elir',
            'password': '123456'
            }
    data = urllib.parse.urlencode(body)
    data = data.encode('ascii') # data should be bytes
    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as response:
       the_page = response.read()
    myjson = the_page
    parsed = json.loads(myjson)
    # coach = parsed["first_name"] + " "+ parsed["last_name"]
    # print(coach)
    teams = parsed["teams"]
    print(teams)
    dicto = {}
    i = 0
    for team in teams:
        dicto[i] = team["image_url"]
        i = i+1
    print(dicto)
    # print(json.dumps(parsed,indent=4,sort_keys=True))
login()
# time.sleep(2)
# print(the_page)
#########################################################################
############### first get dashboard & test
# # init chrome driver
# driver = webdriver.Chrome()
# # open dashboard
# driver.get("http://dashboard.playermaker.co.uk/login")
# # get input name & password -> send them eli credentials
# driver.find_elements_by_tag_name("input")[0].send_keys("$$_elir")
# driver.find_elements_by_tag_name("input")[1].send_keys("123456")
# # wait a sec
# driver.implicitly_wait(1)
# # submit the login form
# driver.find_element_by_class_name("btn-primary").submit()
# element = driver.find_element_by_class_name("fullscreenDiv")
# # example of try & except
# try:
#     i = 1
#     while(element.is_displayed()):
#         print(i)
#         i += 1
# except StaleElementReferenceException:
#     print("over")
#
#
# teams = {}
# div = driver.find_element_by_class_name("user_teams").find_elements_by_tag_name("li")
# for i in range(0,len(div)):
#     teams[i] = div.__getitem__(i).find_element_by_tag_name("p").text
#     # print("#",i," - Team: ", div.__getitem__(i).find_element_by_tag_name("p").text)
# print(teams)
#
#
#


