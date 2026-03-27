from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import time


class PizzaDetailPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def get_pizza_name(self):
        """Получить название пиццы"""
        return self.get_text((By.CSS_SELECTOR, ".product_title"))

    def get_pizza_price(self):
        """Получить цену пиццы"""
        return self.get_text((By.CSS_SELECTOR, ".price .woocommerce-Price-amount"))

    def add_to_cart(self):
        """Добавить пиццу в корзину со страницы деталей"""
        try:
            add_button = self.find_element((By.CSS_SELECTOR, ".single_add_to_cart_button"))
            self.driver.execute_script("arguments[0].click();", add_button)
            time.sleep(2)
            return True
        except Exception as e:
            print(f"Ошибка при добавлении в корзину: {e}")
            return False

    def select_option(self, option_text):
        """Выбрать дополнительную опцию (бортик)"""
        try:
            # Ищем радио-кнопки или чекбоксы с нужным текстом
            options = self.driver.find_elements(By.CSS_SELECTOR, ".variations input, .variations select")
            for opt in options:
                parent = opt.find_element(By.XPATH, "..")
                if option_text.lower() in parent.text.lower():
                    self.driver.execute_script("arguments[0].click();", opt)
                    time.sleep(1)
                    return True
        except Exception as e:
            print(f"Ошибка при выборе опции: {e}")
        return False

    def set_quantity(self, quantity):
        """Установить количество"""
        try:
            qty_input = self.find_element((By.CSS_SELECTOR, ".quantity input"))
            qty_input.clear()
            qty_input.send_keys(str(quantity))
            time.sleep(1)
            return True
        except:
            return False