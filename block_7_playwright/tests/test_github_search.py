import logging
import allure

from .base_test import BaseTest

logger = logging.getLogger(__name__)


class TestGithubSearch(BaseTest):
    # КОНСТАНТЫ
    SEARCH_PAGE_URL = "https://github.com/search/advanced"

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
    def test_advanced_search_repositories(self, page):
        """Поиск репозиториев: Python, >20000 звёзд, environment.yml"""
        with allure.step("Подготовка теста"):
            logger.info("Запуск case_3: Расширенный поиск репозиториев с Python, >20000 звезд и файлом environment.yml")

        # ОТКРЫВАЕМ СТРАНИЦУ
        with allure.step("Открытие страницы расширенного поиска"):
            page.goto(self.SEARCH_PAGE_URL)
            page.wait_for_load_state('networkidle')
            logger.info("Страница поиска загружена")
            logger.debug(f"Текущий URL: {page.url}")

            # Делаем скриншот
            allure.attach(
                page.screenshot(full_page=True),
                name="search_page_loaded",
                attachment_type=allure.attachment_type.PNG
            )

        # ЗАПОЛНЯЕМ ФОРМУ ПОИСКА
        with allure.step("Заполнение формы поиска"):
            self._full_search(page)
            logger.info("Форма поиска заполнена")
            # Скриншот заполненной формы
            allure.attach(
                page.screenshot(full_page=True),
                name="form_filled",
                attachment_type=allure.attachment_type.PNG
            )

        # Нажатие на кнопку Поиск
        with allure.step("Выполнение поиска"):
            logger.debug("Нажимаю кнопку поиска...")
            page.get_by_role("button", name="Search").nth(2).click()
            logger.info("Кнопка поиска нажата")


        # ЖДЕМ ЗАГРУЗКИ РЕЗУЛЬТАТОВ
        with allure.step("Ожидание загрузки результатов"):
            self._wait_for_results(page)

        # Получаем количество найденных репозиториев
        with allure.step("Получение списка репозиториев"):
            page.wait_for_selector('div[data-testid="results-list"]', timeout=15000)

            repositories = page.locator('article.Box-row')
            repo_count = repositories.count()
            logger.info(f"\nНайдено репозиториев: {repo_count}")

            if repo_count == 0:
                logger.warning("Результаты поиска не найдены")
            else:
                logger.debug("Первые 5 репозиториев доступны для проверки")

        # Проверяем звезды для каждого репозитория
        with allure.step("Проверка звезд у каждого репозитория"):
            all_stars_valid = True
            count = 0

            for i in range(repo_count):
                # Получаем название репозитория
                repository = repositories.nth(i)

                repo_title_elem = repository.locator('a[data-hydro-click*="repo_name"]')
                repo_name = repo_title_elem.text_content()
                logger.debug("Обработка репозитория #{i}: {repo_name}")

                # Получаем количество звезд
                stars_elem = repository.locator('a[href*="stargazers"]')
                stars_text = stars_elem.text_content().strip()
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
                logger.info(f"✓ Успешно проверено репозиториев: {count}")
            else:
                logger.error("✗ Не все репозитории соответствуют условию (>20000 звезд)")

        assert all_stars_valid, "Не все репозитории соответствуют условию (>20000 звезд)"

        logger.info("Тест расширенного поиска завершен")

    @allure.step("Заполнение формы расширенного поиска")
    def _full_search(self, page):
        """Заполняет форму поиска"""
        logger.info("Заполняю форму поиска...")
        # Выбор языка Python
        with allure.step("Выбор языка программирования: Python"):
            logger.debug("Выбираю язык Python...")
            page.get_by_label("Written in this language").select_option("Python")

            logger.info("✓ Язык выбран: Python")

        # Ввод количества звезд
        with allure.step("Ввод минимального количества звезд: >20000"):
            logger.debug("Ввожу количество звезд (>20000)...")
            page.get_by_role("textbox", name="With this many stars").click()
            page.get_by_role("textbox", name="With this many stars").fill(">20000")
            logger.info("✓ Количество звезд указано: >20000")

        # Ввод имени файла
        with allure.step("Ввод имени файла: environment.yml"):
            logger.debug("Ввожу имя файла (environment.yml)...")
            page.get_by_role("textbox", name="With this file name").click()
            page.get_by_role("textbox", name="With this file name").fill("environment.yml")
            logger.info("✓ Имя файла указано: environment.yml")

        logger.debug("Форма поиска полностью заполнена")

    @allure.step("Ожидание загрузки результатов поиска")
    def _wait_for_results(self, page):
        """Ждёт загрузки результатов"""
        logger.info("Ожидаю загрузки результатов поиска...")

        # Ждём появления первого результата
        try:
            page.wait_for_selector('div[data-testid="results-list"],'
                                   ' div[data-testid="no-results"]', timeout=15000)
            logger.info("✓ Результаты поиска загружены")
        except Exception as e:
            logger.error(f"Результаты не найдены: {e}")
            logger.warning("Продолжаю выполнение теста, но результаты могут быть недоступны")
