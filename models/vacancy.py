from sqlalchemy import create_engine, Column, Integer, Float, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from data.database import Base

class Vacancy(Base):
    __tablename__ = 'vacancies'

    id = Column(Integer,primary_key=True)
    title = Column(String)
    company = Column(String)
    url = Column(String,unique=True)
    description = Column(Text)
    technologies = Column(String)
    created_at = Column(DateTime,default = datetime.now())


class Compability(Base):
    __tablename__ = 'compability'

    id = Column(Integer,primary_key=True)
    user_id = Column(Integer)
    vacancy_id = Column(Integer,ForeignKey('vacancies.id'))
    score = Column(Float)
    vacancy = relationship("Vacancy")