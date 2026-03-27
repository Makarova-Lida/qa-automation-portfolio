import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class TestSimple:
    """Простые тесты для проверки работоспособности"""

    def test_site_opens(self, driver, base_url):
        """Проверка открытия сайта"""
        driver.get(base_url)
        time.sleep(2)

        # Проверяем заголовок
        title = driver.title
        print(f"Заголовок сайта: {title}")
        assert "Pizzeria" in title or "Пиццерия" in title, "Неверный заголовок"

        # Проверяем, что есть товары
        products = driver.find_elements(By.CSS_SELECTOR, "#product1 .span3")
        print(f"Найдено товаров: {len(products)}")
        assert len(products) > 0, "Нет товаров на странице"

    def test_add_to_cart(self, driver, base_url):
        """Проверка добавления в корзину"""
        driver.get(base_url)
        time.sleep(2)

        # Находим первую кнопку "В корзину"
        add_buttons = driver.find_elements(By.CSS_SELECTOR, ".add_to_cart_button")
        assert len(add_buttons) > 0, "Нет кнопок добавления"

        # Запоминаем текст корзины до клика
        cart_before = driver.find_element(By.CSS_SELECTOR, "a.cart-contents").text

        # Кликаем на первую кнопку
        driver.execute_script("arguments[0].click();", add_buttons[0])
        time.sleep(2)

        # Проверяем, что корзина изменилась
        cart_after = driver.find_element(By.CSS_SELECTOR, "a.cart-contents").text
        assert cart_before != cart_after, "Корзина не изменилась"
        print(f"Корзина до: {cart_before}, после: {cart_after}")

    def test_go_to_cart(self, driver, base_url):
        """Проверка перехода в корзину"""
        driver.get(base_url)
        time.sleep(2)

        # Кликаем на корзину
        cart_link = driver.find_element(By.CSS_SELECTOR, "a.cart-contents")
        cart_link.click()
        time.sleep(2)

        # Проверяем URL
        assert "cart" in driver.current_url or "checkout" in driver.current_url, \
            f"Не перешли в корзину: {driver.current_url}"
        print(f"URL после клика: {driver.current_url}")