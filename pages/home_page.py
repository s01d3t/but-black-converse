from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class HomePage(BasePage):
    base_url = BasePage.base_url

    profile_button = (By.CSS_SELECTOR, 'img[src="/hudson/account.svg"]')
    register_button = (By.LINK_TEXT, 'Register Now')
    men_catalogue_button = (By.LINK_TEXT, 'Men')

    def __init__(self, driver):
        super().__init__(driver)

    def click_profile_button(self):
        """Нажимает на кнопку профиля и проверяет, что произошел переход на страницу логина"""
        self.find_clickable_element(self.profile_button).click()
        assert self.assert_url_changed(self.base_url + '/login')

    def click_register_button(self):
        """Нажимает на кнопку регистрации и проверяет, что произошел переход на страницу регистрации"""
        self.find_clickable_element(self.register_button).click()
        assert self.assert_url_changed(self.base_url + '/register')

    def go_to_catalogue(self):
        """Переходит в каталог для мужчин и проверяет URL"""
        self.find_clickable_element(self.men_catalogue_button).click()
        assert self.assert_url_changed(self.base_url + '/c/men.html')
