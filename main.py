from models.vacancy import Vacancy
from sources.hh_parser import get_vacancies_hh,read_vacancies_hh
from sources.config import TECH_KEYWORDS
from sources.habr_parser import get_vacancies_habr, get_raw_vacancies,extract_skills
from utils.io import save_vacancies,load_vacancies
from export.html_exporter import generate_html_report
from collections import Counter
from pathlib import Path
import argparse
import json

def clearTempFiles():
    folder = Path("sources/tempFiles")
    for file in folder.iterdir():
        if file.is_file():
            file.unlink()  
            print(f"Удалён файл: {file.name}")


def countSkills():
    vac = load_vacancies()
    for vacancy in [x for x in vac if x.site=="hh"]:
        read_vacancies_hh(vacancy)

    for vacancy in [x for x in vac if x.site=="habr"]:
        get_raw_vacancies(vacancy)

    folder_path = Path("sources/tempFiles")
    all_skills = []
    if folder_path.exists() and folder_path.is_dir():
        for file_path in folder_path.glob("*.txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                skills = extract_skills("".join(f.readlines()),TECH_KEYWORDS)
                all_skills.extend(skills)
    else:
        print("Папка tempFiles не существует!")

    counter = Counter(all_skills)
    dict = {}
    for skill,count in counter.most_common(20):
        print(f"{skill}: {count}")
        dict[skill] = count
    
    clearTempFiles()
    with open("data/statistic.json","w") as f:
        json.dump(dict,f,ensure_ascii=False, indent=2)




def main():
    parser = argparse.ArgumentParser(description='Программа для работы с вакансиями')
    
    parser.add_argument('--getvacancies', action='store_true', help='Получить вакансии')
    parser.add_argument('--getstatistic', action='store_true', help='Получить статистику')
    parser.add_argument('--getreport', action='store_true', help='Сгенерировать отчет')
    
    
    args = parser.parse_args()
    vac = []
    if args.getvacancies:
        get_vacancies_habr("python",vac)
        get_vacancies_hh("python",vac)
        save_vacancies(vac[:10])

    if args.getstatistic:
        countSkills()    
    
    if args.getreport:
        generate_html_report()
    
    # Если никаких аргументов не передано
    if not any(vars(args).values()):
        parser.print_help()





if __name__ == '__main__':
    main()
    
    