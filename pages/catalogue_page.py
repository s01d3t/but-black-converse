from random import choice
from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class CataloguePage(BasePage):
    base_url = BasePage.base_url + '/c/men.html'

    products = (By.CLASS_NAME, 'sf-product-card__image')
    colors = (By.CLASS_NAME, 'product__color')
    sizes = (By.CSS_SELECTOR, '.swatch_text_button')
    add_to_cart_button = (By.CSS_SELECTOR, '.sf-add-to-cart__button')
    cart = (By.CLASS_NAME, 'mini-cart')
    item_price = (By.CLASS_NAME, 'card__price')
    total_price = (By.CLASS_NAME, 'sf-price__regular')
    checkout_button = (By.CSS_SELECTOR, 'button[data-testid="category-sidebar-go-to-checkout"]')
    filter_brand = (By.CSS_SELECTOR, 'button[color="CONVERSE"]')
    filter_color = (By.CSS_SELECTOR, 'button[custion-id="Black"')
    apply_filters_button = (By.CSS_SELECTOR, 'button[data-testid="apply-filters"]')
    filter_labels = (By.CLASS_NAME, 'selected-filter__label')

    def __init__(self, driver):
        super().__init__(driver)

    def apply_filters(self):
        """Применяет фильтры по бренду и цвету и подтверждает их"""
        self.driver.execute_script("window.scrollBy(0, 700);")
        brand_filter = self.find_clickable_element(self.filter_brand)
        color_filter = self.find_clickable_element(self.filter_color)
        apply_filters_btn = self.find_clickable_element(self.apply_filters_button)

        # Применяет фильтры с помощью кликов
        self.action.move_to_element(brand_filter).click().perform()
        self.action.move_to_element(color_filter).click().perform()
        self.action.move_to_element(apply_filters_btn).click().perform()

    def add_product_to_cart(self):
        """Выбирает случайный продукт, настраивает его опции и добавляет в корзину"""
        # Проверяет наличие продуктов, соответствующих фильтрам
        products = self.find_elements(self.products)
        if not products:
            raise Exception('Нет продуктов для выбранных фильтров')

        # Открывает карточку случайного продукта
        choice(products).click()

        # Выбирает доступные цвета и размеры
        for color in self.find_elements(self.colors):
            self.action.move_to_element(color).click().perform()

        for size in self.find_elements(self.sizes):
            self.action.move_to_element(size).click().perform()

        # Добавляет товар в корзину и проверяет, что корзина открыта
        self.find_clickable_element(self.add_to_cart_button).click()
        assert self.find_clickable_element(self.cart)

    def check_total_price(self):
        """Проверяет, что итоговая цена соответствует цене товара"""
        item_price = self.driver.find_element(*self.item_price).text
        total_price = self.driver.find_element(*self.total_price).text
        assert item_price == total_price, "Итоговая цена не совпадает с ценой товара"

    def go_to_checkout(self):
        """Переходит к оформлению заказа и проверяет переход на страницу пользователя"""
        self.find_clickable_element(self.checkout_button).click()
        assert self.assert_url_changed(BasePage.base_url + '/checkout/user-account')
