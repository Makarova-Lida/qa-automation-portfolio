import time
import logging
import allure

from selenium.webdriver.support import expected_conditions as EC
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
    def test_commit_activity_graph(self, driver, wait, actions):
        """Тест 5: Проверка графика коммитов"""

        with allure.step("Подготовка теста"):
            logger.info("Запуск case_5: Проверка наведения на график коммитов")

        # Открываем страницу с графиком
        with allure.step("Открытие страницы с графиком коммитов"):
            driver.get("https://github.com/microsoft/vscode/graphs/commit-activity")
            time.sleep(3)
            logger.info("Страница графика коммитов загружена")
            logger.debug(f"Текущий URL: {driver.current_url}")

        # Находим элементы графика
        with allure.step("Поиск элементов графика"):
            all_graph_elements = driver.find_elements("css selector", ".highcharts-point.highcharts-color-0")
            logger.info(f"Найдено элементов графика: {len(all_graph_elements)}")

        if not all_graph_elements:
            logger.error("Элементы графика не найдены")
            raise AssertionError("Элементы графика не найдены")

        # Выбираем элемент в середине графика
        with allure.step("Выбор элемента для взаимодействия"):
            middle_index = len(all_graph_elements) // 2
            graph_element = all_graph_elements[middle_index]
            logger.debug(f"Выбран элемент графика с индексом {middle_index} (всего: {len(all_graph_elements)})")

        # Прокручиваем и наводим курсор
        with allure.step("Подготовка элемента к взаимодействию"):
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", graph_element)
            time.sleep(1)
            logger.debug("Элемент прокручен в область видимости")

        with allure.step("Наведение курсора на элемент графика"):
            actions.move_to_element(graph_element).pause(1).perform()
            logger.info(f"Наведено на элемент графика #{middle_index}")

        # Ждем появления тултипа и извлекаем значение
        with allure.step("Ожидание и проверка тултипа"):
            logger.debug("Ожидаю появления тултипа...")
            try:
                strong_element = wait.until(
                    EC.visibility_of_element_located(("css selector", ".highcharts-tooltip strong"))
                )
                value = strong_element.text.strip()
                logger.info(f"Найдено значение в тултипе: {value}")

                # Проверяем, что значение не пустое
                if value:
                    logger.info("✓ Значение в тултипе успешно получено")
                else:
                    logger.warning("Тултип появился, но значение пустое")

            except Exception as e:
                logger.error(f"Ошибка при получении значения из тултипа: {e}")
                raise
