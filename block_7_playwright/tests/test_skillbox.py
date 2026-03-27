import re
import logging
import allure

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
    def test_filter_courses(self, page):
        """Фильтрация курсов на Skillbox"""

        with allure.step("Подготовка теста"):
            logger.info("Запуск case_4: Фильтрация курсов на Skillbox")

        # Открыть страницу
        with allure.step("Открытие страницы курсов"):
            logger.info("Открываю страницу курсов Skillbox")
            page.goto("https://skillbox.ru/code/")
            # page.wait_for_load_state('networkidle')
            logger.debug(f"Текущий URL: {page.url}")
            # Скриншот начальной страницы
            allure.attach(
                page.screenshot(full_page=True),
                name="page_loaded",
                attachment_type=allure.attachment_type.PNG)

        # Выбрать "Профессия"
        with allure.step("Выбор типа курса: Профессия"):
            logger.info("Выбираю тип курса: Профессия")
            page.locator('button:has-text("Профессия")').click()
            logger.info("✓ Тип 'Профессия' выбран")

        # Выбрать длительность 6-12 месяцев
        with allure.step("Выбор длительности: От 6 до 12 месяцев"):
            logger.info("Выбираю длительность: От 6 до 12 мес.")
            page.locator('button:has-text("Длительность")').click()
            # page.locator('li.ui-round-select__item:has-text("От 6 до 12 мес.")').wait_for(state="visible")
            page.locator('li.ui-round-select__item:has-text("От 6 до 12 мес.")').click()
            logger.info("✓ Длительность 'От 6 до 12 мес.' выбрана")

        # Обновление результатов
        with allure.step("Ожидание обновления списка курсов"):
            page.wait_for_timeout(2000)
            logger.info("Ожидаю обновления списка курсов")

        # вывести информацию
        with allure.step("Получение отфильтрованных курсов"):
            # Ищем ВСЕ карточки курсов
            all_cards = page.locator('div.product-card-new__wrapper')
            card_count = all_cards.count()
            logger.info(f"Найдено карточек: {card_count}")

        with allure.step("Анализ найденных курсов"):
            all_correct = True

            for i in range(card_count):
                card = all_cards.nth(i)

                # Название курса
                title_element = card.locator('a.product-card-new__title')
                course_name = title_element.text_content().strip()

                # Длительность
                duration_element = card.locator('li.product-card-new__feature').first
                duration_text = duration_element.text_content().strip()

                # Извлекаем число месяцев из текста
                months = 0
                try:
                    # Ищем число в тексте
                    match = re.search(r'(\d+)\s*мес', duration_text)
                    if match:
                        months = int(match.group(1))
                except:
                    pass

                # Проверяем соответствие фильтру (6-12 месяцев)
                is_correct = 6 <= months <= 12

                print(f"\nКурс #{i + 1}:")
                print(f"  Название: {course_name}")
                print(f"  Длительность: {duration_text} ({months} мес.)")

                if is_correct:
                    print(f"Соответствует фильтру (6-12 месяцев)")
                else:
                    print(f"НЕ соответствует фильтру!")
                    all_correct = False

        # Проверка результата
        if all_correct:
            logger.info("ТЕСТ ПРОЙДЕН: Все курсы соответствуют фильтру длительности")
        else:
            logger.warning("Не все курсы соответствуют фильтру длительности")