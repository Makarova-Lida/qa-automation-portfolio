import logging
import allure

from playwright.sync_api import Page
from .base_test import BaseTest

logger = logging.getLogger(__name__)


class TestGithubIssues(BaseTest):
    """Тесты для проверки функциональности Issues на GitHub (Playwright)"""
    # Константы
    REPO_URL = "https://github.com/microsoft/vscode/issues"

    @allure.title("Поиск issues с 'bug' в заголовке")
    @allure.description(
        """
    Тест проверяет поиск issues по ключевому слову 'bug' в заголовке.
    Ожидается, что все найденные issues содержат слово 'bug'.
    """
    )
    def test_search_issues_with_bug(self, page: Page):
        """Поиск issues с 'bug' в заголовке"""
        logger.info("Запуск case_1: Поиск issues с 'bug' в заголовке и проверка результатов")
        # Открываем страницу
        with allure.step("Открываем страницу issues"):
            page.goto(self.REPO_URL)
            page.wait_for_load_state('networkidle')
            logger.info(f"Страница загружена: {page.title()}")

            # Скриншот
            allure.attach(
                page.screenshot(full_page=True),
                name="page_loaded",
                attachment_type=allure.attachment_type.PNG
            )

        # ВЫПОЛНЯЕМ ПОИСК
        with allure.step("Выполняем поиск по ключевому слову 'bug'"):
            logger.info("🔍 Выполняю поиск: 'in:title bug'")
            page.get_by_role("combobox", name="Search Issues").click()
            page.get_by_role("combobox", name="Search Issues").fill("in:title bug")
            page.get_by_role("combobox", name="Search Issues").press("Enter")
            logger.info("Поиск выполнен")

        # Получаем все названия задач
        with allure.step("Получение списка найденных задач"):
            # Ждем появления хотя бы одного элемента
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(2000)
            issue_titles = page.get_by_test_id("issue-pr-title-link")
            count = issue_titles.count()

        if count == 0:
            logger.warning("Задачи не найдены")
            # Скриншот
            allure.attach(
                page.screenshot(),
                name="no_results",
                attachment_type=allure.attachment_type.PNG
            )
            return
        logger.info(f"Найдено задач: {count}")

        # Проверяем каждую задачу на наличие слова 'bug' (без учета регистра)
        with allure.step("Проверка наличия 'bug' в заголовках задач"):
            all_contain = True
            bug_count = 0
            non_bug_titles = []

            for i in range(count):
                title_element = issue_titles.nth(i)
                title_text = title_element.text_content()
                title_text_lower = title_text.lower()
                with allure.step(f"Проверка задачи #{i}: {title_text[:50]}..."):
                    if "bug" in title_text_lower:
                        bug_count += 1
                        logger.debug(f"Задача {i}: '{title_text}' - содержит 'bug'")
                    else:
                        all_contain = False
                        non_bug_titles.append(title_text[:50])
                        logger.warning(f"Задача {i}: '{title_text}' - НЕ содержит 'bug'!")

            logger.info(f"Задач с 'bug': {bug_count} из {count}")

        # Проверяем условие
        with allure.step("Формирование результатов теста"):
            if all_contain:
                logger.info("ТЕСТ ПРОЙДЕН: Все задачи содержат слово 'bug' в заголовке")
            else:
                logger.error("ТЕСТ НЕ ПРОЙДЕН: Не все задачи содержат слово 'bug' в заголовке")

        assert all_contain, "ТЕСТ НЕ ПРОЙДЕН: Не все задачи содержат слово 'bug' в заголовке"

    @allure.title("Фильтрация issues по автору bpasero")
    @allure.description("Тест проверяет фильтрацию issues по конкретному автору")
    def test_filter_by_author_bpasero(self, page: Page):
        """Фильтруем issues по автору bpasero"""
        with allure.step("Логирование начала теста"):
            logger.info("Запуск case_2: Фильтрация по автору bpasero и проверка результатов")

        # Открываем страницу
        with allure.step("Открытие страницы issues"):
            page.goto("https://github.com/microsoft/vscode/issues")
            page.wait_for_selector('[data-testid="issue-pr-title-link"]', timeout=15000)
            logger.info("Страница с issues загружена")
            allure.attach(
                page.screenshot(full_page=True),
                name="page_loaded",
                attachment_type=allure.attachment_type.PNG)

        # Применяем фильтр
        with allure.step("Применение фильтра по автору bpasero"):
            self._apply_author_filter(page, 'bpasero')
            logger.info("Фильтр по автору применен")

        # Получаем все задачи
        with allure.step("Получение отфильтрованных задач"):
            page.wait_for_timeout(2000)
            issue_links = page.get_by_test_id("issue-pr-title-link")
            issue_count = issue_links.count()
            if issue_count == 0:
                logger.error("Задачи не найдены ")
                return
            logger.info(f"Найдено задач: {issue_count}")

            # Получаем всех авторов задач
            author_elements = page.locator("//a[contains(text(), 'bpasero')]")
            author_count = author_elements.count()

            logger.info(f"Найдено элементов автора: {author_count}")

        # Логируем информацию о найденных задачах (для отладки)
        with allure.step("Проверка авторов всех задач"):
            all_correct = True

            for i in range(author_count):
                author_element = author_elements.nth(i)
                author_text = author_element.text_content().strip()

                if author_text.lower() != "bpasero":
                    all_correct = False
                    logger.warning(f"Задача #{i + 1}: неправильный автор '{author_text}'")
                else:
                    logger.debug(f"Задача #{i + 1}: правильный автор '{author_text}'")


            with allure.step("Финальная проверка и логирование"):
                if all_correct:
                    logger.info("ТЕСТ ПРОЙДЕН: Фильтрация по автору bpasero работает корректно")

                else:
                    logger.info("ТЕСТ НЕ ПРОЙДЕН: Фильтрация по автору bpasero не работает корректно")

    @allure.step("Выполняет поиск по заданному запросу")
    def _search_issues(self, page, search):
        """Выполняет поиск по заданному запросу"""
        with allure.step(f"Ввод поискового запроса: {search}"):
            logger.info(f"Выполняю поиск: '{search}'")

            page.get_by_role("combobox", name="Search Issues").click()
            page.get_by_role("combobox", name="Search Issues").fill("in:title bug")
            page.get_by_role("combobox", name="Search Issues").press("Enter")
        logger.debug("Действия поиска выполнены")
        # Ждем загрузки результатов
        logger.info(f"Поиск '{search}' завершен, ожидаю загрузки результатов")

    @allure.step("Применение фильтра по автору: '{author_name}'")
    def _apply_author_filter(self, page, author_name):
        """Применяет фильтр по автору"""
        logger.info(f"Применяю фильтр по автору: '{author_name}'")

        # Открываем фильтр по автору
        with allure.step("Открытие фильтра по автору"):
            page.get_by_test_id("authors-anchor-button").click()
            logger.debug("Открыт фильтр по автору")

        # Вводим имя автора в поиск
        with allure.step(f"Ввод имени автора: {author_name}"):
            page.get_by_role("combobox", name="Filter authors").click()
            page.get_by_role("combobox", name="Filter authors").fill(author_name)
            logger.debug(f"Введено имя автора: {author_name}")

        # Выбираем автора
        with allure.step("Выбор автора из списка"):
            page.get_by_test_id("item-picker-root").get_by_text(author_name).click()
            logger.debug(f"Автор {author_name} выбран")
            # Ждем загрузки результатов

            logger.info(f"Фильтр по автору '{author_name}' применен")
