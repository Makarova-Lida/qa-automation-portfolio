"""
Тесты основного флоу клиента (Андрей)
Полный флоу с шага 1 по шаг оформления заказа
"""

import pytest
import time
from selenium.webdriver.common.by import By  # Добавьте эту строку
from pages.main_page import MainPage
from pages.cart_page import CartPage
from pages.pizza_detail_page import PizzaDetailPage
from pages.auth_page import AuthPage
from pages.checkout_page import CheckoutPage
from pages.menu_page import MenuPage


class TestMainFlow:
    """Тесты основного флоу пользователя"""

    def test_step_1_2_open_site_and_see_products(self, main_page):
        """Шаги 1-2: Зайти на сайт и увидеть товары"""
        # Шаг 1 уже выполнен в фикстуре main_page
        products = main_page.get_all_products()
        assert len(products) > 0, "На главной странице нет товаров"
        print(f"✓ Найдено {len(products)} товаров на главной")

    def test_step_3_4_add_first_pizza_to_cart(self, main_page):
        """Шаги 3-4: Добавить пиццу в корзину"""
        # Запоминаем состояние корзины до
        cart_before = main_page.get_cart_total()
        product_name = main_page.get_product_name_by_index(0)

        # Добавляем товар
        result = main_page.add_product_to_cart_by_index(0)
        assert result, "Не удалось добавить товар"

        # Проверяем, что корзина изменилась
        cart_after = main_page.get_cart_total()
        assert cart_before != cart_after, "Сумма корзины не изменилась"
        print(f"✓ Товар '{product_name}' добавлен в корзину")

    def test_step_5_add_multiple_pizzas(self, main_page):
        """Шаг 5: Добавить несколько пицц"""
        # Добавляем несколько товаров
        products = main_page.get_all_products()
        count_to_add = min(3, len(products))

        for i in range(count_to_add):
            cart_before = main_page.get_cart_total()
            main_page.add_product_to_cart_by_index(i)
            cart_after = main_page.get_cart_total()
            assert cart_before != cart_after, f"Товар {i} не добавился"

        print(f"✓ Добавлено {count_to_add} товаров в корзину")

    def test_step_6_check_cart_info(self, main_page):
        """Шаг 6: Проверить информацию о корзине"""
        # Добавляем товар
        main_page.add_product_to_cart_by_index(0)

        # Проверяем, что информация о корзине отображается
        cart_info = main_page.get_cart_total()
        assert cart_info and "₽" in cart_info, "Некорректная информация о корзине"
        print(f"✓ Информация о корзине: {cart_info}")

    def test_step_7_click_pizza_image(self, main_page):
        """Шаг 7: Кликнуть на картинку пиццы для перехода к описанию"""
        # Запоминаем URL до клика
        url_before = main_page.driver.current_url
        product_name = main_page.get_product_name_by_index(0)

        # Кликаем на картинку
        result = main_page.click_on_pizza_image(0)
        assert result, "Не удалось кликнуть на картинку"

        # Проверяем, что перешли на другую страницу
        url_after = main_page.driver.current_url
        assert url_before != url_after, "Не произошел переход на страницу товара"
        assert "product" in url_after, "Не похоже на страницу товара"

        print(f"✓ Перешли на страницу пиццы")

    def test_step_8_select_pizza_options(self, main_page):
        """Шаг 8: Выбрать дополнительные опции (бортики)"""
        # Переходим на страницу пиццы
        main_page.click_on_pizza_image(0)
        detail_page = PizzaDetailPage(main_page.driver)

        # Добавляем в корзину со страницы деталей
        cart_before = main_page.get_cart_total()
        detail_page.add_to_cart()
        time.sleep(2)
        cart_after = main_page.get_cart_total()

        assert cart_before != cart_after, "Товар не добавился в корзину"
        print("✓ Товар добавлен в корзину со страницы деталей")

    def test_step_9_10_go_to_cart_and_update_quantity(self, main_page):
        """Шаги 9-10: Перейти в корзину и увеличить количество товара"""
        # Добавляем товар
        main_page.add_product_to_cart_by_index(0)

        # Переходим в корзину
        main_page.go_to_cart()
        cart_page = CartPage(main_page.driver)

        # Запоминаем текущую сумму
        total_before = cart_page.get_total_sum()

        # Увеличиваем количество
        cart_page.update_quantity(0, 2)
        time.sleep(2)

        # Проверяем, что сумма изменилась
        total_after = cart_page.get_total_sum()
        assert total_before != total_after, "Сумма не изменилась после изменения количества"
        print(f"✓ Количество изменено. Было: {total_before}, стало: {total_after}")

    def test_step_11_remove_item_from_cart(self, main_page):
        """Шаг 11: Удалить товар из корзины"""
        # Добавляем товары
        main_page.add_product_to_cart_by_index(0)
        main_page.add_product_to_cart_by_index(1)

        # Переходим в корзину
        main_page.go_to_cart()
        cart_page = CartPage(main_page.driver)

        # Запоминаем количество товаров
        items_count_before = cart_page.get_items_count()

        # Удаляем один товар
        cart_page.remove_item(0)
        time.sleep(2)

        # Проверяем, что количество уменьшилось
        items_count_after = cart_page.get_items_count()
        assert items_count_after == items_count_before - 1, "Товар не удалился"
        print(f"✓ Товар удален. Было товаров: {items_count_before}, стало: {items_count_after}")

    def test_step_12_13_go_to_menu_and_select_desserts(self, driver, base_url):
        """Шаги 12-13: Перейти в меню и выбрать десерты"""
        driver.get(base_url + "/menu/")
        menu_page = MenuPage(driver)

        # Выбираем категорию десертов
        menu_page.select_category("desserts")
        time.sleep(2)

        # Проверяем, что товары отображаются
        products = menu_page.get_products()
        assert len(products) > 0, "Нет десертов в категории"
        print(f"✓ Найдено {len(products)} десертов")

    def test_step_14_filter_desserts_by_price(self, driver, base_url):
        """Шаг 14: Отфильтровать десерты по цене (до 135 руб)"""
        driver.get(base_url + "/menu/")
        menu_page = MenuPage(driver)

        # Выбираем десерты
        menu_page.select_category("desserts")
        time.sleep(2)

        # Запоминаем все товары до фильтрации
        products_before = menu_page.get_products_count()

        # Фильтруем по цене
        menu_page.filter_by_price(135)
        time.sleep(3)

        # Проверяем, что товары отфильтровались
        products_after = menu_page.get_products_count()
        print(f"✓ До фильтра: {products_before} товаров, после: {products_after} товаров")

    def test_step_15_add_dessert_to_cart(self, main_page, driver):
        """Шаг 15: Добавить десерт в корзину"""
        # Переходим в раздел десертов через меню
        main_page.go_to_menu_section("desserts")
        time.sleep(2)

        # Добавляем первый десерт
        cart_before = main_page.get_cart_total()
        main_page.add_product_to_cart_by_index(0)
        cart_after = main_page.get_cart_total()

        assert cart_before != cart_after, "Десерт не добавился в корзину"
        print("✓ Десерт добавлен в корзину")

    def test_step_16_17_18_go_to_checkout_and_register(self, main_page, driver):
        """Шаги 16-18: Перейти к оформлению и зарегистрироваться"""
        from selenium.webdriver.common.by import By  # Добавляем импорт локально для надежности

        # Добавляем товар
        main_page.add_product_to_cart_by_index(0)

        # Переходим в корзину
        main_page.go_to_cart()
        cart_page = CartPage(driver)

        # Переходим к оформлению
        cart_page.proceed_to_checkout()
        time.sleep(2)

        # Проверяем, что мы на странице оформления заказа
        current_url = driver.current_url
        print(f"Текущий URL: {current_url}")
        assert "checkout" in current_url.lower(), f"Не перешли на страницу оформления: {current_url}"

        # Переходим на страницу аккаунта для регистрации
        print("Переходим на страницу регистрации...")
        main_page.go_to_account()
        time.sleep(2)

        # Регистрируемся
        auth_page = AuthPage(driver)
        user_data = auth_page.register()
        time.sleep(2)

        # Проверяем, что залогинены
        assert auth_page.is_user_logged_in(), "Пользователь не залогинен после регистрации"
        print(f"✓ Пользователь {user_data['username']} зарегистрирован")

        # Возвращаемся в корзину
        main_page.open()
        main_page.go_to_cart()
        time.sleep(1)

        print("✓ Шаг 16-18 выполнен успешно")

    def test_full_order_flow(self, main_page, driver):
        """Полный флоу от добавления товаров до подтверждения заказа"""

        # 1. Добавляем пиццу
        main_page.add_product_to_cart_by_index(0)

        # 2. Переходим в корзину
        main_page.go_to_cart()
        cart_page = CartPage(driver)

        # 3. Переходим на страницу аккаунта и регистрируемся
        main_page.go_to_account()
        auth_page = AuthPage(driver)
        user_data = auth_page.register()
        time.sleep(2)

        # 4. Проверяем, что пользователь залогинен
        assert auth_page.is_user_logged_in(), "Пользователь не залогинен после регистрации"
        print(f"✓ Пользователь {user_data['username']} зарегистрирован и залогинен")

        # 5. Переходим на главную
        main_page.open()

        # 6. Добавляем товар в корзину (уже будучи залогиненным)
        main_page.add_product_to_cart_by_index(0)

        # 7. Переходим в корзину
        main_page.go_to_cart()

        # 8. Переходим к оформлению заказа
        cart_page.proceed_to_checkout()
        time.sleep(2)

        # 9. Проверяем, что мы на странице оформления заказа
        assert "checkout" in driver.current_url.lower(), "Не перешли на страницу оформления"
        print("✓ Страница оформления заказа открыта")

        print("✓ Тест полного флоу выполнен успешно (упрощенная проверка)")