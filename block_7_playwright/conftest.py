import pytest
import logging.config

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s][%(asctime)s][%(name)s] %(message)s',
    handlers=[
        logging.FileHandler('playwright_log.txt', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="function")
def page():
    """Фикстура для создания страницы для каждого теста"""
    from playwright.sync_api import sync_playwright

    logger.info("Запускаю браузер Playwright...")
    with sync_playwright() as playwright:
        # Выбираем браузер (chromium, firefox, webkit)
        browser = playwright.chromium.launch(
            headless=False,  # False - видим браузер, True - скрытый режим
            slow_mo=100,  # Замедляем действия на 100ms для наглядности
        )

        logger.info("Браузер запущен")

        # Создаём контекст (как incognito режим)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},  # Размер окна
            ignore_https_errors=True,  # Игнорируем SSL ошибки
        )
        page = context.new_page()

        # Настраиваем таймауты
        page.set_default_timeout(30000)  # 30 секунд на операции
        page.set_default_navigation_timeout(60000)  # 60 секунд на загрузку страниц

        logger.info("Страница создана и настроена")

        # Передаём страницу тесту
        yield page

        context.close()
        browser.close()


