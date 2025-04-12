from dash import html, dcc
import plotly.express as px
import pandas as pd

def get_layout(data):
    # Используем нужный датасет
    df = data["movielens"]

    # Преобразуем нужные поля
    df['year_ml_rating'] = df['year_ml_rating'].astype(int)
    df['ml_avg_rating'] = df['ml_avg_rating'].astype(float)

    # Группировка: средняя оценка по году
    avg_rating_by_year = df.groupby('year_ml_rating')['ml_avg_rating'].mean().reset_index()

    # Построение графика
    fig = px.line(
        avg_rating_by_year,
        x='year_ml_rating',
        y='ml_avg_rating',
        title='📈 Средняя оценка фильмов по годам',
        labels={'year_ml_rating': 'Год', 'ml_avg_rating': 'Средняя оценка'}
    )

    fig.update_layout(
        xaxis_title='Год',
        yaxis_title='Средняя оценка',
        height=600
    )

    return html.Div([
        html.H2("Динамика среднего рейтинга по годам", className="slide-title"),
        html.Hr(),
        dcc.Graph(figure=fig),
        html.Div("5", className="page-number"),
        html.Div([
            dcc.Link("❮", href="/slide4", className="circle-nav-btn prev"),
            dcc.Link("❯", href="/slide6", className="circle-nav-btn next")
        ], className="circle-nav-container")
    ])
