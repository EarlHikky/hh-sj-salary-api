from itertools import count

from get_stats_utils import get_response

AREA = 1  # Moscow
PERIOD = 30  # Days
PROFESSIONAL_ROLE = 96  # 'Programmer, developer'
PER_PAGE = 100
HH_API_URL = 'https://api.hh.ru/vacancies/'


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


if __name__ == '__main__':
    get_hh_vacancies()
