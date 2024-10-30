from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from faker import Faker


class RegisterPage(BasePage):
    base_url = BasePage.base_url + '/register'
    fake = Faker()

    email_form = (By.ID, 'email')
    first_name_form = (By.ID, 'first-name')
    last_name_form = (By.ID, 'last-name')
    password_form = (By.ID, 'password')
    confirm_password_form = (By.ID, 'confirm-password')
    checkboxes = (By.CSS_SELECTOR, '.sf-checkbox__container')
    submit_button = (By.CSS_SELECTOR, 'button[type="submit"]')
    success_msg = (By.CLASS_NAME, 'sf-notification__message')

    def __init__(self, driver):
        super().__init__(driver)

    def fill_form(self):
        """Заполняет форму регистрации и отправляет данные"""
        # Заполнение полей формы
        self.find_clickable_element(self.email_form).send_keys(self.fake.email())
        self.find_clickable_element(self.first_name_form).send_keys(self.fake.first_name())
        self.find_clickable_element(self.last_name_form).send_keys(self.fake.last_name())

        # Генерация пароля и заполнение полей для пароля и его подтверждения
        fake_password = self.fake.password()
        self.find_clickable_element(self.password_form).send_keys(fake_password)
        self.find_clickable_element(self.confirm_password_form).send_keys(fake_password)

        # Проставляет все чекбоксы на странице
        for checkbox in self.find_elements(self.checkboxes):
            checkbox.click()

        # Нажимает на кнопку отправки и проверяет успешную регистрацию
        self.find_clickable_element(self.submit_button).click()
        success_msg = self.find_clickable_element(self.success_msg)
        assert success_msg.text == 'Registration Successful'
        assert self.assert_url_changed(BasePage.base_url)
