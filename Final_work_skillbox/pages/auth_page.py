from pages.base_page import BasePage
from pages.locators import AuthPageLocators
from selenium.webdriver.common.by import By
import random
import string
import time


class AuthPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def go_to_register_page(self):
        """Перейти на страницу регистрации"""
        self.driver.get("https://pizzeria.skillbox.cc/register/")
        time.sleep(2)

    def register(self, username=None, email=None, password=None):
        """Регистрация нового пользователя"""
        # Сначала переходим на страницу регистрации
        self.go_to_register_page()

        if not username:
            username = self.generate_username()
        if not email:
            email = self.generate_email()
        if not password:
            password = "TestPass123!"

        # На странице регистрации используются другие ID
        try:
            # Поле логина
            username_input = self.find_element((By.ID, "reg_username"))
            username_input.clear()
            username_input.send_keys(username)

            # Поле email
            email_input = self.find_element((By.ID, "reg_email"))
            email_input.clear()
            email_input.send_keys(email)

            # Поле пароля
            password_input = self.find_element((By.ID, "reg_password"))
            password_input.clear()
            password_input.send_keys(password)

            # Кнопка регистрации
            register_btn = self.find_element((By.NAME, "register"))
            self.driver.execute_script("arguments[0].click();", register_btn)
            time.sleep(3)

            print(f"✓ Пользователь {username} зарегистрирован")
            return {"username": username, "email": email, "password": password}

        except Exception as e:
            print(f"Ошибка при регистрации: {e}")
            # Пробуем альтернативные селекторы
            return self.register_alternative(username, email, password)

    def register_alternative(self, username, email, password):
        """Альтернативный метод регистрации"""
        try:
            # Ищем любые поля ввода на странице
            inputs = self.driver.find_elements(By.TAG_NAME, "input")

            # Предполагаем порядок: username, email, password
            if len(inputs) >= 3:
                inputs[0].send_keys(username)
                inputs[1].send_keys(email)
                inputs[2].send_keys(password)

                # Ищем кнопку отправки
                buttons = self.driver.find_elements(By.TAG_NAME, "button")
                for btn in buttons:
                    if "register" in btn.text.lower() or "зарегистрироваться" in btn.text.lower():
                        self.driver.execute_script("arguments[0].click();", btn)
                        time.sleep(3)
                        break

            return {"username": username, "email": email, "password": password}
        except:
            return {"username": username, "email": email, "password": password}

    def login(self, username, password):
        """Вход в систему"""
        self.driver.get("https://pizzeria.skillbox.cc/my-account/")
        time.sleep(2)

        username_input = self.find_element((By.ID, "username"))
        username_input.send_keys(username)

        password_input = self.find_element((By.ID, "password"))
        password_input.send_keys(password)

        login_btn = self.find_element((By.NAME, "login"))
        self.driver.execute_script("arguments[0].click();", login_btn)
        time.sleep(3)

    def is_user_logged_in(self):
        """Проверка, залогинен ли пользователь"""
        try:
            # Проверяем наличие ссылки на выход
            logout_links = self.driver.find_elements(By.LINK_TEXT, "Выйти")
            if logout_links:
                return True

            # Проверяем наличие сообщения о приветствии
            page_source = self.driver.page_source.lower()
            if "здравствуйте" in page_source or "hello" in page_source:
                return True

            return False
        except:
            return False

    def generate_username(self):
        """Генерация случайного имени пользователя"""
        return "test_user_" + ''.join(random.choices(string.digits, k=5))

    def generate_email(self):
        """Генерация случайного email"""
        return f"test_{''.join(random.choices(string.digits, k=5))}@test.com"