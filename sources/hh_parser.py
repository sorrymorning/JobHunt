import requests
from utils.crud import add_vacancy


def get_vacancies_hh(keyword:str,session):
    url = "https://api.hh.ru/vacancies"
    headers = {
        "User-Agent": "my-app"  # hh.ru требует User-Agent
    }
    params = {
        "text": keyword,
        "area": 88,      
        "per_page": 20  
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        vacancies = data.get("items", [])

        for vacancy in vacancies:
            add_vacancy(
                session=session,
                title=vacancy.get('name'),
                company=vacancy.get('employer', {}).get('name'),
                # location = vacancy.get('area').get('name'),
                url = "https://api.hh.ru/vacancies/" + vacancy.get('id'),
                description = vacancy.get('snippet').get('responsibility'),
                technologies = ''
            )
    else:
        print(f"Ошибка запроса: {response.status_code}")



