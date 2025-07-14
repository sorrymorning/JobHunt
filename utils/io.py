import json
from pathlib import Path
from models.vacancy import Vacancy

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
 