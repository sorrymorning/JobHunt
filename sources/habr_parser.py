import requests
from bs4 import BeautifulSoup
from models.vacancy import Vacancy

# тут не нужные библы
import re
from collections import Counter

def get_raw_vacancies(vacancy: Vacancy):

    if vacancy.site == "habr":
        url = f"https://career.habr.com/vacancies/{vacancy.id}"
        
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text,'lxml')
            description = soup.find(class_='vacancy-description__text')
            
            with open(f"sources/tempFiles/{vacancy.id}habr.txt", "w", encoding="utf-8") as f:
                f.write(description.text)
                
        else:
            print(f"Ошибка запроса: {response.status_code}")


def extract_skills(text:str,keywords:list[str]) -> list[str]:
    text = text.lower()
    found = []

    for kw in keywords:
        if re.search(rf'\b{re.escape(kw.lower())}\b',text):
            found.append(kw)
    return found


def get_vacancies_habr(job : str,vacancies : list[Vacancy]):
    urls = "https://career.habr.com/vacancies"
    params = {
        "page":1,
        "q": job,
        "qid":1,
        "type": "all"  
    }

    response = requests.get(urls,  params=params)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text,'lxml')
        links = soup.find_all(class_='vacancy-card__title-link')
        companyName = soup.find_all(class_='vacancy-card__company-title')
        locationJob = soup.find_all(class_='vacancy-card__meta')
        if len(links) > 0:
            for index,name in enumerate(links):
                vacancies.append(
                    Vacancy(
                        id=name["href"][name["href"].rfind("/")+1:],
                        site="habr",
                        title=name.text,
                        company = companyName[index].text,
                        location = locationJob[index].text,
                        url=f"{urls}/{name["href"][name["href"].rfind("/")+1:]}",
                        description=''
                    )
                )
    else:
        print(f"Ошибка запроса: {response.status_code}")    