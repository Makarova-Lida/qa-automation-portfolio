from pages.base_page import BasePage
from pages.locators import CartPageLocators
from selenium.webdriver.common.by import By
import time


class CartPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def get_items_count(self):
        """Получить количество товаров в корзине"""
        items = self.find_elements(CartPageLocators.CART_ITEMS)
        return len(items)

    def get_item_names(self):
        """Получить названия товаров в корзине"""
        items = self.find_elements(CartPageLocators.CART_ITEMS)
        names = []
        for item in items:
            try:
                name_elem = item.find_element(*CartPageLocators.ITEM_NAME)
                names.append(name_elem.text.strip())
            except:
                names.append("Неизвестный товар")
        return names

    def get_total_sum(self):
        """Получить общую сумму корзины"""
        try:
            total_text = self.get_text(CartPageLocators.CART_TOTAL)
            return total_text.strip()
        except:
            return "0,00₽"

    def proceed_to_checkout(self):
        """Перейти к оформлению заказа"""
        try:
            self.click(CartPageLocators.PROCEED_TO_CHECKOUT)
            return True
        except:
            return False

    def update_quantity(self, item_index=0, quantity=2):
        """Изменить количество товара"""
        items = self.find_elements(CartPageLocators.CART_ITEMS)
        if item_index < len(items):
            item = items[item_index]
            try:
                quantity_input = item.find_element(By.CSS_SELECTOR, "input.qty")
                quantity_input.clear()
                quantity_input.send_keys(str(quantity))

                # Нажимаем кнопку обновления корзины
                update_button = self.driver.find_element(By.NAME, "update_cart")
                self.driver.execute_script("arguments[0].click();", update_button)
                time.sleep(3)
                return True
            except Exception as e:
                print(f"Ошибка при обновлении количества: {e}")
                return False
        return False

    def remove_item(self, item_index=0):
        """Удалить товар из корзины"""
        items = self.find_elements(CartPageLocators.CART_ITEMS)
        if item_index < len(items):
            item = items[item_index]
            try:
                remove_link = item.find_element(By.CSS_SELECTOR, "a.remove")
                self.driver.execute_script("arguments[0].click();", remove_link)
                time.sleep(3)
                return True
            except Exception as e:
                print(f"Ошибка при удалении товара: {e}")
                return False
        return False

    def is_empty(self):
        """Проверить, пуста ли корзина"""
        try:
            empty_msg = self.find_element(CartPageLocators.EMPTY_CART_MESSAGE, timeout=3)
            return empty_msg.is_displayed()
        except:
            return False