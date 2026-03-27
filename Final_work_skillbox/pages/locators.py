from selenium.webdriver.common.by import By


class MainPageLocators:
    """Локаторы главной страницы (на основе работающих тестов)"""

    # Корзина
    CART_ICON = (By.CSS_SELECTOR, "a.cart-contents")
    CART_TEXT = (By.CSS_SELECTOR, "a.cart-contents")

    # Меню
    MENU_LINK = (By.XPATH, "//a[contains(text(), 'Меню')]")
    PIZZA_LINK = (By.XPATH, "//a[contains(text(), 'Пицца')]")
    DESSERTS_LINK = (By.XPATH, "//a[contains(text(), 'Десерты')]")
    DRINKS_LINK = (By.XPATH, "//a[contains(text(), 'Напитки')]")
    LOGIN_LINK = (By.XPATH, "//a[contains(text(), 'Войти')]")
    ACCOUNT_LINK = (By.XPATH, "//a[contains(text(), 'Мой аккаунт')]")

    # Секции товаров
    PIZZA_SECTION = (By.ID, "product1")
    DESSERTS_SECTION = (By.ID, "product2")
    DRINKS_SECTION = (By.CSS_SELECTOR, ".ap-cat-list")

    # Заголовки секций
    PIZZA_TITLE = (By.XPATH, "//h2[contains(@class, 'prod-title') and contains(text(), 'Пицца')]")
    DESSERTS_TITLE = (By.XPATH, "//h2[contains(@class, 'prod-title') and contains(text(), 'Десерты')]")
    DRINKS_TITLE = (By.XPATH, "//h2[contains(@class, 'prod-title') and contains(text(), 'Напитки')]")

    # Кнопки "В корзину"
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "#product1 .add_to_cart_button")
    ALL_ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, ".add_to_cart_button")

    # Карточки товаров
    PIZZA_CARDS = (By.CSS_SELECTOR, "#product1 .span3")
    PIZZA_NAMES = (By.CSS_SELECTOR, "#product1 h3")
    PIZZA_PRICES = (By.CSS_SELECTOR, "#product1 .price .woocommerce-Price-amount")

    # Слайдер
    SLIDER_NEXT = (By.CSS_SELECTOR, ".bx-next")
    SLIDER_PREV = (By.CSS_SELECTOR, ".bx-prev")
    SLIDER_PAGINATION = (By.CSS_SELECTOR, ".bx-pager-link")


class CartPageLocators:
    """Локаторы страницы корзины"""
    CART_ITEMS = (By.CSS_SELECTOR, ".cart_item")
    ITEM_NAME = (By.CSS_SELECTOR, ".product-name a")
    ITEM_PRICE = (By.CSS_SELECTOR, ".product-price .woocommerce-Price-amount")
    ITEM_QUANTITY = (By.CSS_SELECTOR, ".product-quantity input.qty")
    ITEM_SUBTOTAL = (By.CSS_SELECTOR, ".product-subtotal .woocommerce-Price-amount")
    CART_SUBTOTAL = (By.CSS_SELECTOR, ".cart-subtotal .woocommerce-Price-amount")
    CART_TOTAL = (By.CSS_SELECTOR, ".order-total .woocommerce-Price-amount")
    PROCEED_TO_CHECKOUT = (By.CSS_SELECTOR, ".checkout-button")
    UPDATE_CART = (By.NAME, "update_cart")
    REMOVE_ITEM = (By.CSS_SELECTOR, "a.remove")
    COUPON_CODE = (By.ID, "coupon_code")
    APPLY_COUPON = (By.NAME, "apply_coupon")
    EMPTY_CART_MESSAGE = (By.CSS_SELECTOR, ".cart-empty")


class AuthPageLocators:
    """Локаторы страницы авторизации"""
    # Вход
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.NAME, "login")
    REMEMBER_ME = (By.ID, "rememberme")

    # Регистрация
    REGISTER_USERNAME = (By.ID, "reg_username")
    REGISTER_EMAIL = (By.ID, "reg_email")
    REGISTER_PASSWORD = (By.ID, "reg_password")
    REGISTER_BUTTON = (By.NAME, "register")

    # Статус
    LOGOUT_LINK = (By.LINK_TEXT, "Выйти")
    ACCOUNT_DETAILS = (By.LINK_TEXT, "Детали аккаунта")
    ORDERS_LINK = (By.LINK_TEXT, "Заказы")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".woocommerce-error")


class CheckoutPageLocators:
    """Локаторы страницы оформления заказа"""

    # Поля для заполнения
    BILLING_FIRST_NAME = (By.ID, "billing_first_name")
    BILLING_LAST_NAME = (By.ID, "billing_last_name")
    BILLING_COMPANY = (By.ID, "billing_company")
    BILLING_COUNTRY = (By.ID, "billing_country")
    BILLING_ADDRESS_1 = (By.ID, "billing_address_1")
    BILLING_ADDRESS_2 = (By.ID, "billing_address_2")
    BILLING_CITY = (By.ID, "billing_city")
    BILLING_STATE = (By.ID, "billing_state")
    BILLING_POSTCODE = (By.ID, "billing_postcode")
    BILLING_PHONE = (By.ID, "billing_phone")
    BILLING_EMAIL = (By.ID, "billing_email")

    # Дата доставки
    DELIVERY_DATE = (By.ID, "delivery_date")  # предположительно
    DELIVERY_TIME = (By.ID, "delivery_time")  # предположительно

    # Способ оплаты
    PAYMENT_METHOD_CASH = (By.ID, "payment_method_cod")  # наличные при доставке
    PAYMENT_METHOD_CARD = (By.ID, "payment_method_online")  # картой онлайн
    PAYMENT_METHODS = (By.CSS_SELECTOR, ".payment_methods input")

    # Промокоды
    COUPON_FIELD = (By.ID, "coupon_code")
    APPLY_COUPON_BUTTON = (By.NAME, "apply_coupon")
    COUPON_SUCCESS = (By.CSS_SELECTOR, ".woocommerce-message")
    COUPON_ERROR = (By.CSS_SELECTOR, ".woocommerce-error")

    # Подтверждение заказа
    PLACE_ORDER_BUTTON = (By.ID, "place_order")
    ORDER_NOTES = (By.ID, "order_comments")
    TERMS_CHECKBOX = (By.ID, "terms")

    # Страница подтверждения
    ORDER_RECEIVED = (By.CSS_SELECTOR, ".woocommerce-order-received")
    ORDER_NUMBER = (By.CSS_SELECTOR, ".order-number")
    ORDER_TOTAL = (By.CSS_SELECTOR, ".order-total")
    ORDER_DETAILS = (By.CSS_SELECTOR, ".woocommerce-order-details")

    # Товары в заказе
    ORDER_ITEMS = (By.CSS_SELECTOR, ".woocommerce-table__line-item")
    ORDER_ITEM_NAME = (By.CSS_SELECTOR, ".product-name a")
    ORDER_ITEM_TOTAL = (By.CSS_SELECTOR, ".product-total")


class PizzaDetailPageLocators:
    """Локаторы страницы деталей пиццы"""

    PRODUCT_TITLE = (By.CSS_SELECTOR, ".product_title")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".price .woocommerce-Price-amount")
    PRODUCT_DESCRIPTION = (By.CSS_SELECTOR, ".woocommerce-product-details__short-description")

    # Опции (бортики и т.д.)
    PRODUCT_OPTIONS = (By.CSS_SELECTOR, ".variations select, .variations input")
    OPTION_CHEESE_BORDER = (By.XPATH, "//label[contains(text(), 'сырный')]/input")
    OPTION_SAUSAGE_BORDER = (By.XPATH, "//label[contains(text(), 'колбасный')]/input")

    # Количество и добавление
    QUANTITY_INPUT = (By.CSS_SELECTOR, ".quantity input")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, ".single_add_to_cart_button")

    # Вкладки
    DESCRIPTION_TAB = (By.CSS_SELECTOR, ".description_tab a")
    ADDITIONAL_INFO_TAB = (By.CSS_SELECTOR, ".additional_information_tab a")
    REVIEWS_TAB = (By.CSS_SELECTOR, ".reviews_tab a")

    # Связанные товары
    RELATED_PRODUCTS = (By.CSS_SELECTOR, ".related.products li")
    RELATED_PRODUCTS_TITLE = (By.CSS_SELECTOR, ".related.products h2")


class BonusPageLocators:
    """Локаторы страницы бонусной программы"""

    BONUS_FORM = (By.CSS_SELECTOR, ".bonus-form, #bonus-form")
    NAME_INPUT = (By.ID, "bonus_name, #name")
    PHONE_INPUT = (By.ID, "bonus_phone, #phone")
    EMAIL_INPUT = (By.ID, "bonus_email, #email")
    BIRTHDAY_INPUT = (By.ID, "bonus_birthday, #birthday")

    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit'], .bonus-submit")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".woocommerce-message, .success, .bonus-success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".woocommerce-error, .error, .bonus-error")

    # Валидация полей
    NAME_ERROR = (By.CSS_SELECTOR, ".name-error, #name-error")
    PHONE_ERROR = (By.CSS_SELECTOR, ".phone-error, #phone-error")
    EMAIL_ERROR = (By.CSS_SELECTOR, ".email-error, #email-error")

    # Условия программы
    BONUS_TERMS = (By.CSS_SELECTOR, ".bonus-terms, .terms-text")
    BONUS_RULES = (By.LINK_TEXT, "Правила программы")


class MenuPageLocators:
    """Локаторы страницы меню"""

    # Фильтры
    FILTER_DROPDOWN = (By.CSS_SELECTOR, ".filter-dropdown, .orderby")
    FILTER_POPULARITY = (By.XPATH, "//option[contains(text(), 'популярности')]")
    FILTER_RATING = (By.XPATH, "//option[contains(text(), 'рейтингу')]")
    FILTER_NEWNESS = (By.XPATH, "//option[contains(text(), 'новизне')]")
    FILTER_PRICE_ASC = (By.XPATH, "//option[contains(text(), 'цене: по возрастанию')]")
    FILTER_PRICE_DESC = (By.XPATH, "//option[contains(text(), 'цене: по убыванию')]")

    # Категории
    CATEGORY_PIZZA = (By.XPATH, "//a[contains(text(), 'Пицца') and contains(@class, 'cat-item')]")
    CATEGORY_DESSERTS = (By.XPATH, "//a[contains(text(), 'Десерты') and contains(@class, 'cat-item')]")
    CATEGORY_DRINKS = (By.XPATH, "//a[contains(text(), 'Напитки') and contains(@class, 'cat-item')]")

    # Фильтр по цене
    PRICE_FILTER = (By.CSS_SELECTOR, ".price_slider")
    PRICE_MIN = (By.CSS_SELECTOR, ".price_slider_amount #min_price")
    PRICE_MAX = (By.CSS_SELECTOR, ".price_slider_amount #max_price")
    PRICE_FILTER_BUTTON = (By.CSS_SELECTOR, ".price_slider_amount button")

    # Результаты
    PRODUCTS_FOUND = (By.CSS_SELECTOR, ".woocommerce-result-count")
    NO_PRODUCTS_MESSAGE = (By.CSS_SELECTOR, ".woocommerce-info")