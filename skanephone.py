import requests
from bs4 import BeautifulSoup


# Пример функции для проверки регистрации на конкретном сайте
def check_registration(phone_number, url, form_data, check_text):
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    try:
        response = requests.post(url, data=form_data, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            if check_text in soup.text:
                return True
            else:
                return False
        else:
            return None  # Ошибка при запросе
    except requests.RequestException as e:
        print(f'Ошибка при запросе: {e}')
        return None


# Функция для записи результата в файл
def write_result_to_file(phone_number, site, is_registered):
    with open('registration_results.txt', 'a') as file:
        if is_registered:
            file.write(f'На сайте {site} регистрация по номеру {phone_number} обнаружена.\n')
        elif is_registered is None:
            file.write(f'На сайте {site} произошла ошибка при проверке номера {phone_number}.\n')
        else:
            file.write(f'На сайте {site} регистрация по номеру {phone_number} не обнаружена.\n')


# Список сайтов для проверки
sites = [
    {
        'name': 'example1.com',
        'url': 'https://example1.com/register',
        'form_data': {
            'phone': '',  # Здесь будет подставлен номер телефона
            'submit': 'register'
        },
        'check_text': 'номер уже зарегистрирован'
    },
    {
        'name': 'example2.com',
        'url': 'https://example2.com/signup',
        'form_data': {
            'phone_number': '',  # Здесь будет подставлен номер телефона
            'submit': 'sign up'
        },
        'check_text': 'Этот номер уже используется'
    }
    # Добавьте больше сайтов по аналогии
]

# Пример использования функции для нескольких сайтов
phone_number = '1234567890'

for site in sites:
    # Подставляем номер телефона в данные формы
    site['form_data']['phone'] = phone_number if 'phone' in site['form_data'] else phone_number
    site['form_data']['phone_number'] = phone_number if 'phone_number' in site['form_data'] else phone_number

    # Проверка регистрации на текущем сайте
    is_registered = check_registration(phone_number, site['url'], site['form_data'], site['check_text'])

    # Запись результата в файл
    write_result_to_file(phone_number, site['name'], is_registered)

    # Вывод результата в консоль
    if is_registered:
        print(f'Телефонный номер {phone_number} уже зарегистрирован на сайте {site["name"]}.')
    elif is_registered is None:
        print(f'Произошла ошибка при проверке регистрации на сайте {site["name"]}.')
    else:
        print(f'Телефонный номер {phone_number} не зарегистрирован на сайте {site["name"]}.')
