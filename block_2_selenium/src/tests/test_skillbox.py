from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class TestSkillbox:
    # Тесты для сайта Skillbox

    def test_dummy_1(self):
        # Тест-заглушка 1"
        pass

    def test_dummy_2(self):
        # Тест-заглушка 2
        pass

    def test_skillbox_title(self):
        # Тест проверки заголовка сайта Skillbox
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Автоматическое управление драйверами
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            driver.get("https://skillbox.ru")
            expected_title = "Skillbox"
            assert expected_title in driver.title, f"Заголовок не совпадает. Актуальный: {driver.title}"
            print(f"Успех! Заголовок страницы: {driver.title}")
        finally:
            driver.quit()


def test_another_dummy():
    # Еще один тест-заглушка
    pass
