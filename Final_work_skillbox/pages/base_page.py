from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
import time


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_element(self, locator, timeout=10) -> WebElement:
        """Поиск элемента с ожиданием"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator),
            f"Элемент {locator} не найден"
        )

    def find_elements(self, locator, timeout=10):
        """Поиск нескольких элементов"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )

    def click(self, locator, timeout=10):
        """Клик по элементу"""
        element = self.find_element(locator, timeout)
        element.click()
        time.sleep(1)

    def js_click(self, locator, timeout=10):
        """Клик через JavaScript (более надежно)"""
        element = self.find_element(locator, timeout)
        self.driver.execute_script("arguments[0].click();", element)
        time.sleep(1)

    def scroll_to_element(self, locator, timeout=10):
        """Скролл к элементу"""
        element = self.find_element(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(0.5)

    def get_text(self, locator, timeout=10) -> str:
        """Получение текста элемента"""
        element = self.find_element(locator, timeout)
        return element.text.strip()

    def wait_for_url_contains(self, text, timeout=10):
        """Ожидание, что URL содержит текст"""
        WebDriverWait(self.driver, timeout).until(
            EC.url_contains(text)
        )

    def wait_for_element_visible(self, locator, timeout=10):
        """Ожидание видимости элемента"""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def take_screenshot(self, name):
        """Сделать скриншот"""
        self.driver.save_screenshot(f"screenshots/{name}.png")