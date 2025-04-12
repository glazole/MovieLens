from dash import html, dcc
import plotly.express as px
import pandas as pd
import ast

def get_layout(data):
    df = data["movielens"]

    # Преобразуем рейтинг
    df['ml_avg_rating'] = pd.to_numeric(df['ml_avg_rating'], errors='coerce')

    # Универсальный разбор жанров
    def parse_genres(val):
        try:
            parsed = ast.literal_eval(val)
            if isinstance(parsed, list):
                return parsed
        except:
            pass
        # fallback: разбиваем по '|' если это просто строка
        if isinstance(val, str) and "|" in val:
            return val.split("|")
        return []

    df['genres_ml'] = df['genres_ml'].apply(parse_genres)

    # Разворачиваем по жанрам
    df_genres = df.explode('genres_ml').dropna(subset=['genres_ml'])

    # Фильтруем только непустые жанры
    df_genres = df_genres[df_genres['genres_ml'].str.strip() != '']

    # Считаем среднюю оценку по жанрам
    genre_avg = (
        df_genres.groupby('genres_ml')['ml_avg_rating']
        .mean()
        .sort_values(ascending=False)
        .head(20)
        .reset_index()
        .rename(columns={'genres_ml': 'Жанр', 'ml_avg_rating': 'Средняя оценка'})
    )

    # Построение графика
    fig = px.bar(
        genre_avg.sort_values(by='Средняя оценка'),
        x='Средняя оценка',
        y='Жанр',
        orientation='h',
        title='🎭 ТОП-20 жанров по средней оценке фильмов',
        text='Средняя оценка'
    )

    fig.update_layout(
        yaxis=dict(autorange='reversed'),
        height=700
    )

    return html.Div([
        html.H2("ТОП-20 жанров по средней оценке", className="slide-title"),
        html.Hr(),
        dcc.Graph(figure=fig),
        html.Div("8", className="page-number"),
        html.Div([
            dcc.Link("❮", href="/slide7", className="circle-nav-btn prev"),
            dcc.Link("❯", href="/slide9", className="circle-nav-btn next")
        ], className="circle-nav-container")
    ])
