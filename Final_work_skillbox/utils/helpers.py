import re
import random
import string
from datetime import datetime, timedelta


def extract_number_from_price(price_text):
    """Извлечение числа из строки цены (например, '1 200,00₽' -> 1200.00)"""
    if not price_text:
        return 0.0
    # Удаляем все кроме цифр, запятых и точек
    cleaned = re.sub(r'[^\d,]', '', price_text)
    # Заменяем запятую на точку для преобразования в float
    cleaned = cleaned.replace(',', '.')
    try:
        return float(cleaned)
    except:
        return 0.0


def generate_random_string(length=8):
    """Генерация случайной строки"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def generate_random_phone():
    """Генерация случайного телефона"""
    return f"+7{''.join(random.choices(string.digits, k=10))}"


def generate_random_email():
    """Генерация случайного email"""
    return f"test_{generate_random_string(5)}@test.com"


def generate_random_name():
    """Генерация случайного имени"""
    first_names = ["Александр", "Андрей", "Дмитрий", "Сергей", "Максим", "Иван"]
    last_names = ["Иванов", "Петров", "Сидоров", "Кузнецов", "Смирнов", "Попов"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"


def wait_for_ajax(driver, timeout=10):
    """Ожидание завершения AJAX-запросов"""
    try:
        return driver.execute_script("return jQuery.active == 0")
    except:
        return True


def get_future_date(days_ahead=1, format="%d.%m.%Y"):
    """Получить дату в будущем"""
    return (datetime.now() + timedelta(days=days_ahead)).strftime(format)


def calculate_discount(original_price, discount_percent=10):
    """Рассчитать цену со скидкой"""
    if isinstance(original_price, str):
        original_price = extract_number_from_price(original_price)
    return original_price * (1 - discount_percent / 100)


def compare_prices(price1, price2, tolerance=0.01):
    """Сравнить две цены с погрешностью"""
    num1 = extract_number_from_price(price1) if isinstance(price1, str) else price1
    num2 = extract_number_from_price(price2) if isinstance(price2, str) else price2
    return abs(num1 - num2) < tolerance


def take_screenshot(driver, name):
    """Сделать скриншот"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshots/{name}_{timestamp}.png"
    driver.save_screenshot(filename)
    return filename