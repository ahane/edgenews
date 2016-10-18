from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pytest

from edgenews import app

# @pytest.fixture(scope='module')
# def app():
#     app.run()
#     yield app
    #we need a way to shut down the app
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.close()

def test_signup(driver):
    driver.get("localhost:5000/signup")
    driver.find_element_by_name("name").send_keys("some-user-name")
    driver.find_element_by_name("email").send_keys("some@email.com")
    driver.find_element_by_name("plain_password").send_keys("apassword")
    driver.find_element_by_name("signup").send_keys(Keys.ENTER)
    assert "Welcome some-user-name" in driver.page_source

def test_signup_again(driver):
    driver.get("localhost:5000/signup")
    driver.find_element_by_name("name").send_keys("some-user-name")
    driver.find_element_by_name("email").send_keys("some@email.com")
    driver.find_element_by_name("plain_password").send_keys("apassword")
    driver.find_element_by_name("signup").send_keys(Keys.ENTER)
    assert "username already taken" in driver.page_source
