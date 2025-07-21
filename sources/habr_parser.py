import requests
from bs4 import BeautifulSoup
import re
from utils.crud import add_vacancy

def extract_skills(text:str,keywords:list[str]) -> list[str]:
    text = text.lower()
    found = []

    for kw in keywords:
        if re.search(rf'\b{re.escape(kw.lower())}\b',text):
            found.append(kw)
    return found


def get_vacancies_habr(job : str,session):
    urls = "https://career.habr.com/vacancies"

    for id in [1,3]:
        params = {
            "page":1,
            "q": job,
            "qid":id,
            "type": "all"  
        }

        response = requests.get(urls,  params=params)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text,'lxml')
            links = soup.find_all(class_='vacancy-card__title-link')
            companyName = soup.find_all(class_='vacancy-card__company-title')
            # locationJob = soup.find_all(class_='vacancy-card__meta')
            if len(links) > 0:
                for index,name in enumerate(links):
                    
                    add_vacancy(
                            session=session,
                            title=name.text,
                            company = companyName[index].text,
                            url=f"{urls}/{name["href"][name["href"].rfind("/")+1:]}",
                            description='',
                            technologies = ''
                        )

        else:
            print(f"Ошибка запроса: {response.status_code}")    