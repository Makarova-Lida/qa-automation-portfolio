import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
#импорт для работы с селектами
from selenium.webdriver.support.select import Select
#импорт для работы с клавиатурой
from selenium.webdriver import Keys

from selenium.webdriver.support import expected_conditions as EC


options = Options()
options.add_argument('--window-size=1920x1080')

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)
actions = ActionChains(driver)

def case_1():
    actions = ActionChains(driver)
    print("Запуск case_1: Поиск issues с 'bug' в заголовке и проверка результатов")
    SEARCH_INPUT_LOCATOR = ("xpath", '//input[@id="repository-input"]')

    driver.get("https://github.com/microsoft/vscode/issues")
    time.sleep(3)

    search_input = wait.until(EC.presence_of_element_located(SEARCH_INPUT_LOCATOR))
    actions \
    .click(search_input) \
    .pause(3) \
    .key_down(Keys.CONTROL) \
    .send_keys('a') \
    .key_up(Keys.CONTROL) \
    .send_keys(Keys.DELETE) \
    .send_keys("in:title bug") \
    .send_keys(Keys.ENTER) \
    .perform()
    # Ждем загрузки результатов
    time.sleep(3)
    # Получаем все названия задач
    issue_titles = driver.find_elements("xpath", '//a[contains(@data-hovercard-url, "issues")]')
    # Проверяем каждую задачу на наличие слова 'bug' (без учета регистра)
    all_contain = True
    bug_count = 0
    for i, title_element in enumerate(issue_titles):
        title_text = title_element.text.lower()
        if 'bug' in title_text:
            bug_count += 1
            print(f"Задача {i}: '{title_element.text}' - содержит 'bug'")
        else:
            all_contain = False
            print(f"Задача {i}: '{title_element.text}' - НЕ содержит 'bug'!")

    # Проверяем условие
    if all_contain:
        print(f"\nТЕСТ ПРОЙДЕН: Все задачи содержат слово 'bug' в заголовке")
    else:
        print(f"\nТЕСТ НЕ ПРОЙДЕН: Не все задачи содержат слово 'bug' в заголовке")

def case_2():
    actions = ActionChains(driver)
    print("Запуск case_2: Фильтрация по автору bpasero и проверка результатов")
    AUTHOR_LOCATOR = ("xpath", "//span[text()='Author']")
    SEARCH_LOCATOR = ("xpath", '//input[@placeholder="Filter authors"]')
    AUTHOR_BPASERO_LOCATOR = ("xpath", "//span[text()='bpasero']")

    ISSUES_LOCATOR = ("xpath", "//a[contains(@class, 'authorCreatedLink') and text()='bpasero']")
    FILTER_AUTHOR_BPASERO_LOCATOR = ("xpath", "//input[@id='repository-input' and contains(@value, 'bpasero')]")
    driver.get("https://github.com/microsoft/vscode/issues")
    time.sleep(3)

    author = wait.until(EC.element_to_be_clickable(AUTHOR_LOCATOR))
    author.click()
    time.sleep(3)
    # Вводим имя автора в поиск
    search_input = wait.until(EC.presence_of_element_located(SEARCH_LOCATOR))
    actions \
        .click(search_input) \
        .send_keys("bpasero") \
        .perform()
    driver.find_element(*AUTHOR_BPASERO_LOCATOR).click()
    # Ждем загрузки результатов
    time.sleep(3)
    # Получаем все задачи
    issues = driver.find_elements(*ISSUES_LOCATOR)
    # Получаем информацию об авторе из фильтра
    element = driver.find_element(*FILTER_AUTHOR_BPASERO_LOCATOR)
    value = element.get_attribute('value')
    if 'bpasero' in value:
        print("Фильтр по автору применен и содержит 'bpasero' в value")
        print(f"Полное значение value: {value}")
        if len(issues) > 0:
            print(f"Найдено задач: {len(issues)}")
            print(f"\nТЕСТ ПРОЙДЕН")
            return True
        else:
            print("После фильтрации не найдено задач")
            return False
    else:
        print(" Фильтр по автору не применен или не содержит 'bpasero'")
        print(f"\nТЕСТ НЕ ПРОЙДЕН")

def case_3():
    actions = ActionChains(driver)
    print("Запуск case_3: Расширенный поиск репозиториев с Python, >20000 звезд и файлом environment.yml")
    SELECT_LANGUAGE_LOCATOR = ("xpath", '//select[@id="search_language"]')
    STARS_LOCATOR = ("xpath", '//input[@id="search_stars"]')
    NAME_FILE_LOCATOR = ("xpath", '//input[@id="search_filename"]')
    SEARCH_LOCATOR = ("xpath", '//button[@class="btn flex-auto"][1]')

    REPOSITORIES_LOCATOR = ("xpath", '//div[@class="Box-sc-62in7e-0 fXzjPH"]')
    REPO_STARS_LOCATOR = ("xpath", './/a[contains(@href, "stargazers")]')
    REPO_TITLE_LOCATOR = ("css selector", 'a.prc-Link-Link-9ZwDx span.search-match')
    REPO_LINK_LOCATOR = ("xpath", './/a[contains(@class, "prc-Link-Link")]')
    driver.get("https://github.com/search/advanced")
    time.sleep(3)

    # Выбор языка Python
    select_language = Select(wait.until(EC.presence_of_element_located(SELECT_LANGUAGE_LOCATOR)))
    select_language.select_by_visible_text("Python")

    # Ввод количества звезд
    stars_input = wait.until(EC.presence_of_element_located(STARS_LOCATOR))
    actions.click(stars_input).send_keys(">20000").perform()

    # Ввод имени файла
    name_file = wait.until(EC.presence_of_element_located(NAME_FILE_LOCATOR))
    actions.click(name_file).send_keys("environment.yml").perform()

    # Нажатие на кнопку Поиск
    search_button = wait.until(EC.element_to_be_clickable(SEARCH_LOCATOR))
    search_button.click()

    # Получаем количество найденных репозиториев
    repositories = driver.find_elements(*REPOSITORIES_LOCATOR)
    print(f"\nНайдено репозиториев: {len(repositories)}")

    # Проверяем звезды для каждого репозитория
    all_stars_valid = True
    count = 0

    for i, repository in enumerate(repositories, 1):
        ## Получаем название репозитория
        repo_title_elem = repository.find_element(*REPO_TITLE_LOCATOR)
        repo_name = repo_title_elem.text

        # Получаем ссылку на репозиторий
        repo_link_elem = repository.find_element(*REPO_LINK_LOCATOR)
        repo_url = repo_link_elem.get_attribute('href')

        # Получаем количество звезд
        stars_elem = repository.find_element(*REPO_STARS_LOCATOR)
        stars_text = stars_elem.text.strip()

        stars_value = 0
        if stars_text:
            if 'k' in stars_text.lower():
                stars_value = float(stars_text.lower().replace('k', '')) * 1000
            else:
                stars_text = stars_text.replace(',', '')
                stars_value = float(stars_text)

        # Проверяем условие >20000
        stars_valid = stars_value > 20000
        if not stars_valid:
            all_stars_valid = False

        # Выводим информацию
        print(f"Репозиторий #{i} Название: {repo_name}")
        print(f"  Звезды: {stars_text} ({stars_value:.0f})")
        print(f"  Соответствие условию (>20000): {stars_valid}")
        print("-" * 40)
        count += 1

    if all_stars_valid:
        print("ТЕСТ ПРОЙДЕН. ВСЕ проверенные репозитории соответствуют условию (>20000 звезд)")
    else:
        print("ТЕСТ НЕ ПРОЙДЕН. НЕ ВСЕ репозитории соответствуют условию (>20000 звезд)")


def case_4():
    actions = ActionChains(driver)
    print("Запуск case_4: Фильтрация курсов на Skillbox")
    MENU_BUTTON_LOCATOR = ("xpath", '//button[@aria-label="Показать фильтр"]')
    PROF_LOCATOR = ("xpath", '//button[contains(@class, "programs-filter-group__tab") and .//span[contains(text(), "Профессия")]]')
    DLIT_LOCATOR = ("xpath", '//button[.//span[normalize-space(text())="От 6 до 12 мес."]]')
    COURSE_CARDS_LOCATOR = ("xpath", '//div[contains(@class, "product-card-new__info")]')
    BUTTON_LOCATOR = ("xpath", '//button[normalize-space(text())="Применить"]')

    driver.get("https://skillbox.ru/code/")
    # Открыть фильтр
    filter_bt = wait.until(EC.element_to_be_clickable(MENU_BUTTON_LOCATOR))
    filter_bt.click()
    time.sleep(3)
    # Выбрать "Профессия"
    profession = wait.until(EC.element_to_be_clickable(PROF_LOCATOR))
    profession.click()
    # Выбрать длительность 6-12 месяцев
    duration = wait.until(EC.element_to_be_clickable(DLIT_LOCATOR))
    duration.click()

    time.sleep(3)
    apply_btn = wait.until(EC.element_to_be_clickable(BUTTON_LOCATOR))
    apply_btn.click()
    # вывести информацию
    courses = driver.find_elements(*COURSE_CARDS_LOCATOR)

    if courses:
        print("\n" + "=" * 50)
        print("НАЙДЕННЫЕ КУРСЫ:")
        print("=" * 50)

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
                print(f"\nКурс #{i}: Ошибка при извлечении данных: {str(e)}")
                continue
        print(f"\nТЕСТ ПРОЙДЕН")
    else:
        print("\nТЕСТ НЕ ПРОЙДЕН")


def case_5():

    print("Запуск case_5: Проверка наведения на график коммитов...")
    #Открываем страницу с графиком
    driver.get("https://github.com/microsoft/vscode/graphs/commit-activity")
    time.sleep(3)
    print("Страница загружена")

    #Находим элементы графика
    all_graph_elements = driver.find_elements('css selector', '.highcharts-point.highcharts-color-0')

    #Выбираем элемент в середине графика
    middle_index = len(all_graph_elements) // 2
    graph_element = all_graph_elements[middle_index]

    #Прокручиваем и наводим курсор
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", graph_element)
    time.sleep(1)
    actions = ActionChains(driver)
    actions.move_to_element(graph_element).pause(1).perform()
    print(f"Наведено на элемент графика #{middle_index}")

    # Ждем появления тултипа и извлекаем значение
    strong_element = WebDriverWait(driver, 3).until(
    EC.visibility_of_element_located(('css selector', '.highcharts-tooltip strong')))
    value = strong_element.text.strip()
    print(f"✓ Найдено значение в <strong>: {value}")

    print("\nПроверьте соответствует ли всплывающая информация и найденное значение")
    input("Нажмите Enter...")
    print("Тест завершен")


case_map = {
    1: case_1,
    2: case_2,
    3: case_3,
    4: case_4,
    5: case_5,
    }

def main():

    while True:
        print("\n" + "-" * 40)
        print("ВЫБЕРИТЕ ТЕСТ ДЛЯ ЗАПУСКА:")
        print("1. Поиск issues с 'bug' в заголовке")
        print("2. Фильтрация issues по автору 'bpasero'")
        print("3. Расширенный поиск репозиториев (Python, >20000 звезд, environment.yml)")
        print("4. Фильтрация курсов на Skillbox")
        print("5. Проверка графика коммитов")
        print("0. Выход и закрытие браузера")
        try:
            choice = input("\nВыберите действие (0-5): ")
            if choice == '0':
                driver.quit()
                print("Выход из программы")
                break
            if choice not in ['1', '2', '3', '4', '5']:
                print("Ошибка: введите число от 0 до 5")
                continue
            choice_num = int(choice)
            if choice_num in case_map:
                # Вызываем функцию по ключу
                case_map[choice_num]()
            else:
                print(f"Некорректный номер. Доступны: {list(case_map.keys())}")
        except ValueError:
            print("Пожалуйста, введите число")

if __name__ == "__main__":
    main()





