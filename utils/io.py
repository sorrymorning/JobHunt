import csv
import json
from pathlib import Path
from models.vacancy import Vacancy
from utils.crud import get_vacancies
DATA_PATH = Path("data/vacancies.json")
STATISTIC_PATH = Path("data/statistic.json")

def load_vacancies() -> list[Vacancy]:
    if not DATA_PATH.exists():
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)
        return [Vacancy.from_dict(data=v) for v in raw]

def load_statictic() -> dict:
    if not STATISTIC_PATH.exists():
        return []
    with open(STATISTIC_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)
        return raw

def save_vacancies(vacancies: list[Vacancy]):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump([v.to_dict() for v in vacancies], f, ensure_ascii=False, indent=2)
 


def export_data_to_csv(session):
    vacancies = get_vacancies(session)
    with open("data/vacancies.csv", "w", newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id','title', 'company', 'url', 'description', 'technologies','created_at']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for vacancy in vacancies:
            writer.writerow({
                'id': vacancy.id,
                'title': vacancy.title,
                'company': vacancy.company,
                'url': vacancy.url,
                'description': vacancy.description,
                'technologies': vacancy.technologies,
                'created_at': vacancy.created_at.isoformat()
            })