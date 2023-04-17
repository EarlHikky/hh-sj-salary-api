# Сравниваем вакансии программистов

Скрипт вывод в консоль информацию о средней зарплате для разных языков программирования по Москве на сервисах [HeadHunter](https://hh.ru/) и [SuperJob](https://www.superjob.ru/).

### Как установить

Для запуска сайта Python (версия >= 3.6) должен быть установлен.

1. Скачайте код с GitHub.  
   
2. Установите зависимости:
```console
pip install -r requirements.txt
```
3. Определите переменные-окружения. Для этого создайте файл `.env` в каталоге скрипта и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.
- `SJ_SECRET_KEY=`[API ключ SuperJob](https://api.superjob.ru/)

### Запуск

```console
python get_stats.py
```
### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).