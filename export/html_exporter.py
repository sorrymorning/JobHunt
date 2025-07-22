from jinja2 import Environment, FileSystemLoader
from models.vacancy import Vacancy
from pathlib import Path
from utils.crud import get_vacancies_with_compabilities
from utils.io import load_statictic


TEMPLATE_DIR = Path("templates")
OUTPUT_PATH = Path("report.html")


def generate_html_report(session):
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("vacancies.html")
    statistic = load_statictic()
    vacancies = get_vacancies_with_compabilities(session)
    html_content = template.render(vacancies=vacancies,technologies=statistic)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ Отчёт сохранён в {OUTPUT_PATH.absolute()}")