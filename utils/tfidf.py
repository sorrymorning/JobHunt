from utils.crud import get_vacancies_df
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import re



def clean_text(text):
    text = str(text).lower()                          # Приводим к нижнему регистру
    text = re.sub(r'\\[ntr]', ' ', text)              # Удаляем \n, \t и др.
    text = re.sub(r'[^a-zA-Zа-яА-Я0-9\s]', '', text)  # Удаляем пунктуацию
    text = re.sub(r'\s+', ' ', text)                  # Убираем лишние пробелы
    # text = re.sub(r'\b[а-яА-ЯёЁ]+\b', '', text)
    return text.strip()

def remove_russian_words(text):
    return re.sub(r'\b[а-яА-ЯёЁ]+\b', '', text)


def train_model(session):
    # Загрузка и очистка данных
    df = get_vacancies_df(session)
    df["text"] = df["text"].apply(remove_russian_words)

    # Векторизация
    vectorizer = TfidfVectorizer(
        max_features=3000,
        token_pattern=r'\b[a-zA-Z]{2,}\b',
        stop_words='english',
        min_df=3,
        max_df=0.9
    )
    X = vectorizer.fit_transform(df["text"])

    # Кластеризация
    n_clusters = 8
    model = KMeans(n_clusters=n_clusters, random_state=42)
    df["cluster"] = model.fit_predict(X)

    return model, vectorizer, df

def get_matching_vacancies(model, vectorizer, df, stack):

    candidate_stack = clean_text(stack)
    candidate_vector = vectorizer.transform([candidate_stack])
    predicted_cluster = model.predict(candidate_vector)[0]
    print("->Предсказанный кластер:", predicted_cluster)
    matching_vacancies = df[df["cluster"] == predicted_cluster]
    print("Подходящие вакансии:")
    if not matching_vacancies.empty:
        print(matching_vacancies[["title", "url"]].dropna().head(10).to_string(index=False))
    else:
        print("Нет подходящих вакансий.")


