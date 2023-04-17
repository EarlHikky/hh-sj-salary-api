from pprint import pprint
import re
from typing import Any

import requests
from environs import Env

env = Env()
env.read_env()

PROFESSION = 48
TOWN = 4

SJ_API_URL = 'https://api.superjob.ru/2.0/vacancies/'
# SJ_API_URL = 'https://api.superjob.ru/doc/'
HEADERS = {'X-Api-App-Id': env('SJ_SECRET_KEY')}
PARAMS = {'catalogues': PROFESSION, 'town': TOWN}

response = requests.get(SJ_API_URL, headers=HEADERS, params=PARAMS)
# response = requests.get(SJ_API_URL, headers=HEADERS)
response.raise_for_status()


# pprint(type(response.json()))

# def predict_rub_salary_for_superJob(vacancy):
#     """Returns average salary for a vacancy in RUB"""
#     salary_from = vacancy['payment_from']
#     salary_to = vacancy['payment_to']
#     if salary_from and salary_to:
#         predicted_salary = (salary_from + salary_to) / 2
#     elif salary_from:
#         predicted_salary = salary_from * 1.2
#     elif salary_to:
#         predicted_salary = salary_to * 0.8
#     else:
#         return
#     return predicted_salary

def predict_rub_salary_for_superJob(vacancy: dict) -> float | None | Any:
    """Returns average salary for a vacancy in RUB
    :return: float
    :type vacancy: dict
    """
    salary_from = vacancy.get('payment_from') or vacancy.get('from')
    print(salary_from)
    salary_to = vacancy.get('payment_to') or vacancy.get('to')
    print(salary_to)
    pprint(vacancy)
    if salary_from and salary_to:
        predicted_salary = (salary_from + salary_to) / 2
    elif salary_from:
        predicted_salary = salary_from * 1.2
    elif salary_to:
        predicted_salary = salary_to * 0.8
    else:
        return None
    return predicted_salary


for vacancy in response.json()['objects']:
    pprint(predict_rub_salary_for_superJob(vacancy))
    # print(vacancy['profession'], vacancy['town']['title'], sep=', ')

'''
'payment_from': 0,
            'payment_to': 200000,
 'total': 118}
'profession':
 'catalogues': [{'id': 1,
                              'key': 1,
                              'positions': [{'id': 5,
                                             'key': 5,
                                             'title': 'Диспетчерская служба'}],
                              'title': 'Административная работа, секретариат, '
                                       'АХО'},
                             {'id': 438,
                              'key': 438,
                              'positions': [{'id': 34,
                                             'key': 34,
                                             'title': 'Call Center'},
                                            {'id': 470,
                                             'key': 470,
                                             'title': 'Начало карьеры, мало '
                                                      'опыта'}],
                              'title': 'Продажи'},
                             {'id': 234,
                              'key': 234,
                              'positions': [{'id': 256,
                                             'key': 256,
                                             'title': 'Телемаркетинг'}],
                              'title': 'Маркетинг, реклама, PR'}],
'''
