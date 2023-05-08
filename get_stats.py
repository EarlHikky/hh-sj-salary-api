import os
import requests
from collections import defaultdict
from terminaltables import DoubleTable
from dotenv import load_dotenv
from itertools import count

LANGUAGES = [
    'JavaScript', 'Java', 'Python', 'Ruby',
    'PHP', 'C++', 'C#', 'C', 'Go', 'Scala',
]

AREA = 1  # Moscow
PERIOD = 30  # Days
PROFESSIONAL_ROLE = 96  # 'Programmer, developer'
PER_PAGE = 100
HH_API_URL = 'https://api.hh.ru/vacancies/'

TOWN = 4  # Moscow
PROFESSION = 48  # 'Programmer, developer'
SJ_API_URL = 'https://api.superjob.ru/2.0/vacancies/'


def predict_rub_salary(vacancy):
    """Returns average salary for a vacancy in RUB"""
    salary_from = vacancy.get('payment_from') or vacancy.get('salary', dict()).get('from')
    salary_to = vacancy.get('payment_to') or vacancy.get('salary', dict()).get('to')
    if salary_from and salary_to:
        predicted_salary = (salary_from + salary_to) / 2
    elif salary_from:
        predicted_salary = salary_from * 1.2
    elif salary_to:
        predicted_salary = salary_to * 0.8
    else:
        return 0, 0
    return predicted_salary, 1


def currency_check(vacancy):
    """Checking a type of currency"""
    if not vacancy.get('salary'):
        return vacancy.get('currency') == 'rub'
    else:
        return vacancy['salary']['currency'] == 'RUR'


def get_average_salary(vacancies):
    """Get average salary for a language in RUB"""
    average_salaries = []
    vacancies_processed = 0
    for vacancy in vacancies:
        if not currency_check(vacancy):
            continue
        salary, counter = predict_rub_salary(vacancy)
        average_salaries.append(salary)
        vacancies_processed += counter
    try:
        return int(sum(average_salaries) / len(average_salaries)), vacancies_processed
    except ZeroDivisionError:
        return 0, 0


def get_response(url, headers, params):
    """Get a response from a service"""
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    raw_vacancies = response.json()
    vacancies = raw_vacancies.get('items') or raw_vacancies.get('objects')
    vacancies_found = raw_vacancies.get('total') or raw_vacancies.get('found') or 0
    available_vacancies_check = raw_vacancies.get('pages') or raw_vacancies.get('more')
    return vacancies, available_vacancies_check, vacancies_found


def get_sj_vacancies(language):
    """Get all vacancies for a language from the SuperJob"""
    headers = {'X-Api-App-Id': sj_api_key}
    vacancies_roster = []
    params = {'catalogues': PROFESSION, 'keyword': language, 'town': TOWN,
              'count': PER_PAGE}
    for page in count(0):
        params['page'] = page
        vacancies, available_vacancies_check, vacancies_found = get_response(SJ_API_URL, headers, params)
        vacancies_roster.extend(vacancies)
        if not available_vacancies_check:
            break
    return vacancies_roster, vacancies_found


def get_hh_vacancies(language):
    """Get all vacancies for a language from the HeadHunter"""
    params = {'professional_role': PROFESSIONAL_ROLE, 'area': AREA, 'text': language, 'period': PERIOD,
              'per_page': PER_PAGE}
    vacancies_roster = []
    for page in count(0):
        params['page'] = page
        vacancies, available_vacancies_check, vacancies_found = get_response(HH_API_URL, {}, params)
        vacancies_roster.extend(vacancies)
        if page >= available_vacancies_check - 1:
            break
    return vacancies_roster, vacancies_found


def get_vacancies_stats(get_vacancies):
    """Get a stats for LANGUAGES"""
    vacancies_stats = defaultdict(dict)
    for language in LANGUAGES:
        vacancies, vacancies_found = get_vacancies(language)
        average_salary, vacancies_processed = get_average_salary(vacancies)
        vacancies_stats[language]['vacancies_found'] = vacancies_found
        vacancies_stats[language]['vacancies_processed'] = vacancies_processed
        vacancies_stats[language]['average_salary'] = average_salary
    return dict(vacancies_stats)


def main():
    hh_vacancies_stats = get_vacancies_stats(get_hh_vacancies)
    sj_vacancies_stats = get_vacancies_stats(get_sj_vacancies)
    for index, stats in enumerate((hh_vacancies_stats, sj_vacancies_stats)):
        table_title = ('+HeadHunter Moscow+', '+SuperJob Moscow+')[index]
        table_values = [['Язык программирования', 'Найдено вакансий', 'Обработано вакансий', 'Средняя зарплата'],
                        *[[k, *v.values()] for k, v in stats.items()]]
        table_instance = DoubleTable(table_values, table_title)
        print(table_instance.table)
        print()


if __name__ == '__main__':
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if not os.path.exists(env_path):
        raise FileNotFoundError('.env does not exist')
    load_dotenv(env_path)
    sj_api_key = os.environ.get('SJ_SECRET_KEY')
    main()
