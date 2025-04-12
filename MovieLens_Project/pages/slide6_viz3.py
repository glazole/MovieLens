from dash import html, dcc
import plotly.express as px
import pandas as pd

def get_layout(data):
    # Получаем нужный датасет
    df = data["movielens"]

    # Преобразуем типы
    df['ml_avg_rating'] = df['ml_avg_rating'].astype(float)
    df['season_ml_rating'] = df['season_ml_rating'].astype(str)

    # Установим порядок сезонов
    season_order = ['Winter', 'Spring', 'Summer', 'Autumn']
    df['season_ml_rating'] = pd.Categorical(df['season_ml_rating'], categories=season_order, ordered=True)

    # Группировка: средняя оценка по сезону
    avg_rating_by_season = (
        df.groupby('season_ml_rating', observed=False)['ml_avg_rating']
        .mean()
        .reset_index()
    )

    # Построение графика
    fig = px.bar(
        avg_rating_by_season,
        x='season_ml_rating',
        y='ml_avg_rating',
        title='📉 Средняя оценка фильмов по сезонам (все годы)',
        labels={'season_ml_rating': 'Сезон', 'ml_avg_rating': 'Средняя оценка'},
        text_auto='.2f'
    )

    fig.update_layout(
        xaxis_title='Сезон',
        yaxis_title='Средняя оценка',
        height=600
    )

    return html.Div([
        html.H2("Средняя оценка фильмов по сезонам", className="slide-title"),
        html.Hr(),
        dcc.Graph(figure=fig),
        html.Div("6", className="page-number"),
        html.Div([
            dcc.Link("❮", href="/slide5", className="circle-nav-btn prev"),
            dcc.Link("❯", href="/slide7", className="circle-nav-btn next")
        ], className="circle-nav-container")
    ])
