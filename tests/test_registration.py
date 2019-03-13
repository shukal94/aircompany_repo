
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pytest
from tests.test_utils import UserFactory


class TestRegistration():

    @classmethod
    def setup_class(cls):
        cls.minimal_user = UserFactory().create_minimal_user()


    def setup(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(5)
        self.browser.get('http://localhost:5000/')

    def teardown(self):
        self.browser.close()


    def test_minimal_registration(self):
        reg_button = self.browser.find_element_by_link_text('Click to Register!')
        reg_button.click()

        field = self.browser.find_element_by_id('username')
        field.send_keys(self.minimal_user.username)

        first_name = self.browser.find_element_by_id('first_name')
        first_name.send_keys(self.minimal_user.first_name)

        last_name = self.browser.find_element_by_id('last_name')
        last_name.send_keys(self.minimal_user.last_name)

        email = self.browser.find_element_by_id('email')
        email.send_keys(self.minimal_user.email)

        password = self.browser.find_element_by_id('password')
        password.send_keys(self.minimal_user.password)

        repeat_password = self.browser.find_element_by_id('password2')
        repeat_password.send_keys(self.minimal_user.password2)

        address = self.browser.find_element_by_id('address')
        address.send_keys(self.minimal_user.address)

        postal_code = self.browser.find_element_by_id('postal_code')
        postal_code.send_keys(self.minimal_user.postal_code)

        button = self.browser.find_element_by_id('submit')
        button.click()

        insert_username = self.browser.find_element_by_id('username')
        insert_username.send_keys(self.minimal_user.username)

        insert_password = self.browser.find_element_by_id('password')
        insert_password.send_keys(self.minimal_user.password)

        login_button = self.browser.find_element_by_id('submit')
        login_button.click()

        element = self.browser.find_element(By.XPATH, "//*[contains(text(), 'Hi')]")
        if element:
            logout_button = self.browser.find_element(By.XPATH, "//*[contains(text(), 'Logout')]")
            logout_button.click()


    # phone_field = browser.find_element_by_id('DataViewModel.Phone_I')
    #
    # for _ in range(22):
    #     phone_field.send_keys(Keys.ARROW_LEFT)
    #
    # phone_field.send_keys('375111111111')
    # button = browser.find_element_by_id('btnNext')
    # button.click()

# class TestAuth:
#     @classmethod
#     def setup_class(cls):
#         """ preconditions for suite preconditions """
#
#     def setup(self):
#         """ logic for test precondintions """
#
#     def test_user_can_succesfully_login(self):
#         """ test logic """
