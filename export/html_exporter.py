from jinja2 import Environment, FileSystemLoader
from models.vacancy import Vacancy
from pathlib import Path
from utils.io import load_vacancies,load_statictic

TEMPLATE_DIR = Path("templates")
OUTPUT_PATH = Path("report.html")
VACANCIES_PATH = Path("data/vacancies.json")


def generate_html_report():
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("vacancies.html")
    vacancies = load_vacancies()
    statistic = load_statictic()
    vacancies.sort(reverse=True, key = lambda x : x.compatibility)
    html_content = template.render(vacancies=vacancies,technologies=statistic)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ Отчёт сохранён в {OUTPUT_PATH.absolute()}")