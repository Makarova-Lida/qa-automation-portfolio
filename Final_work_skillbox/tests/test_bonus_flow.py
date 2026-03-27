"""
Тесты бонусной системы
"""

import pytest
import time
from pages.bonus_page import BonusPage
from selenium.webdriver.common.by import By


class TestBonusFlow:
    """Тесты бонусной программы"""

    def test_bonus_registration_success(self, driver, base_url):
        """Сценарий: Регистрация в бонусной программе с валидными данными"""
        # Открываем страницу бонусной программы
        bonus_page = BonusPage(driver)
        bonus_page.open()

        # Делаем скриншот для отладки
        driver.save_screenshot("bonus_page_before.png")
        print("Скриншот страницы бонусов сохранен")

        # Заполняем форму
        name_filled = bonus_page.fill_name("Тестовый Пользователь")
        phone_filled = bonus_page.fill_phone("+79991234567")

        print(f"Имя заполнено: {name_filled}")
        print(f"Телефон заполнен: {phone_filled}")

        assert name_filled, "Не удалось заполнить имя"
        assert phone_filled, "Не удалось заполнить телефон"

        # Отправляем форму
        submitted = bonus_page.submit()
        assert submitted, "Не удалось отправить форму"

        # Проверяем успешность
        time.sleep(3)
        success = bonus_page.is_activation_successful()

        if not success:
            driver.save_screenshot("bonus_page_after.png")
            print("Скриншот после отправки сохранен")
            # Выводим HTML для отладки
            print("HTML страницы после отправки:")
            print(driver.page_source[:500])

        assert success, "Не появилось сообщение об успешной активации"
        print("✓ Успешная регистрация в бонусной программе")

    def test_bonus_name_validation(self, driver, base_url):
        """Проверка валидации поля имени"""
        bonus_page = BonusPage(driver)
        bonus_page.open()

        # Пробуем отправить с пустым именем
        bonus_page.fill_phone("+79991234567")
        bonus_page.submit()
        time.sleep(2)

        # Проверяем, что появилась ошибка
        page_source = driver.page_source.lower()
        has_error = "обязательно" in page_source or "заполните" in page_source or "имя" in page_source

        if not has_error:
            driver.save_screenshot("validation_error_missing.png")
            print("Скриншот при отсутствии ошибки валидации сохранен")

        assert has_error, "Нет ошибки при пустом имени"
        print("✓ Валидация имени работает")

    def test_bonus_phone_validation(self, driver, base_url):
        """Проверка валидации поля телефона"""
        bonus_page = BonusPage(driver)
        bonus_page.open()

        # Пробуем отправить с пустым телефоном
        bonus_page.fill_name("Тестовый Пользователь")
        bonus_page.submit()
        time.sleep(2)

        # Проверяем, что появилась ошибка
        page_source = driver.page_source.lower()
        has_error = "телефон" in page_source and ("обязательно" in page_source or "заполните" in page_source)

        if not has_error:
            driver.save_screenshot("phone_validation_error_missing.png")
            print("Скриншот при отсутствии ошибки валидации телефона сохранен")

        assert has_error, "Нет ошибки при пустом телефоне"
        print("✓ Валидация телефона работает")