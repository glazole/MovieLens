from dash import html, dcc
import plotly.express as px
import pandas as pd
import ast

def get_layout(data):
    df = data["movielens"]

    df['ml_avg_rating'] = pd.to_numeric(df['ml_avg_rating'], errors='coerce')
    df['year_ml_rating'] = pd.to_numeric(df['year_ml_rating'], errors='coerce')
    df = df.dropna(subset=['ml_avg_rating', 'year_ml_rating', 'genres_ml'])

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
    df_genres = df.explode('genres_ml').dropna(subset=['genres_ml'])

    df_genres['year_ml_rating'] = df_genres['year_ml_rating'].astype(int)

    # 🔧 группируем по числовому году!
    genre_year_avg = (
        df_genres
        .groupby(['year_ml_rating', 'genres_ml'], observed=True)['ml_avg_rating']
        .mean()
        .reset_index()
        .rename(columns={'genres_ml': 'Жанр', 'ml_avg_rating': 'Средняя оценка'})
    )

    # 🔧 сортируем по числовому году
    top10_genres_by_year = (
        genre_year_avg
        .sort_values(['year_ml_rating', 'Средняя оценка'], ascending=[True, False])
        .groupby('year_ml_rating', observed=True)
        .head(10)
        .sort_values('year_ml_rating')  # фиксируем порядок анимации
    )

    fig = px.bar(
        top10_genres_by_year,
        x='Средняя оценка',
        y='Жанр',
        orientation='h',
        animation_frame='year_ml_rating',  # ← теперь всё на числовом
        title='🎭 ТОП-10 жанров по средней оценке фильмов (анимация по годам)',
        text='Средняя оценка',
        range_x=[
            top10_genres_by_year['Средняя оценка'].min() - 0.1,
            top10_genres_by_year['Средняя оценка'].max() + 0.1
        ],
        height=700
    )

    fig.update_layout(
        yaxis=dict(autorange='reversed'),
        transition={'duration': 800}
    )

    return html.Div([
        html.H2("ТОП-10 жанров по средней оценке по годам", className="slide-title"),
        html.Hr(),
        dcc.Graph(figure=fig),
        html.Div("10", className="page-number"),
        html.Div([
            dcc.Link("❮", href="/slide9", className="circle-nav-btn prev"),
            dcc.Link("❯", href="/slide11", className="circle-nav-btn next")
        ], className="circle-nav-container")
    ])
