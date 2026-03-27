# Оформление заказа
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.locators import CheckoutPageLocators
import time


class CheckoutPage(BasePage):
    """Страница оформления заказа"""

    def __init__(self, driver):
        super().__init__(driver)

    def apply_coupon(self, coupon_code):
        """Применить промокод"""
        try:
            # Ждем появления поля для промокода
            time.sleep(1)

            # Пробуем найти поле для промокода
            coupon_field = self.find_element((By.ID, "coupon_code"))

            # Скроллим к полю
            self.driver.execute_script("arguments[0].scrollIntoView(true);", coupon_field)
            time.sleep(1)

            # Очищаем поле и вводим промокод
            coupon_field.clear()
            coupon_field.send_keys(coupon_code)
            print(f"Промокод {coupon_code} введен")

            # Находим и нажимаем кнопку применения
            apply_button = self.find_element((By.NAME, "apply_coupon"))
            self.driver.execute_script("arguments[0].click();", apply_button)
            print("Кнопка применения нажата")

            time.sleep(2)
            return True
        except Exception as e:
            print(f"Ошибка применения промокода: {e}")
            return False

    def get_total_with_coupon(self):
        """Получить итоговую сумму с учетом скидки"""
        try:
            # Пробуем разные селекторы для итоговой суммы
            selectors = [
                (By.CSS_SELECTOR, ".order-total .woocommerce-Price-amount"),
                (By.CSS_SELECTOR, ".cart-subtotal .woocommerce-Price-amount"),
                (By.CSS_SELECTOR, ".amount"),
                (By.CSS_SELECTOR, ".price"),
            ]

            for selector in selectors:
                try:
                    elements = self.driver.find_elements(*selector)
                    if elements:
                        # Берем последний элемент (обычно это итоговая сумма)
                        total_element = elements[-1]
                        total_text = total_element.text.strip()
                        if total_text and total_text != "0":
                            print(f"Найдена сумма: {total_text} по селектору {selector}")
                            return total_text
                except:
                    continue

            # Если ничего не нашли, возвращаем 0
            print("Внимание: сумма не найдена на странице")
            return "0"
        except Exception as e:
            print(f"Ошибка получения суммы: {e}")
            return "0"

    def is_error_displayed(self):
        """Проверить, отображается ли сообщение об ошибке"""
        try:
            # Проверяем разные селекторы для сообщений об ошибке
            error_selectors = [
                (By.CSS_SELECTOR, ".woocommerce-error"),
                (By.CSS_SELECTOR, ".woocommerce-message"),
                (By.CSS_SELECTOR, ".woocommerce-info"),
                (By.XPATH, "//*[contains(text(), 'недействителен')]"),
                (By.XPATH, "//*[contains(text(), 'не существует')]"),
            ]

            for selector in error_selectors:
                try:
                    elements = self.driver.find_elements(*selector)
                    if elements:
                        print(f"Найдено сообщение: {elements[0].text[:100]}")
                        return True
                except:
                    continue

            return False
        except Exception as e:
            print(f"Ошибка проверки сообщения: {e}")
            return False

    def is_success_displayed(self):
        """Проверить, отображается ли сообщение об успехе"""
        try:
            success = self.find_element(CheckoutPageLocators.COUPON_SUCCESS, timeout=3)
            return success.is_displayed()
        except:
            return False

    def fill_billing_details(self, first_name="Тест", last_name="Тестов",
                             address="ул. Тестовая, д. 1", city="Москва",
                             phone="+79991234567", email="test@test.com"):
        """Заполнить платежные данные"""
        try:
            self.find_element(CheckoutPageLocators.BILLING_FIRST_NAME).send_keys(first_name)
            self.find_element(CheckoutPageLocators.BILLING_LAST_NAME).send_keys(last_name)
            self.find_element(CheckoutPageLocators.BILLING_ADDRESS_1).send_keys(address)
            self.find_element(CheckoutPageLocators.BILLING_CITY).send_keys(city)
            self.find_element(CheckoutPageLocators.BILLING_PHONE).send_keys(phone)
            self.find_element(CheckoutPageLocators.BILLING_EMAIL).send_keys(email)
            return True
        except Exception as e:
            print(f"Ошибка заполнения данных: {e}")
            return False

    def set_delivery_date(self, days_ahead=1):
        """Установить дату доставки (на days_ahead дней вперед)"""
        try:
            from datetime import datetime, timedelta
            delivery_date = (datetime.now() + timedelta(days=days_ahead)).strftime("%d.%m.%Y")
            date_field = self.find_element(CheckoutPageLocators.DELIVERY_DATE)
            date_field.clear()
            date_field.send_keys(delivery_date)
            return True
        except:
            # Если поля нет - пропускаем
            return False

    def select_payment_method(self, method="cash"):
        """Выбрать способ оплаты"""
        try:
            if method == "cash":
                self.click(CheckoutPageLocators.PAYMENT_METHOD_CASH)
            elif method == "card":
                self.click(CheckoutPageLocators.PAYMENT_METHOD_CARD)
            return True
        except:
            # Если нет радио-кнопок, может быть только один способ
            return False

    def place_order(self):
        """Подтвердить заказ"""
        try:
            # Принимаем условия
            try:
                self.click(CheckoutPageLocators.TERMS_CHECKBOX)
            except:
                pass

            # Отправляем заказ
            self.click(CheckoutPageLocators.PLACE_ORDER_BUTTON)
            time.sleep(3)
            return True
        except:
            return False

    def is_order_successful(self):
        """Проверить, успешно ли оформлен заказ"""
        try:
            self.find_element(CheckoutPageLocators.ORDER_RECEIVED, timeout=10)
            return True
        except:
            return False

    def get_order_number(self):
        """Получить номер заказа"""
        try:
            return self.get_text(CheckoutPageLocators.ORDER_NUMBER)
        except:
            return ""

    def get_order_total(self):
        """Получить итоговую сумму заказа"""
        try:
            return self.get_text(CheckoutPageLocators.ORDER_TOTAL)
        except:
            return ""

    def verify_order_details(self):
        """Проверить детали заказа"""
        result = {
            "order_number": self.get_order_number(),
            "order_total": self.get_order_total(),
            "has_items": False
        }

        # Проверяем наличие товаров
        try:
            items = self.find_elements(CheckoutPageLocators.ORDER_ITEMS)
            result["has_items"] = len(items) > 0
            result["items_count"] = len(items)
        except:
            result["has_items"] = False
            result["items_count"] = 0

        return result