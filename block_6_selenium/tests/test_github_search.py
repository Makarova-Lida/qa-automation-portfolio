import time
import logging
import allure

# импорт для работы с селектами
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from .base_test import BaseTest

logger = logging.getLogger(__name__)


class TestGithubSearch(BaseTest):
    # КОНСТАНТЫ
    SEARCH_PAGE_URL = "https://github.com/search/advanced"
    # Локаторы формы поиска
    SELECT_LANGUAGE_LOCATOR = ("xpath", '//select[@id="search_language"]')
    STARS_LOCATOR = ("xpath", '//input[@id="search_stars"]')
    NAME_FILE_LOCATOR = ("xpath", '//input[@id="search_filename"]')
    SEARCH_LOCATOR = ("xpath", '//button[@class="btn flex-auto"][1]')
    # Локаторы результатов
    REPOSITORIES_LOCATOR = ("xpath", '//div[@class="Box-sc-62in7e-0 fXzjPH"]')
    REPO_STARS_LOCATOR = ("xpath", './/a[contains(@href, "stargazers")]')
    REPO_TITLE_LOCATOR = ("css selector", "a.prc-Link-Link-9ZwDx span.search-match")
    REPO_LINK_LOCATOR = ("xpath", './/a[contains(@class, "prc-Link-Link")]')

    @allure.title("Расширенный поиск репозиториев")
    @allure.description(
        """
       Тест проверяет расширенный поиск репозиториев на GitHub с фильтрами:
       - Язык: Python
       - Звезды: >20000
       - Файл: environment.yml

       Ожидается, что все найденные репозитории имеют более 20000 звезд.
       """
    )
    def test_advanced_search_repositories(self, driver, wait, actions):
        """Поиск репозиториев: Python, >20000 звёзд, environment.yml"""
        with allure.step("Подготовка теста"):
            logger.info("Запуск case_3: Расширенный поиск репозиториев с Python, >20000 звезд и файлом environment.yml")

        # ОТКРЫВАЕМ СТРАНИЦУ
        with allure.step("Открытие страницы расширенного поиска"):
            driver.get(self.SEARCH_PAGE_URL)
            time.sleep(3)
            logger.info("Страница поиска загружена")
            logger.debug(f"Текущий URL: {driver.current_url}")

        # ЗАПОЛНЯЕМ ФОРМУ ПОИСКА
        with allure.step("Заполнение формы поиска"):
            self._full_search(driver, wait, actions)
            logger.info("Форма поиска заполнена")

        # Нажатие на кнопку Поиск
        with allure.step("Выполнение поиска"):
            logger.debug("Нажимаю кнопку поиска...")
            search_button = wait.until(EC.element_to_be_clickable(self.SEARCH_LOCATOR))
            search_button.click()
            logger.info("Кнопка поиска нажата")

        # ЖДЕМ ЗАГРУЗКИ РЕЗУЛЬТАТОВ
        with allure.step("Ожидание загрузки результатов"):
            self._wait_for_results(wait)

        # Получаем количество найденных репозиториев
        with allure.step("Получение списка репозиториев"):
            repositories = driver.find_elements(*self.REPOSITORIES_LOCATOR)
            logger.info(f"\nНайдено репозиториев: {len(repositories)}")

            if len(repositories) == 0:
                logger.warning("Результаты поиска не найдены")
            else:
                logger.debug("Первые 5 репозиториев доступны для проверки")

        # Проверяем звезды для каждого репозитория
        with allure.step("Проверка звезд у каждого репозитория"):
            all_stars_valid = True
            count = 0

            for i, repository in enumerate(repositories, 1):
                # Получаем название репозитория
                repo_title_elem = repository.find_element(*self.REPO_TITLE_LOCATOR)
                repo_name = repo_title_elem.text
                logger.debug("Обработка репозитория #{i}: {repo_name}")

                # Получаем количество звезд
                stars_elem = repository.find_element(*self.REPO_STARS_LOCATOR)
                stars_text = stars_elem.text.strip()
                logger.debug(f"  Исходный текст звезд: '{stars_text}'")

                stars_value = 0
                if stars_text:
                    if "k" in stars_text.lower():
                        stars_value = float(stars_text.lower().replace("k", "")) * 1000
                    else:
                        stars_text = stars_text.replace(",", "")
                        stars_value = float(stars_text)

                # Проверяем условие >20000
                stars_valid = stars_value > 20000

                if not stars_valid:
                    all_stars_valid = False

                # Выводим информацию
                logger.debug(f"Репозиторий #{i} Название: {repo_name}")
                logger.debug(f"  Звезды: {stars_text} ({stars_value:.0f})")
                logger.debug(f"  Соответствие условию (>20000): {stars_valid}")
                count += 1
        with allure.step("Формирование результатов теста"):
            if all_stars_valid:
                logger.info("✓ Все проверенные репозитории соответствуют условию (>20000 звезд)")
                logger.info(f"✓ Успешно проверено репозиториев: {len(repositories)}")
            else:
                logger.error("✗ Не все репозитории соответствуют условию (>20000 звезд)")

        assert all_stars_valid, "Не все репозитории соответствуют условию (>20000 звезд)"

        logger.info("Тест расширенного поиска завершен")

    @allure.step("Заполнение формы расширенного поиска")
    def _full_search(self, driver, wait, actions):
        """Заполняет форму поиска"""
        logger.info("Заполняю форму поиска...")
        # Выбор языка Python
        with allure.step("Выбор языка программирования: Python"):
            logger.debug("Выбираю язык Python...")
            select_language = Select(wait.until(EC.presence_of_element_located(self.SELECT_LANGUAGE_LOCATOR)))
            select_language.select_by_visible_text("Python")
            logger.info("✓ Язык выбран: Python")

        # Ввод количества звезд
        with allure.step("Ввод минимального количества звезд: >20000"):
            logger.debug("Ввожу количество звезд (>20000)...")
            stars_input = wait.until(EC.presence_of_element_located(self.STARS_LOCATOR))
            actions.click(stars_input).send_keys(">20000").perform()
            time.sleep(1)
            logger.info("✓ Количество звезд указано: >20000")

        # Ввод имени файла
        with allure.step("Ввод имени файла: environment.yml"):
            logger.debug("Ввожу имя файла (environment.yml)...")
            name_file = wait.until(EC.presence_of_element_located(self.NAME_FILE_LOCATOR))
            actions.click(name_file).send_keys("environment.yml").perform()
            time.sleep(1)
            logger.info("✓ Имя файла указано: environment.yml")

        logger.debug("Форма поиска полностью заполнена")

    @allure.step("Ожидание загрузки результатов поиска")
    def _wait_for_results(self, wait):
        """Ждёт загрузки результатов"""
        logger.info("Ожидаю загрузки результатов поиска...")

        # Ждём появления первого результата
        try:
            wait.until(EC.presence_of_element_located(self.REPOSITORIES_LOCATOR))
            logger.info("✓ Результаты поиска загружены")
        except Exception as e:
            logger.error(f"⚠️ Результаты не найдены: {e}")
            logger.warning("Продолжаю выполнение теста, но результаты могут быть недоступны")
