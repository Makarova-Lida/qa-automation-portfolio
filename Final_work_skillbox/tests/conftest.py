import pytest
import logging
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Отключаем подробные логи WebDriver
logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.WARNING)
logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)
logging.getLogger('WDM').setLevel(logging.WARNING)


def setup_logging():
    """Настройка логирования"""
    if not os.path.exists('logs'):
        os.makedirs('logs')

    log_filename = f'logs/test_run_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

    log_format = '[%(levelname)s][%(asctime)s][%(name)s] %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'

    # Убираем лишние handlers для консоли
    logging.basicConfig(
        level=logging.INFO,  # INFO вместо DEBUG
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger(__name__)
    logger.info(f"Логирование настроено. Файл: {log_filename}")
    return logger


logger = setup_logging()


@pytest.fixture(scope="function")
def driver():
    logger.info("=" * 60)
    logger.info("ЗАПУСК ТЕСТА")
    logger.info("=" * 60)

    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')

    try:
        # Настройка опций Chrome для подавления ошибок
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--log-level=3')  # Только fatal ошибки
        chrome_options.add_argument('--silent')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        logger.info("Браузер Chrome запущен")
    except Exception as e:
        logger.warning(f"Ошибка: {e}")
        driver = webdriver.Chrome()

    driver.maximize_window()
    logger.info("Окно браузера развернуто")

    yield driver

    logger.info("Закрытие браузера")
    driver.quit()
    logger.info("=" * 60 + "\n")

@pytest.fixture
def browser(driver):
    return driver


@pytest.fixture
def base_url():
    return "https://pizzeria.skillbox.cc/"


@pytest.fixture
def main_page(driver):
    from pages.main_page import MainPage
    page = MainPage(driver)
    page.open()
    logger.info("Главная страница открыта")
    return page


@pytest.fixture
def cart_page(driver, main_page):
    from pages.cart_page import CartPage
    main_page.add_product_to_cart_by_index(0)
    main_page.go_to_cart()
    logger.info("Страница корзины открыта")
    return CartPage(driver)


@pytest.fixture
def auth_page(driver, main_page):
    from pages.auth_page import AuthPage
    main_page.go_to_account()
    logger.info("Страница авторизации открыта")
    return AuthPage(driver)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        logger.error(f"❌ Тест {item.name} УПАЛ!")

        if "driver" in item.fixturenames:
            driver = item.funcargs["driver"]
            screenshot_name = f"screenshots/{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            driver.save_screenshot(screenshot_name)
            logger.info(f"📸 Скриншот: {screenshot_name}")