from collections import defaultdict
from pprint import pprint
import requests


def get_response(url, params, language):
    params.update(text=language)
    response = requests.get(url, params)
    response.raise_for_status()
    return response.json()


def get_vacancies(url, params, languages):
    vacancies_stats = defaultdict(dict)
    for language in languages:
        vacancies = get_response(url, params, language)
        average_salary, vacancies_processed = get_average_salary(vacancies)
        vacancies_stats[language].setdefault('vacancies_found', vacancies['found'])
        vacancies_stats[language].setdefault('average_salary', average_salary)
        vacancies_stats[language].setdefault('vacancies_processed', vacancies_processed)
    return dict(vacancies_stats)


def get_average_salary(vacancies):
    average_salary = []
    vacancies_processed = 0
    for vacancy in vacancies['items']:
        if not vacancy['salary'] or vacancy['salary']['currency'] != 'RUR':
            continue
        average_salary.append(predict_rub_salary(vacancy['salary']))
        vacancies_processed += 1
    return sum(average_salary), vacancies_processed


def predict_rub_salary(vacancy):
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
    return int(predicted_salary)


def main():
    url = 'https://api.hh.ru/vacancies/'
    area = 1
    period = 30
    professional_role = 96
    params = {'professional_role': professional_role, 'area': area, 'period': period}
    languages = [
        'JavaScript', 'Java', 'Python', 'Ruby',
        'PHP', 'C++', 'C#', 'C', 'Go', 'Scala',
    ]
    pprint(get_vacancies(url, params, languages))


if __name__ == '__main__':
    main()
