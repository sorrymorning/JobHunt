from models.vacancy import Vacancy
from models.vacancy import Compability
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



def add_compability(session,user_id,vacancy_id,score):
    compability = Compability(
        user_id=user_id,
        vacancy_id=vacancy_id,
        score=score
    )
    session.add(compability)

    try:
        session.commit()
        print(f"Соответствие {user_id} и {vacancy_id} добавлено")
    except IntegrityError:
        session.rollback()
        print(f"Соответствие уже существует")

def update_compability(session,vacancy_id,new_score = None):
    compability = session.query(Compability).filter_by(vacancy_id=vacancy_id).first()
    
    if new_score is not None:
        compability.score = new_score

    session.commit()
    print("Соответствие обновлено")


def get_compability_by_id(session,vacancy_id) -> bool:
    comp = session.query(Compability).filter_by(vacancy_id=vacancy_id).first()
    if comp:
        return True
    return False


def get_vacancies_with_compabilities(session):
    result = (
        session.query(Vacancy,Compability)
        .join(Compability,Vacancy.id == Compability.vacancy_id)
        .order_by(Compability.score.desc())
        .all()
    )

    return result
