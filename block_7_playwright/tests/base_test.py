
class BaseTest:
    """Базовый класс для всех тестов"""

    def setup_method(self):
        print("\n" + "=" * 50)
        print("НАЧАЛО ТЕСТА")

    def teardown_method(self):
        print("КОНЕЦ ТЕСТА")
        print("=" * 50)
