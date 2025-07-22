from sources.hh_parser import get_vacancies_hh
from sources.config import TECH_KEYWORDS
from sources.habr_parser import get_vacancies_habr,extract_skills
from sources.fetch_vacancy import fetch_vacancy
from export.html_exporter import generate_html_report
from collections import Counter
import argparse
import json
from data.database import SessionLocal,engine
from data.database import Base
from utils.crud import get_vacancies,update_vacancies,add_compability,\
                        get_compability_by_id,update_compability



def count_skills(session):
    vac = get_vacancies(session)

    all_skills = []
    for vacancy in vac: 
        f = fetch_vacancy(vacancy)
        skills = extract_skills(f,TECH_KEYWORDS)
        update_vacancies(session,vacancy.url,','.join(skills))
        all_skills.extend(skills)

    counter = Counter(all_skills)
    dict = {}
    for skill,count in counter.most_common(20):
        print(f"{skill}: {count}")
        dict[skill] = count

    with open("data/statistic.json","w") as f:
        json.dump(dict,f,ensure_ascii=False, indent=2)

def jaccard_similarity(set1, set2):
    set1,set2 = set(set1),set(set2)
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union else 0


def get_best_vacancy(session,user_skills):
    vac = get_vacancies(session)

    for vacancy in vac:
        score = jaccard_similarity(user_skills,vacancy.technologies.split(','))
        print(f"{vacancy.title}: совпадение {score:.2f}")
        if get_compability_by_id(session,vacancy.id):
            update_compability(session,vacancy.id,score)
        else:
            add_compability(session,1,vacancy.id,score)

def main():
    parser = argparse.ArgumentParser(description='Программа для работы с вакансиями')
    
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    


    parser.add_argument('--getvacancies', action='store_true', help='Получить вакансии')
    parser.add_argument('--getstatistic', action='store_true', help='Получить статистику')
    parser.add_argument('--getreport', action='store_true', help='Сгенерировать отчет')
    parser.add_argument('--getbest',type=lambda s: s.split(','), help='Узнать совместимость вакансий')
    
    
    args = parser.parse_args()
    if args.getvacancies:
        get_vacancies_habr("python",session)
        get_vacancies_hh("python",session)

    if args.getstatistic:
        count_skills(session)    
    
    if args.getreport:
        generate_html_report(session)
    
    if args.getbest:
        get_best_vacancy(session,args.getbest)

    if not any(vars(args).values()):
        parser.print_help()





if __name__ == '__main__':
    main()
    
    