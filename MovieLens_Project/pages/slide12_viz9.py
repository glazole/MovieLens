from dash import html, dcc
import plotly.express as px
import pandas as pd
import ast

def get_layout(data):
    df = data["movies_total"]

    # Преобразуем длительность
    df['runtimeMinutes_imdb'] = pd.to_numeric(df['runtimeMinutes_imdb'], errors='coerce')

    # Удаляем строки без длительности или жанров
    df = df.dropna(subset=['runtimeMinutes_imdb', 'genres_ml']).copy()

    # Парсим жанры
    def parse_genres(val):
        try:
            genres = ast.literal_eval(val)
            if isinstance(genres, list):
                return genres
        except:
            pass
        if isinstance(val, str) and "|" in val:
            return val.split("|")
        return []

    df['genres_ml'] = df['genres_ml'].apply(parse_genres)

    # Разворачиваем по жанрам
    exploded = df.explode('genres_ml')
    exploded = exploded.dropna(subset=['genres_ml'])

    # Удаляем пустые строки в жанрах
    exploded = exploded[exploded['genres_ml'].str.strip() != ""]

    # One-hot encoding
    genre_dummies = pd.get_dummies(exploded['genres_ml'])

    if genre_dummies.empty or exploded['runtimeMinutes_imdb'].isna().all():
        return html.Div([
            html.H2("Корреляция между жанрами и длительностью фильма", className="slide-title"),
            html.P("⚠️ Недостаточно данных для построения графика."),
            html.Div("13", className="page-number"),
            html.Div([
                dcc.Link("❮", href="/slide12", className="circle-nav-btn prev"),
                dcc.Link("❯", href="/slide14", className="circle-nav-btn next")
            ], className="circle-nav-container")
        ])

    # Объединяем
    matrix = pd.concat([genre_dummies, exploded['runtimeMinutes_imdb']], axis=1)

    # Корреляция
    correlation = matrix.corr(numeric_only=True).round(2)
    correlation_to_runtime = correlation[['runtimeMinutes_imdb']].drop('runtimeMinutes_imdb')

    # Визуализация
    fig = px.imshow(
        correlation_to_runtime,
        text_auto=True,
        aspect='auto',
        color_continuous_scale='RdBu_r',
        title='🎬 Корреляция продолжительности фильма и жанров'
    )

    fig.update_layout(
        xaxis_title='Продолжительность (минуты)',
        yaxis_title='Жанры',
        height=700
    )

    return html.Div([
        html.H2("Корреляция между жанрами и длительностью фильма", className="slide-title"),
        html.Hr(),
        dcc.Graph(figure=fig),
        html.Div("12", className="page-number"),
        html.Div([
            dcc.Link("❮", href="/slide11", className="circle-nav-btn prev"),
            dcc.Link("❯", href="/slide13", className="circle-nav-btn next")
        ], className="circle-nav-container")
    ])
