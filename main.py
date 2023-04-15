import requests
from collections import defaultdict
from itertools import count
from pprint import pprint

AREA = 1  # Moscow
PERIOD = 30  # Days
PROFESSIONAL_ROLE = 96  # ~= 'Programmer, developer'
PER_PAGE = 100
URL = 'https://api.hh.ru/vacancies/'
PARAMS = {'professional_role': PROFESSIONAL_ROLE, 'area': AREA, 'period': PERIOD, 'per_page': PER_PAGE}
LANGUAGES = [
    'JavaScript', 'Java', 'Python', 'Ruby',
    'PHP', 'C++', 'C#', 'C', 'Go', 'Scala',
]


def get_response(page, language):
    """Get a response from the HeadHunter"""
    PARAMS.update(text=language, page=page)
    response = requests.get(URL, PARAMS)
    response.raise_for_status()
    vacancies = response.json()
    return vacancies['items'], vacancies['pages'], vacancies['found']


def get_vacancies(language):
    """Get all vacancies for a language"""
    vacancies_list = []
    for page in count(0):
        vacancies, check, vacancies_found = get_response(page, language)
        vacancies_list.extend(vacancies)
        if page >= check - 1:
            break
    return vacancies_list, vacancies_found


def get_vacancies_stats():
    """Get a stats for LANGUAGES"""
    vacancies_stats = defaultdict(dict)
    for language in LANGUAGES:
        vacancies, vacancies_found = get_vacancies(language)
        average_salary, vacancies_processed = get_average_salary(vacancies)
        vacancies_stats[language]['vacancies_found'] = vacancies_found
        vacancies_stats[language]['average_salary'] = average_salary
        vacancies_stats[language]['vacancies_processed'] = vacancies_processed
    return dict(vacancies_stats)


def get_average_salary(vacancies):
    """Get average salary for a language in RUB"""
    average_salary = []
    vacancies_processed = 0
    for vacancy in vacancies:
        if not vacancy['salary'] or vacancy['salary']['currency'] != 'RUR':
            continue
        average_salary.append(predict_rub_salary(vacancy['salary']))
        vacancies_processed += 1
    return int(sum(average_salary) / len(average_salary)), vacancies_processed


def predict_rub_salary(vacancy):
    """Returns average salary for a vacancy in RUB"""
    salary_from = vacancy['from']
    salary_to = vacancy['to']
    if salary_from and salary_to:
        predicted_salary = (salary_from + salary_to) / 2
    elif salary_from:
        predicted_salary = salary_from * 1.2
    elif salary_to:
        predicted_salary = salary_to * 0.8
    else:
        return
    return predicted_salary


def main():
    pass


if __name__ == '__main__':
    pprint(get_vacancies_stats())
    # main()
