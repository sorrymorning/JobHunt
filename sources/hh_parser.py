import requests
from models.vacancy import Vacancy



def read_vacancies_hh(vacancy: Vacancy):

    if vacancy.site == 'hh':
        url = f"https://api.hh.ru/vacancies/{vacancy.id}"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            skills = [skill['name'] for skill in data.get('key_skills', [])]
            desc = data.get('description')
            
            with open(f"sources/tempFiles/{vacancy.id}hh.txt", "w", encoding="utf-8") as f:
                f.write(" ".join(skills))
                f.write(desc)
                
        else:
            print(f"Ошибка запроса: {response.status_code}")
    else:
        print("Не тот сайт")


def get_vacancies_hh(keyword:str,vacans):
    url = "https://api.hh.ru/vacancies"
    headers = {
        "User-Agent": "my-app"  # hh.ru требует User-Agent
    }
    params = {
        "text": keyword,
        "area": 88,      
        "per_page": 10  
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        vacancies = data.get("items", [])

        for vacancy in vacancies:
            vacans.append(Vacancy(
                id=vacancy.get('id'),
                site="hh",
                title=vacancy.get('name'),
                company=vacancy.get('employer', {}).get('name'),
                location = vacancy.get('area').get('name'),
                url = "https://hh.ru/vacancy/" + vacancy.get('id'),
                description = vacancy.get('snippet').get('responsibility')
            ))
    else:
        print(f"Ошибка запроса: {response.status_code}")



