import logging
import allure

from .base_test import BaseTest

logger = logging.getLogger(__name__)


class TestGithubGraph(BaseTest):

    @allure.title("Проверка графика активности коммитов")
    @allure.description(
        """
       Тест проверяет интерактивность графика коммитов на GitHub.
       Выполняет наведение на элемент графика и проверяет отображение тултипа.
       """
    )
    def test_commit_activity_graph(self, page):
        """Тест 5: Проверка графика коммитов"""

        with allure.step("Подготовка теста"):
            logger.info("Запуск case_5: Проверка наведения на график коммитов")

        # Открываем страницу с графиком
        with allure.step("Открытие страницы с графиком коммитов"):
            page.goto("https://github.com/microsoft/vscode/graphs/commit-activity")
            logger.info("Страница графика коммитов загружена")
            logger.debug(f"Текущий URL: {page.url}")
            # Скриншот загруженной страницы
            allure.attach(
                page.screenshot(full_page=True),
                name="graph_page_loaded",
                attachment_type=allure.attachment_type.PNG
            )
        page.wait_for_timeout(5000)
        # Находим элементы графика
        with allure.step("Поиск элементов графика"):
            all_graph_elements = page.locator('.highcharts-point')
            logger.info(f"Найдено элементов графика: {all_graph_elements.count()}")

        if not all_graph_elements:
            logger.error("Элементы графика не найдены")
            raise AssertionError("Элементы графика не найдены")

        # Выбираем элемент в середине графика
        with allure.step("Выбор элемента для взаимодействия"):
            middle_index = all_graph_elements.count() // 2
            graph_element = all_graph_elements.nth(middle_index)
            logger.debug(f"Выбран элемент графика с индексом {middle_index} (всего: {all_graph_elements.count()})")

        # Прокручиваем и наводим курсор
        with allure.step("Наведение курсора на элемент графика"):
            graph_element.hover()
            page.wait_for_timeout(5000)
            logger.info(f"Наведено на элемент графика #{middle_index}")

        # Ждем появления тултипа и извлекаем значение
        with allure.step("Ожидание и проверка тултипа"):
            logger.debug("Ожидаю появления тултипа...")
            try:
                strong_element = page.locator('.highcharts-tooltip strong')
                value = strong_element.text_content().strip()
                logger.info(f"Найдено значение в тултипе: {value}")

                # Проверяем, что значение не пустое
                if value:
                    logger.info("✓ Значение в тултипе успешно получено")
                else:
                    logger.warning("Тултип появился, но значение пустое")

            except Exception as e:
                logger.error(f"Ошибка при получении значения из тултипа: {e}")
                raise
