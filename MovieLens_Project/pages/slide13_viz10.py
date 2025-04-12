from dash import html, dcc
import plotly.express as px
import pandas as pd
import ast

def get_layout(data):
    # Загружаем таблицу
    df = data["movies_total"]

    # Преобразуем числовые поля
    df['ml_avg_rating'] = pd.to_numeric(df['ml_avg_rating'], errors='coerce')
    df['avgRating_imdb'] = pd.to_numeric(df['avgRating_imdb'], errors='coerce')
    df['rating_kp'] = pd.to_numeric(df['rating_kp'], errors='coerce')
    df['voteAvg_tmdb'] = pd.to_numeric(df['voteAvg_tmdb'], errors='coerce')

    # Удалим строки с пропущенными значениями
    filtered = df.dropna(subset=['ml_avg_rating', 'avgRating_imdb', 'voteAvg_tmdb', 'rating_kp', 'genres_ml']).copy()

    # Парсим жанры: поддержка '|' и строковых списков
    def parse_genres(val):
        if pd.isna(val):
            return []
        if isinstance(val, str):
            val = val.strip()
            if val.startswith("[") and val.endswith("]"):
                try:
                    parsed = ast.literal_eval(val)
                    return parsed if isinstance(parsed, list) else []
                except:
                    return []
            elif '|' in val:
                return val.split('|')
        return []

    filtered['genres_ml'] = filtered['genres_ml'].apply(parse_genres)

    # print("▶ genres_ml после парсинга:", filtered['genres_ml'].head())

    # Разворачиваем жанры
    exploded = filtered.explode('genres_ml').dropna(subset=['genres_ml'])
    # print("▶ Кол-во строк после explode:", len(exploded))
    # print("▶ Примеры жанров:", exploded['genres_ml'].unique()[:10])

    # One-hot кодировка
    genre_dummies = pd.get_dummies(exploded['genres_ml'])
    # print("▶ Колонки жанров:", genre_dummies.columns.tolist())

    # Объединяем с рейтингами
    matrix = pd.concat([genre_dummies, exploded[['ml_avg_rating', 'avgRating_imdb', 'voteAvg_tmdb', 'rating_kp']]], axis=1)

    # Строим корреляционную матрицу
    correlation = matrix.corr(numeric_only=True).round(2)

    # Извлекаем только строки по жанрам и колонки с рейтингами
    corr_genres_ratings = correlation[['ml_avg_rating', 'avgRating_imdb', 'voteAvg_tmdb', 'rating_kp']].drop(['ml_avg_rating', 'avgRating_imdb', 'voteAvg_tmdb', 'rating_kp'])

    if corr_genres_ratings.empty:
        # print("⚠ Корреляционная матрица пуста. Проверь исходные жанры.")
        return html.Div([
            html.H2("Корреляция между жанрами и рейтингами", className="slide-title"),
            html.Hr(),
            html.Div("❌ Не удалось построить график: нет данных после обработки."),
            html.Div("13", className="page-number"),
            html.Div([
                dcc.Link("❮", href="/slide12", className="circle-nav-btn prev"),
                dcc.Link("❯", href="/slide14", className="circle-nav-btn next")
            ], className="circle-nav-container")
        ])

    # Построение графика
    fig = px.imshow(
        corr_genres_ratings,
        text_auto=True,
        aspect='auto',
        color_continuous_scale='RdBu_r',
        title='🎭 Корреляция жанров с рейтингами MovieLens и IMDb'
    )

    fig.update_layout(
        xaxis_title='Рейтинг',
        yaxis_title='Жанры',
        height=700
    )

    return html.Div([
        html.H2("Корреляция между жанрами и рейтингами", className="slide-title"),
        html.Hr(),
        dcc.Graph(figure=fig),
        html.Div("13", className="page-number"),
        html.Div([
            dcc.Link("❮", href="/slide12", className="circle-nav-btn prev"),
            dcc.Link("❯", href="/slide14", className="circle-nav-btn next")
        ], className="circle-nav-container")
    ])
