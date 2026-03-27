from pages.base_page import BasePage
from pages.locators import MainPageLocators
import random
import time
from selenium.webdriver.common.by import By


class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://pizzeria.skillbox.cc/"

    def open(self):
        """Открыть главную страницу"""
        self.driver.get(self.url)
        time.sleep(1)

    def get_all_products(self):
        """Получить все карточки товаров"""
        return self.find_elements(MainPageLocators.PIZZA_CARDS)

    def add_product_to_cart_by_index(self, index=0):
        """Добавить товар в корзину по индексу"""
        products = self.get_all_products()
        if index < len(products):
            product = products[index]
            try:
                # Находим кнопку добавления внутри карточки товара
                add_button = product.find_element(*MainPageLocators.ADD_TO_CART_BUTTONS)
                # Кликаем через JavaScript
                self.driver.execute_script("arguments[0].click();", add_button)
                time.sleep(2)  # Ждем обновления корзины
                return True
            except Exception as e:
                print(f"Ошибка при добавлении товара: {e}")
                return False
        return False

    def get_product_name_by_index(self, index=0):
        """Получить название товара по индексу"""
        products = self.get_all_products()
        if index < len(products):
            try:
                name_element = products[index].find_element(*MainPageLocators.PIZZA_NAMES)
                return name_element.text.strip()
            except:
                return "Товар без названия"
        return ""

    def get_cart_total(self):
        """Получить сумму в корзине"""
        try:
            cart_element = self.find_element(MainPageLocators.CART_ICON)
            return cart_element.text.strip()
        except:
            return "0,00₽"

    def go_to_cart(self):
        """Перейти в корзину"""
        try:
            cart_link = self.find_element(MainPageLocators.CART_ICON)
            cart_link.click()
            time.sleep(2)
            return True
        except:
            return False

    def go_to_account(self):
        """Перейти в личный кабинет"""
        try:
            account_link = self.find_element(MainPageLocators.ACCOUNT_LINK)
            account_link.click()
            time.sleep(2)
            return True
        except:
            return False

    def go_to_menu_section(self, section="pizza"):
        """Перейти в раздел меню"""
        sections = {
            "pizza": MainPageLocators.PIZZA_LINK,
            "desserts": MainPageLocators.DESSERTS_LINK,
            "drinks": MainPageLocators.DRINKS_LINK
        }
        if section in sections:
            try:
                self.click(sections[section])
                time.sleep(2)
                return True
            except:
                return False
        return False

    def click_on_pizza_image(self, index=0):
        """Клик на картинку пиццы для перехода к деталям"""
        products = self.get_all_products()
        if index < len(products):
            product = products[index]
            try:
                # Пробуем разные способы найти ссылку на товар
                selectors = [
                    "a.woocommerce-LoopProduct-link",
                    "h3 a",
                    ".product-images a",
                    "a[href*='product']"
                ]

                for selector in selectors:
                    try:
                        img_link = product.find_element(By.CSS_SELECTOR, selector)
                        # Запоминаем URL до клика
                        url_before = self.driver.current_url

                        # Кликаем через JavaScript
                        self.driver.execute_script("arguments[0].click();", img_link)
                        time.sleep(3)

                        # Проверяем, что URL изменился
                        if self.driver.current_url != url_before:
                            return True
                    except:
                        continue

                # Если не нашли по селекторам, пробуем кликнуть по изображению
                try:
                    img = product.find_element(By.CSS_SELECTOR, "img")
                    self.driver.execute_script("arguments[0].click();", img)
                    time.sleep(3)
                    return True
                except:
                    pass

                return False
            except Exception as e:
                print(f"Ошибка при клике на картинку: {e}")
                return False
        return False

    def add_random_products(self, count=2):
        """Добавить случайные товары в корзину"""
        products = self.get_all_products()
        if len(products) < count:
            count = len(products)

        if count == 0:
            return []

        indices = random.sample(range(len(products)), min(count, len(products)))
        added = []

        for idx in indices:
            name = self.get_product_name_by_index(idx)
            if self.add_product_to_cart_by_index(idx):
                added.append(name)
                time.sleep(1)

        return added