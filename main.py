from pprint import pprint

import requests

url = 'https://api.hh.ru/vacancies/'
languages = [
    'JavaScript', 'Java', 'Python', 'Ruby',
    'PHP', 'C++', 'C#', 'C', 'Go', 'Scala'
]

area = 1
period = 30
professional_role = 96

# text = 'Python'
# professional_roles = {'id': 96}, {'name': ''}
# professional_role = "Программист, разработчик"
# params = {'search_field': 'name', 'text': text, 'area': area, 'period': period}
# params = {'professional_roles': 96}
params = {'professional_role': professional_role, 'area': area, 'period': period}


def get_vacancies_for_lang():
    vacancies = dict()
    for language in languages:
        params.update(text=language)
        response = requests.get(url, params)
        response.raise_for_status()
        vacancies.setdefault(language, response.json()['found'])
    print(vacancies)


def get_vacancies_for_python(language):
    params.update(text=language)
    response = requests.get(url, params)
    response.raise_for_status()
    for vacancy in response.json()['items']:
        if vacancy['salary']:
            print(predict_rub_salary(vacancy['salary']))


def predict_rub_salary(vacancy):
    salary_from = vacancy['from']
    salary_to = vacancy['to']
    if not vacancy['currency'] == 'RUR':
        return
    elif salary_from and salary_to:
        predicted_salary = (salary_from + salary_to) / 2
    elif salary_from:
        predicted_salary = salary_from * 1.2
    elif salary_to:
        predicted_salary = salary_to * 0.8
    else:
        return
    return predicted_salary


# pprint(response.json()) {'from': 100000, 'to': 180000, 'currency': 'RUR', 'gross': False}
# get_vacancies_for_python()
get_vacancies_for_python('python')
