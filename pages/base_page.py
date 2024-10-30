from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    base_url = 'https://www.hudsonstore.com/mt'

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.action = ActionChains(self.driver)
        self.open_page()

    def open_page(self):
        """Открывает базовый URL, если текущий URL отличается"""
        if self.driver.current_url != self.base_url:
            self.driver.get(self.base_url)
            assert self.assert_url_changed(self.base_url)

    def assert_url_changed(self, expected_url):
        """Ждет, пока URL изменится на ожидаемый"""
        try:
            WebDriverWait(self.driver, 10).until(EC.url_to_be(expected_url))
            return True
        except Exception as e:
            print(f"Ошибка при ожидании URL: {e}")
            print(f"Текущий URL: {self.driver.current_url}")
            return False

    def wait_for_page_to_load(self):
        """Ожидает полной загрузки страницы"""
        self.wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

    def wait_for_alert_to_disappear(self, alert_locator):
        """Ждет, пока алерт с указанным локатором исчезнет со страницы"""
        self.wait.until(EC.staleness_of(self.driver.find_element(*alert_locator)),
                        message=f"Алерт с локатором {alert_locator} не исчез")

    def find_clickable_element(self, locator):
        """Находит и возвращает кликабельный элемент с указанным локатором"""
        self.wait_for_page_to_load()
        self.wait.until(EC.visibility_of_element_located(locator),
                        message=f"Элемент {locator} не видно")
        return self.wait.until(EC.element_to_be_clickable(locator),
                               message=f"Элемент {locator} не найден")

    def find_elements(self, locator):
        """Возвращает все элементы, найденные по указанному локатору"""
        self.wait_for_page_to_load()
        return self.wait.until(EC.presence_of_all_elements_located(locator))
