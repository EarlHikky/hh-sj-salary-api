import os
from collections import defaultdict
from dotenv import load_dotenv
from terminaltables import DoubleTable

from get_stats_utils import get_average_salary
from hh_api import get_hh_vacancies
from sj_api import get_sj_vacancies

LANGUAGES = [
    'JavaScript', 'Java', 'Python', 'Ruby',
    'PHP', 'C++', 'C#', 'C', 'Go', 'Scala',
]


def get_vacancies_stats(get_vacancies, secret_key):
    """Get a stats for LANGUAGES"""
    vacancies_stats = defaultdict(dict)
    for language in LANGUAGES:
        vacancies, vacancies_found = get_vacancies(language, secret_key)
        average_salary, vacancies_processed = get_average_salary(vacancies)
        vacancies_stats[language]['vacancies_found'] = vacancies_found
        vacancies_stats[language]['vacancies_processed'] = vacancies_processed
        vacancies_stats[language]['average_salary'] = average_salary
    return dict(vacancies_stats)


def main():
    load_dotenv()
    sj_secret_key = os.environ.get('SJ_SECRET_KEY')
    hh_vacancies_stats = get_vacancies_stats(get_hh_vacancies, '')
    sj_vacancies_stats = get_vacancies_stats(get_sj_vacancies, sj_secret_key)
    for index, stats in enumerate((hh_vacancies_stats, sj_vacancies_stats)):
        table_title = ('+HeadHunter Moscow+', '+SuperJob Moscow+')[index]
        table_values = [['Язык программирования', 'Найдено вакансий', 'Обработано вакансий', 'Средняя зарплата'],
                      *[[k, *v.values()] for k, v in stats.items()]]
        table_instance = DoubleTable(table_values, table_title)
        print(table_instance.table)
        print()
    # print(sj_vacancies_stats)

if __name__ == '__main__':
    main()
