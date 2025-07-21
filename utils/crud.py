from models.vacancy import Vacancy
from sqlalchemy.exc import IntegrityError



def add_vacancy(session,title,company,url,description,technologies):
    vacancy = Vacancy(
        title=title, 
        company=company, 
        url=url, 
        description=description,
        technologies=technologies
    )
    session.add(vacancy)

    try:
        session.commit()
        print(f"Вакансия {title} добавлена")
    except IntegrityError:
        session.rollback()
        print(f"Вакансия {title} уже существует")


def get_vacancies(session):
    return session.query(Vacancy).all()


def update_vacancies(session,url,new_skills = None):
    vacancy = session.query(Vacancy).filter_by(url=url).first()

    if not vacancy:
        print(f"Такой вакансии нет -> {url}")
        return

    if new_skills is not None:
        vacancy.technologies = new_skills
    

    session.commit()
    print("Вакансия обновлена")
