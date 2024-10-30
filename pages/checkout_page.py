from faker import Faker
from random import randint

from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class CheckoutPage(BasePage):
    base_url = BasePage.base_url + '/checkout/user-account'
    fake = Faker()

    submit_button = (By.CSS_SELECTOR, '.form__action-button.sf-button')
    first_name = (By.ID, 'firstName')
    last_name = (By.ID, 'lastName')
    street_name = (By.ID, 'streetName')
    zip_code = (By.ID, 'zipCode')
    apartment = (By.ID, 'apartment')
    city_dropdown = (By.CSS_SELECTOR, '.vs__search:nth-child(1)')
    phone = (By.ID, 'telephone')
    radiobutton = (By.CSS_SELECTOR, '.sf-radio__checkmark')
    success_alert = (By.CSS_SELECTOR, '.sf-notification.color-success')

    def __init__(self, driver):
        super().__init__(driver)

    def submit_user_account_section(self):
        """Отправляет данные пользователя в секции аккаунта и переходит к секции доставки"""
        self.wait_for_alert_to_disappear(self.success_alert)
        submit_button = self.find_clickable_element(self.submit_button)
        self.action.move_to_element(submit_button).click().perform()
        assert self.assert_url_changed(BasePage.base_url + '/checkout/shipping')

    def submit_shipping_section(self):
        """Заполняет и отправляет данные в секции доставки, затем переходит к секции оплаты"""
        self.find_clickable_element(self.first_name).send_keys(self.fake.first_name())
        self.find_clickable_element(self.last_name).send_keys(self.fake.last_name())
        self.find_clickable_element(self.street_name).send_keys(self.fake.street_name())
        self.find_clickable_element(self.phone).send_keys(self.fake.msisdn())
        self.find_clickable_element(self.zip_code).send_keys(self.fake.zipcode())
        self.find_clickable_element(self.apartment).send_keys(randint(1, 10))

        # Выбирает город в раскрывающемся списке
        city_dropdown = self.find_clickable_element(self.city_dropdown)
        city_dropdown.send_keys('a' + Keys.ENTER)

        # Кликает на кнопку отправки и радиокнопку, затем подтверждает переход к секции оплаты
        self.find_clickable_element(self.submit_button).click()
        self.find_clickable_element(self.radiobutton).click()
        self.find_clickable_element(self.submit_button).click()
        assert self.assert_url_changed(BasePage.base_url + '/checkout/billing')

    def submit_billing_section(self):
        """Отправляет данные в секции биллинга и переходит к секции платежей"""
        self.find_clickable_element(self.submit_button).click()
        assert self.assert_url_changed(BasePage.base_url + '/checkout/payment')

    def test_payment_section(self):
        """Тестирует доступные способы оплаты, кликая на каждый из них"""
        payment_options = self.find_elements(self.radiobutton)
        for option in payment_options:
            option.click()
