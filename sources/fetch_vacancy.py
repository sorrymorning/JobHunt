import requests
from bs4 import BeautifulSoup

def fetch_vacancy(vacancy):
    url = vacancy.url
    description = ""
    if url.find('habr') != -1:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text,'lxml')
            description = soup.find(class_='vacancy-description__text')
            description = description.text
        else:
            print(f"Ошибка запроса: {response.status_code}")

    elif url.find('hh.ru') != -1:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            skills = [skill['name'] for skill in data.get('key_skills', [])]
            description = data.get('description')
            description += " " + " ".join(skills)
        else:
            print(f"Ошибка запроса hh: {response.status_code}")
    else:
        print(f"Неправильный URL: {url}")

    return description
