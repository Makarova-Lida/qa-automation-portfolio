import pytest
import logging.config
from os import path

log_file_path = path.join(path.dirname(path.abspath(__file__)), "logging.ini")
logging.config.fileConfig(log_file_path)
logger = logging.getLogger(__name__)

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains


@pytest.fixture(scope="function")
def driver():
    """Фикстура для инициализации и завершения работы драйвера"""
    logger.info("Настраиваю опции браузера...")
    options = Options()
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    service = Service(executable_path=ChromeDriverManager().install())
    logger.info("Создаю драйвер...")
    driver_instance = webdriver.Chrome(service=service, options=options)

    logger.info("Передаю драйвер в тест...")
    yield driver_instance

    logger.info("Закрываю браузер...")
    driver_instance.quit()


@pytest.fixture(scope="function")
def wait(driver):
    """Фикстура для ожиданий"""
    return WebDriverWait(driver, 10)


@pytest.fixture(scope="function")
def actions(driver):
    """Фикстура для действий ActionChains"""
    return ActionChains(driver)
