from itertools import count

from get_stats_utils import get_response

TOWN = 4  # Moscow
PROFESSION = 48  # 'Programmer, developer'
PER_PAGE = 100
SJ_API_URL = 'https://api.superjob.ru/2.0/vacancies/'


def get_sj_vacancies(language, secret_key):
    """Get all vacancies for a language from the SuperJob"""
    headers = {'X-Api-App-Id': secret_key}
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


if __name__ == '__main__':
    get_sj_vacancies()