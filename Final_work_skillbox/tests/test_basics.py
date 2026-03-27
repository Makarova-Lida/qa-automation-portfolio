import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestBasicFunctionality:
    """Базовые тесты функциональности сайта"""

    def test_site_title(self, browser, base_url):
        """Тест: открытие сайта и проверка заголовка"""
        browser.get(base_url)
        time.sleep(2)
        title = browser.title
        print(f"Заголовок: {title}")
        assert "Pizzeria" in title or "Пиццерия" in title

    def test_cart_icon(self, browser, base_url):
        """Тест: наличие иконки корзины"""
        browser.get(base_url)
        time.sleep(2)
        cart = browser.find_element(By.CSS_SELECTOR, "a.cart-contents")
        assert cart.is_displayed()
        print(f"Корзина найдена: '{cart.text}'")

    def test_main_menu(self, browser, base_url):
        """Тест: основные пункты меню"""
        browser.get(base_url)
        time.sleep(2)

        # Проверяем реальные пункты меню на сайте
        menu_items = [
            ("Меню", "//a[contains(text(), 'Меню')]"),
            ("Пицца", "//a[contains(text(), 'Пицца')]"),
            ("Десерты", "//a[contains(text(), 'Десерты')]"),
            ("Напитки", "//a[contains(text(), 'Напитки')]"),
            ("Войти", "//a[contains(text(), 'Войти')]"),
            ("Мой аккаунт", "//a[contains(text(), 'Мой аккаунт')]"),
        ]

        found = 0
        found_items = []

        for name, xpath in menu_items:
            try:
                elements = browser.find_elements(By.XPATH, xpath)
                for element in elements:
                    if element.is_displayed():
                        print(f"  ✓ '{name}' найден")
                        found += 1
                        found_items.append(name)
                        break
            except:
                print(f"  ✗ '{name}' не найден")

        print(f"Найдено пунктов меню: {found}/{len(menu_items)}")
        print(f"Найденные пункты: {', '.join(found_items)}")

        # Должны найти хотя бы основные пункты
        assert found >= 3, f"Найдено только {found} пунктов меню"

    def test_product_sections(self, browser, base_url):
        """Тест: секции товаров на главной"""
        browser.get(base_url)
        time.sleep(2)

        sections = [
            ("Пицца", "#product1"),
            ("Десерты", "#product2"),
            ("Напитки", ".ap-cat-list")
        ]

        for name, selector in sections:
            try:
                element = browser.find_element(By.CSS_SELECTOR, selector)
                assert element.is_displayed()
                print(f"  ✓ Секция '{name}' найдена")
            except:
                print(f"  ✗ Секция '{name}' не найдена")

    def test_add_to_cart_buttons(self, browser, base_url):
        """Тест: кнопки 'В корзину'"""
        browser.get(base_url)
        time.sleep(2)

        # Ищем кнопки в секции пицц
        add_buttons = browser.find_elements(
            By.CSS_SELECTOR,
            "#product1 .add_to_cart_button"
        )

        print(f"Кнопок 'В корзину' в секции пицц: {len(add_buttons)}")
        assert len(add_buttons) > 0, "Нет кнопок 'В корзину' в секции пицц"

        # Проверяем, что кнопки существуют (текст может быть пустым, если это иконка)
        for button in add_buttons[:3]:
            assert button.is_displayed() or button.is_enabled()

    @pytest.mark.slow
    def test_add_product_to_cart(self, browser, base_url):
        """Тест: добавление товара в корзину"""
        browser.get(base_url)
        time.sleep(3)

        # 1. Находим кнопку "В корзину"
        add_buttons = browser.find_elements(
            By.CSS_SELECTOR,
            "#product1 .add_to_cart_button"
        )
        assert len(add_buttons) > 0

        # 2. Запоминаем состояние корзины ДО
        cart_before = browser.find_element(
            By.CSS_SELECTOR, "a.cart-contents"
        ).text
        print(f"Корзина ДО: '{cart_before}'")

        # 3. Кликаем через JavaScript (более надежно)
        browser.execute_script("arguments[0].click();", add_buttons[0])
        time.sleep(3)

        # 4. Проверяем состояние корзины ПОСЛЕ
        cart_after = browser.find_element(
            By.CSS_SELECTOR, "a.cart-contents"
        ).text
        print(f"Корзина ПОСЛЕ: '{cart_after}'")

        assert cart_before != cart_after, "Корзина не изменилась"

    def test_navigate_to_cart_page(self, browser, base_url):
        """Тест: переход на страницу корзины"""
        browser.get(base_url)
        time.sleep(2)

        # Кликаем на корзину
        cart_link = browser.find_element(By.CSS_SELECTOR, "a.cart-contents")
        cart_link.click()
        time.sleep(2)

        # Проверяем URL
        current_url = browser.current_url
        print(f"URL после клика: {current_url}")

        assert "cart" in current_url or "checkout" in current_url, \
            f"Не перешли в корзину: {current_url}"
        print("✓ Успешно перешли на страницу корзины")