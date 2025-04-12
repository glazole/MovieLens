import pandas as pd
import os

def load_data():
    # Абсолютный или относительный путь к каталогу с данными
    DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"❌ Путь к данным не существует: {DATA_PATH}")

    # Загружаем все нужные CSV
    actors = pd.read_csv(os.path.join(DATA_PATH, "ACTORS_BATCH.csv"), sep=';', dtype='object', low_memory=False)
    movies_total = pd.read_csv(os.path.join(DATA_PATH, "MOVIES_TOTAL.csv"), sep=';', dtype='object', low_memory=False)
    movielens = pd.read_csv(os.path.join(DATA_PATH, "DATASET_MovieLens.csv"), sep=';', dtype='object', low_memory=False)

    return {
        "actors": actors,
        "movies_total": movies_total,
        "movielens": movielens
    }
