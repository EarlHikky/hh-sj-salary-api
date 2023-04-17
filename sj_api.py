from itertools import count
from environs import Env

from get_stats_utils import get_response

TOWN = 4  # Moscow
PROFESSION = 48  # 'Programmer, developer'
PER_PAGE = 100
SJ_API_URL = 'https://api.superjob.ru/2.0/vacancies/'


def get_sj_vacancies(language):
    """Get all vacancies for a language from the SuperJob"""
    env = Env()
    env.read_env()
    headers = {'X-Api-App-Id': env('SJ_SECRET_KEY')}
    vacancies_list = []
    params = {'catalogues': PROFESSION, 'keyword': language, 'town': TOWN,
              'count': PER_PAGE}
    for page in count(0):
        params['page'] = page
        vacancies, check, vacancies_found = get_response(SJ_API_URL, headers, params)
        vacancies_list.extend(vacancies)
        if not check:
            break
    return vacancies_list, vacancies_found


if __name__ == '__main__':
    get_sj_vacancies()
