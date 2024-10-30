from pages.home_page import HomePage
from pages.register_page import RegisterPage
from pages.catalogue_page import CataloguePage
from pages.checkout_page import CheckoutPage


class TestBuyBlackConverse:
    def test_open_home_page(self, driver):
        home_page = HomePage(driver)

    def test_open_register_page(self, driver):
        home_page = HomePage(driver)
        home_page.click_profile_button()
        home_page.click_register_button()

    def test_register(self, driver):
        register_page = RegisterPage(driver)
        register_page.fill_form()

    def test_go_to_catalogue(self, driver):
        home_page = HomePage(driver)
        home_page.go_to_catalogue()

    def test_add_to_cart(self, driver):
        catalogue_page = CataloguePage(driver)
        catalogue_page.apply_filters()
        catalogue_page.add_product_to_cart()
        catalogue_page.check_total_price()
        catalogue_page.go_to_checkout()

    def test_checkout(self, driver):
        checkout_page = CheckoutPage(driver)
        checkout_page.submit_user_account_section()
        checkout_page.submit_shipping_section()
        checkout_page.submit_billing_section()
        checkout_page.test_payment_section()
