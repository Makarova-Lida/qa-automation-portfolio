from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import time


class BonusPage(BasePage):
    """Страница бонусной программы"""

    def __init__(self, driver):
        super().__init__(driver)

    def open(self):
        """Открыть страницу бонусной программы"""
        self.driver.get("https://pizzeria.skillbox.cc/bonus/")
        time.sleep(2)

    def fill_name(self, name):
        """Заполнить поле имени"""
        try:
            name_input = self.find_element((By.ID, "bonus_username"))
            name_input.clear()
            name_input.send_keys(name)
            print(f"Имя '{name}' заполнено")
            return True
        except Exception as e:
            print(f"Ошибка заполнения имени: {e}")
            return False

    def fill_phone(self, phone):
        """Заполнить поле телефона"""
        try:
            phone_input = self.find_element((By.ID, "bonus_phone"))
            phone_input.clear()
            phone_input.send_keys(phone)
            print(f"Телефон '{phone}' заполнен")
            return True
        except Exception as e:
            print(f"Ошибка заполнения телефона: {e}")
            return False

    def submit(self):
        """Отправить форму через JavaScript функцию на странице"""
        try:
            # Вызываем функцию loader() через JavaScript
            self.driver.execute_script("loader();")
            print("✓ Функция loader() вызвана")

            # Ждем появления alert
            time.sleep(1)

            # Переключаемся на alert и принимаем его
            try:
                alert = self.driver.switch_to.alert
                alert_text = alert.text
                print(f"✓ Появился alert: {alert_text}")
                alert.accept()
                print("✓ Alert принят")
                time.sleep(6)  # Ждем появления сообщения об успехе
            except:
                print("⚠ Alert не появился")

            # Проверяем результат
            page_source = self.driver.page_source
            if "Ваша карта оформлена!" in page_source:
                print("✓ Карта успешно оформлена!")
                return True
            else:
                # Проверяем сообщения об ошибках
                error_selectors = [
                    "//*[contains(text(), 'обязательно для заполнения')]",
                    "//*[contains(text(), 'неверный формат телефона')]"
                ]

                for selector in error_selectors:
                    try:
                        error = self.driver.find_element(By.XPATH, selector)
                        print(f"⚠ Ошибка валидации: {error.text}")
                        return False
                    except:
                        continue

                print("⚠ Неизвестный результат")
                return False

        except Exception as e:
            print(f"✗ Ошибка при вызове функции: {e}")
            return False

    def is_activation_successful(self):
        """Проверить успешность активации"""
        try:
            page_source = self.driver.page_source
            if "Ваша карта оформлена!" in page_source:
                print("✓ Найдено сообщение об успехе")
                return True
            return False
        except Exception as e:
            print(f"Ошибка проверки успешности: {e}")
            return False

    def get_error_message(self):
        """Получить сообщение об ошибке"""
        try:
            error = self.driver.find_element(By.ID, "bonus_content")
            if error.text:
                return error.text
        except:
            pass
        return ""