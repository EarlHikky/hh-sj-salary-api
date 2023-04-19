import requests


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
