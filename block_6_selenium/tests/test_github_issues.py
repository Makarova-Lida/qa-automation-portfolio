import time
import logging
import allure

from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
from .base_test import BaseTest

logger = logging.getLogger(__name__)


class TestGithubIssues(BaseTest):

    # Константы
    REPO_URL = "https://github.com/microsoft/vscode/issues"

    SEARCH_INPUT_LOCATOR = ("xpath", '//input[@id="repository-input"]')
    AUTHOR_LOCATOR = ("xpath", "//span[text()='Author']")
    SEARCH_LOCATOR = ("xpath", '//input[@placeholder="Filter authors"]')

    @allure.title("Поиск issues с 'bug' в заголовке")
    @allure.description(
        """
    Тест проверяет поиск issues по ключевому слову 'bug' в заголовке.
    Ожидается, что все найденные issues содержат слово 'bug'.
    """
    )
    def test_search_issues_with_bug(self, driver, wait, actions):
        """Поиск issues с 'bug' в заголовке"""
        logger.info("Запуск case_1: Поиск issues с 'bug' в заголовке и проверка результатов")
        # Открываем страницу
        with allure.step("Открываем страницу issues"):
            driver.get(self.REPO_URL)
            time.sleep(2)
            logger.debug("Страница загружена")

        # ВЫПОЛНЯЕМ ПОИСК
        with allure.step("Выполняем поиск по ключевому слову 'bug'"):  # <- Добавляем
            self._search_issues(wait, actions, "in:title bug")
            logger.info("Поиск выполнен")

        # Получаем все названия задач
        with allure.step("Получение списка найденных задач"):
            issue_titles = driver.find_elements("xpath", '//a[contains(@data-hovercard-url, "issues")]')
            logger.info(f"Найдено задач: {len(issue_titles)}")

        logger.debug(f"Найдены элементы: {issue_titles}")

        # Проверяем каждую задачу на наличие слова 'bug' (без учета регистра)
        with allure.step("Проверка наличия 'bug' в заголовках задач"):
            all_contain = True
            bug_count = 0

            for i, title_element in enumerate(issue_titles):
                title_text = title_element.text.lower()
                with allure.step(f"Проверка задачи #{i}: {title_text[:50]}..."):
                    if "bug" in title_text:
                        bug_count += 1
                        logger.debug(f"Задача {i}: '{title_element.text}' - содержит 'bug'")
                    else:
                        all_contain = False
                        logger.warning(f"Задача {i}: '{title_element.text}' - НЕ содержит 'bug'!")

            logger.info(f"Задач с 'bug': {bug_count} из {len(issue_titles)}")

        # Проверяем условие
        with allure.step("Формирование результатов теста"):
            if all_contain:
                logger.info("ТЕСТ ПРОЙДЕН: Все задачи содержат слово 'bug' в заголовке")
            else:
                logger.error("ТЕСТ НЕ ПРОЙДЕН: Не все задачи содержат слово 'bug' в заголовке")

        assert all_contain, "ТЕСТ НЕ ПРОЙДЕН: Не все задачи содержат слово 'bug' в заголовке"

    @allure.title("Фильтрация issues по автору bpasero")
    @allure.description("Тест проверяет фильтрацию issues по конкретному автору")
    def test_filter_by_author_bpasero(self, driver, wait, actions):
        """Фильтруем issues по автору bpasero"""
        with allure.step("Логирование начала теста"):
            logger.info("Запуск case_2: Фильтрация по автору bpasero и проверка результатов")

        # Локаторы
        AUTHOR_BPASERO_LOCATOR = ("xpath", "//span[text()='bpasero']")
        ISSUES_LOCATOR = ("xpath", "//a[contains(@class, 'authorCreatedLink') and text()='bpasero']")
        FILTER_AUTHOR_BPASERO_LOCATOR = ("xpath", "//input[@id='repository-input' and contains(@value, 'bpasero')]")

        # Открываем страницу
        with allure.step("Открытие страницы issues"):
            driver.get(self.REPO_URL)
            time.sleep(2)
            logger.debug("Страница с issues загружена")

        # ПРИМЕНЯЕМ ФИЛЬТР
        with allure.step("Применение фильтра по автору bpasero"):
            self._apply_author_filter(driver, wait, actions, "bpasero", AUTHOR_BPASERO_LOCATOR)
            logger.info("Фильтр по автору применен")

        # Получаем все задачи
        with allure.step("Получение отфильтрованных задач"):
            issues = driver.find_elements(*ISSUES_LOCATOR)
            logger.info(f"Найдено задач автора bpasero: {len(issues)}")

        # Логируем информацию о найденных задачах (для отладки)
        for i, issue in enumerate(issues[:5]):  # Логируем только первые 5 для примера
            logger.debug(f"Задача {i}: {issue.text}")

        # Получаем информацию об авторе из фильтра
        with allure.step("Проверка значения фильтра"):
            element = driver.find_element(*FILTER_AUTHOR_BPASERO_LOCATOR)
            value = element.get_attribute("value")
            logger.debug(f"Значение фильтра: {value}")

            if "bpasero" in value:
                logger.info("Фильтр по автору применен и содержит 'bpasero' в value")
            else:
                logger.error("Фильтр по автору не применен или не содержит 'bpasero'")

        with allure.step("Финальная проверка и логирование"):
            assert "bpasero" in value, "Фильтр по автору не применен или не содержит 'bpasero'"
            logger.info("ТЕСТ ПРОЙДЕН: Фильтрация по автору bpasero работает корректно")

    def _search_issues(self, wait, actions, search):
        """Выполняет поиск по заданному запросу"""
        with allure.step(f"Ввод поискового запроса: {search}"):
            logger.info(f"Выполняю поиск: '{search}'")

            search_input = wait.until(EC.presence_of_element_located(self.SEARCH_INPUT_LOCATOR))
            actions.click(search_input).pause(1).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(
                Keys.DELETE
            ).send_keys(search).send_keys(Keys.ENTER).perform()

        logger.debug("Действия поиска выполнены")
        # Ждем загрузки результатов
        time.sleep(3)
        logger.info(f"Поиск '{search}' завершен, ожидаю загрузки результатов")

    @allure.step("Применение фильтра по автору: '{author_name}'")
    def _apply_author_filter(self, driver, wait, actions, author_name, author_locator):
        """Применяет фильтр по автору"""
        logger.info(f"Применяю фильтр по автору: '{author_name}'")

        # Открываем фильтр по автору
        with allure.step("Открытие фильтра по автору"):
            author = wait.until(EC.element_to_be_clickable(self.AUTHOR_LOCATOR))
            author.click()
            logger.debug("Открыт фильтр по автору")
            time.sleep(1)

        # Вводим имя автора в поиск
        with allure.step(f"Ввод имени автора: {author_name}"):
            search_input = wait.until(EC.presence_of_element_located(self.SEARCH_LOCATOR))
            actions.click(search_input).send_keys("bpasero").perform()
            logger.debug(f"Введено имя автора: {author_name}")
            time.sleep(1)

        # Выбираем автора
        with allure.step("Выбор автора из списка"):
            driver.find_element(*author_locator).click()
            logger.debug(f"Автор {author_name} выбран")
            # Ждем загрузки результатов
            time.sleep(3)
            logger.info(f"Фильтр по автору '{author_name}' применен")
