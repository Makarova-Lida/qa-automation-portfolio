import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
# импорт для работы с селектами
from selenium.webdriver.support.select import Select
# импорт для работы с клавиатурой
from selenium.webdriver import Keys

options = Options()
options.add_argument('--window-size=1920x1080')

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
actions = ActionChains(driver)

def case_1():
    actions = ActionChains(driver)
    print("Запуск case_1: Поиск issues с 'bug' в заголовке...")
    SEARCH_INPUT_LOCATOR = ("xpath", '//input[@id="repository-input"]')

    driver.get("https://github.com/microsoft/vscode/issues")
    time.sleep(3)
    search_input = driver.find_element(*SEARCH_INPUT_LOCATOR)

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

    print("\nТест на паузе. Проверьте результаты в браузере.")
    print("Нажмите Enter в этой консоли, чтобы продолжить...")
    input()
    print("Case 1 завершен.")

def case_2():
    actions = ActionChains(driver)

    print("Запуск case_2: Фильтрация по автору bpasero...")
    AUTHOR_LOCATOR = ("xpath", "//span[text()='Author']")
    SEARCH_LOCATOR = ("xpath", '//input[@placeholder="Filter authors"]')
    AUTHOR_LOCATOR_BRASERO = ("xpath", "//span[text()='bpasero']")

    driver.get("https://github.com/microsoft/vscode/issues")
    time.sleep(3)
    author = driver.find_element(*AUTHOR_LOCATOR)
    author.click()
    time.sleep(3)
    search_input = driver.find_element(*SEARCH_LOCATOR)

    actions \
        .click(search_input) \
        .send_keys("bpasero") \
        .perform()
    time.sleep(3)
    driver.find_element(*AUTHOR_LOCATOR_BRASERO).click()

    print("\nТест на паузе. Проверьте фильтрацию по автору.")
    print("Нажмите Enter в этой консоли, чтобы продолжить...")
    input()
    print("Case 2 завершен.")

def case_3():
    actions = ActionChains(driver)
    print("Запуск case_3: Расширенный поиск на GitHub...")
    SELECT_LANGUAGE_LOCATOR = ("xpath", '//select[@id="search_language"]')
    STARS_LOCATOR = ("xpath", '//input[@id="search_stars"]')
    NAME_FILE_LOCATOR = ("xpath", '//input[@id="search_filename"]')
    SEARCH_LOCATOR = ("xpath", '//button[@class="btn flex-auto"][1]')

    driver.get("https://github.com/search/advanced")
    time.sleep(3)

    # Выбор языка Python
    select_language = Select(driver.find_element(*SELECT_LANGUAGE_LOCATOR))
    select_language.select_by_visible_text("Python")

    # Ввод количества звезд
    stars_input = driver.find_element(*STARS_LOCATOR)
    actions.click(stars_input).send_keys(">20000").perform()

    # Ввод имени файла
    name_file = driver.find_element(*NAME_FILE_LOCATOR)
    actions.click(name_file).send_keys("environment.yml").perform()

    time.sleep(3)
    driver.find_element(*SEARCH_LOCATOR).click()

    print("\nТест на паузе. Проверьте результаты расширенного поиска.")
    print("Нажмите Enter в этой консоли, чтобы продолжить...")
    input()
    print("Case 3 завершен.")

def case_4():
    actions = ActionChains(driver)
    print("Запуск case_4: ")
    MENU_BUTTON_LOCATOR = ("xpath", '//button[@aria-label="Показать фильтр"]')
    PROF_LOCATOR = ("xpath", '//button[contains(@class, "programs-filter-group__tab") and .//span[contains(text(), "Профессия")]]')
    DLIT_LOCATOR = ("xpath", '//button[.//span[normalize-space(text())="От 6 до 12 мес."]]')
    BUTTON_LOCATOR = ("xpath", '//button[normalize-space(text())="Применить"]')
    driver.get("https://skillbox.ru/code/")
    driver.find_element(*MENU_BUTTON_LOCATOR).click()
    time.sleep(3)

    prof_button = driver.find_element(*PROF_LOCATOR)
    actions.move_to_element(prof_button).click_and_hold().release().perform()

    dlit_button = driver.find_element(*DLIT_LOCATOR)
    actions.move_to_element(dlit_button).click_and_hold().release().perform()
    time.sleep(3)
    driver.find_element(*BUTTON_LOCATOR).click()

    print("\nТест на паузе. Проверьте результаты расширенного поиска.")
    print("Нажмите Enter в этой консоли, чтобы продолжить...")
    input()
    print("Case 4 завершен.")

def case_5():
    print("Запуск case_5: Проверка наведения на график коммитов..")
    driver.get("https://github.com/microsoft/vscode/graphs/commit-activity")
    time.sleep(3)
    GRAPH_LOCATOR = ('css selector', '.highcharts-point.highcharts-color-0')
    all_graph_element = driver.find_elements(*GRAPH_LOCATOR)
    number = len(all_graph_element) // 2
    graph_element = all_graph_element[number]
    driver.execute_script("arguments[0].scrollIntoView();", graph_element)
    actions = ActionChains(driver)
    actions.move_to_element(graph_element).pause(2).perform()
    time.sleep(3)
    print("\nПроверьте появилась ли всплывающая информация")
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
    print("=" * 50)
    print("МЕНЮ АВТОТЕСТОВ GitHub")

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





