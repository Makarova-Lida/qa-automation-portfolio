from pages.base_page import BasePage
from pages.locators import MenuPageLocators, MainPageLocators
from selenium.webdriver.common.by import By
import time


class MenuPage(BasePage):
    """Страница меню"""

    def __init__(self, driver):
        super().__init__(driver)

    def open(self):
        """Открыть страницу меню"""
        self.driver.get("https://pizzeria.skillbox.cc/menu/")
        time.sleep(2)

    def select_category(self, category="desserts"):
        """Выбрать категорию товаров"""
        categories = {
            "pizza": (By.LINK_TEXT, "Пицца"),
            "desserts": (By.LINK_TEXT, "Десерты"),
            "drinks": (By.LINK_TEXT, "Напитки"),
        }

        if category in categories:
            try:
                # Пробуем найти по тексту ссылки
                elements = self.driver.find_elements(*categories[category])
                for element in elements:
                    if element.is_displayed():
                        self.driver.execute_script("arguments[0].click();", element)
                        time.sleep(3)
                        print(f"Выбрана категория: {category}")
                        return True

                # Если не нашли, пробуем через CSS
                css_selectors = {
                    "pizza": "a[href*='pizza']",
                    "desserts": "a[href*='dessert']",
                    "drinks": "a[href*='drink']",
                }

                elements = self.driver.find_elements(By.CSS_SELECTOR, css_selectors[category])
                if elements:
                    self.driver.execute_script("arguments[0].click();", elements[0])
                    time.sleep(3)
                    print(f"Выбрана категория через CSS: {category}")
                    return True

            except Exception as e:
                print(f"Ошибка выбора категории {category}: {e}")
                return False
        return False

    def get_products(self):
        """Получить список товаров на странице"""
        # Пробуем разные селекторы для товаров
        selectors = [
            MainPageLocators.PIZZA_CARDS,
            (By.CSS_SELECTOR, ".product"),
            (By.CSS_SELECTOR, ".type-product"),
            (By.CSS_SELECTOR, "li.product"),
        ]

        for selector in selectors:
            try:
                products = self.find_elements(selector, timeout=5)
                if products:
                    print(f"Найдено товаров по селектору {selector}: {len(products)}")
                    return products
            except:
                continue

        return []

    def get_products_count(self):
        """Получить количество товаров на странице"""
        products = self.get_products()
        return len(products)

    def filter_by_price(self, max_price=135):
        """Отфильтровать товары по максимальной цене"""
        try:
            # Пробуем найти фильтр цены на странице
            price_filters = [
                (By.CSS_SELECTOR, ".price_slider"),
                (By.CSS_SELECTOR, ".widget_price_filter"),
                (By.CSS_SELECTOR, ".price-filter")
            ]

            filter_found = False
            for selector in price_filters:
                try:
                    if self.driver.find_elements(*selector):
                        filter_found = True
                        print(f"Найден фильтр цены: {selector}")
                        break
                except:
                    continue

            if not filter_found:
                print("⚠ Фильтр по цене не найден на странице")
                return False

            # Пробуем установить максимальную цену через JavaScript
            # так как на сайте может быть слайдер
            try:
                # Устанавливаем значение через JS
                script = f"""
                var maxInput = document.querySelector('.price_slider_amount #max_price, .slider-input-max');
                if(maxInput) {{
                    maxInput.value = '{max_price}';
                    maxInput.dispatchEvent(new Event('change'));

                    // Нажимаем кнопку фильтра
                    var filterBtn = document.querySelector('.price_slider_amount button, button[type="submit"]');
                    if(filterBtn) filterBtn.click();
                }}
                """
                self.driver.execute_script(script)
                time.sleep(3)
                print(f"✓ Фильтр по цене {max_price}₽ применен")
                return True

            except Exception as e:
                print(f"Ошибка при установке фильтра: {e}")

                # Пробуем найти поля ввода цены
                try:
                    max_input = self.driver.find_element(By.CSS_SELECTOR, "#max_price, .slider-input-max")
                    max_input.clear()
                    max_input.send_keys(str(max_price))
                    time.sleep(1)

                    # Нажимаем кнопку фильтра
                    filter_btn = self.driver.find_element(By.CSS_SELECTOR, ".price_slider_amount button")
                    filter_btn.click()
                    time.sleep(3)
                    return True
                except:
                    pass

            return False

        except Exception as e:
            print(f"Ошибка фильтрации по цене: {e}")
            return False