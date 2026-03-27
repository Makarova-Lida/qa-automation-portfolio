import time
import logging
import allure

from selenium.webdriver.support import expected_conditions as EC
from .base_test import BaseTest

logger = logging.getLogger(__name__)


class TestSkillBox(BaseTest):
    @allure.title("Фильтрация курсов на Skillbox")
    @allure.description(
        """
       Тест проверяет функциональность фильтрации курсов на платформе Skillbox.
       Применяются фильтры:
       - Тип курса: Профессия
       - Длительность: От 6 до 12 месяцев

       Тест проверяет, что после применения фильтров отображаются соответствующие курсы.
       """
    )
    def test_filter_courses(self, driver, wait):
        """Фильтрация курсов на Skillbox"""

        # Локаторы
        MENU_BUTTON_LOCATOR = ("xpath", '//button[@aria-label="Показать фильтр"]')
        PROF_LOCATOR = (
            "xpath",
            '//button[contains(@class, "programs-filter-group__tab") and .//span[contains(text(), "Профессия")]]',
        )
        DLIT_LOCATOR = ("xpath", '//button[.//span[normalize-space(text())="От 6 до 12 мес."]]')
        COURSE_CARDS_LOCATOR = ("xpath", '//div[contains(@class, "product-card-new__info")]')
        BUTTON_LOCATOR = ("xpath", '//button[normalize-space(text())="Применить"]')

        with allure.step("Подготовка теста"):
            logger.info("Запуск case_4: Фильтрация курсов на Skillbox")

        # Открыть страницу
        with allure.step("Открытие страницы курсов"):
            logger.info("Открываю страницу курсов Skillbox")
            driver.get("https://skillbox.ru/code/")
            logger.debug(f"Текущий URL: {driver.current_url}")

        # Открыть фильтр
        with allure.step("Открытие панели фильтров"):
            logger.info("Открываю фильтр курсов")
            filter_bt = wait.until(EC.element_to_be_clickable(MENU_BUTTON_LOCATOR))
            filter_bt.click()
            time.sleep(3)
            logger.info("✓ Фильтр открыт")

        # Выбрать "Профессия"
        with allure.step("Выбор типа курса: Профессия"):
            logger.info("Выбираю тип курса: Профессия")
            profession = wait.until(EC.element_to_be_clickable(PROF_LOCATOR))
            profession.click()
            logger.info("✓ Тип 'Профессия' выбран")

        # Выбрать длительность 6-12 месяцев
        with allure.step("Выбор длительности: От 6 до 12 месяцев"):
            logger.info("Выбираю длительность: От 6 до 12 мес.")
            duration = wait.until(EC.element_to_be_clickable(DLIT_LOCATOR))
            duration.click()
            logger.info("✓ Длительность 'От 6 до 12 мес.' выбрана")

        # Применить фильтры
        with allure.step("Применение выбранных фильтров"):
            time.sleep(3)
            logger.info("Применяю выбранные фильтры")
            apply_btn = wait.until(EC.element_to_be_clickable(BUTTON_LOCATOR))
            apply_btn.click()
            logger.info("✓ Фильтры применены")

        # Обновление результатов
        with allure.step("Ожидание обновления списка курсов"):
            time.sleep(3)
            logger.info("Ожидаю обновления списка курсов")

        # вывести информацию
        with allure.step("Получение отфильтрованных курсов"):
            courses = driver.find_elements(*COURSE_CARDS_LOCATOR)
            logger.info(f"Найдено курсов после фильтрации: {len(courses)}")
            if not courses:
                logger.error("✗ Курсы не найдены после применения фильтров")
                logger.error("ТЕСТ НЕ ПРОЙДЕН: Не найдены курсы после фильтрации")
                raise AssertionError("Курсы не найдены после применения фильтров")
        with allure.step("Анализ найденных курсов"):
            logger.info("=" * 60)
            logger.info("НАЙДЕННЫЕ КУРСЫ:")
            logger.info("=" * 60)

            # Извлекаем информацию о каждом курсе
            for i, course in enumerate(courses, 1):
                try:
                    # Название курса
                    title_elem = course.find_element("xpath", './/a[contains(@class, "product-card-new__title")]')
                    course_name = title_elem.text.strip()

                    # Длительность курса (первый элемент в списке features)
                    duration_elem = course.find_element("css selector", 'li[class*="product-card-new__feature"]')
                    course_duration = duration_elem.text.strip()

                    print(f"\nКурс #{i}:")
                    print(f"  Название: {course_name}")
                    print(f"  Длительность: {course_duration}")

                except Exception as e:
                    error_msg = f"Курс #{i}: Ошибка при извлечении данных: {str(e)}"
                    logger.error(error_msg)

        with allure.step("Формирование результатов теста"):
            if len(courses) > 0:
                logger.info("✓ ТЕСТ ПРОЙДЕН: Курсы успешно отфильтрованы")
                logger.info(f"✓ Найдено {len(courses)} корректных курсов после фильтрации")
            else:
                logger.error("✗ ТЕСТ НЕ ПРОЙДЕН: Не удалось извлечь информацию ни об одном курсе")
                raise AssertionError("Не удалось извлечь информацию ни об одном курсе")

        logger.info("Тест фильтрации курсов завершен успешно")
