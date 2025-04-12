from dash import html, dcc
import plotly.express as px
import pandas as pd

def get_layout(data):
    df = data["movielens"]

    # Преобразуем типы
    df['ml_num_ratings'] = pd.to_numeric(df['ml_num_ratings'], errors='coerce')
    df['ml_avg_rating'] = pd.to_numeric(df['ml_avg_rating'], errors='coerce')
    df['year_ml_rating'] = pd.to_numeric(df['year_ml_rating'], errors='coerce')
    df['title_ml'] = df['title_ml'].astype(str)

    # Фильтрация и сортировка по году
    filtered = df.dropna(subset=['ml_num_ratings', 'ml_avg_rating', 'year_ml_rating']).copy()
    filtered['year_ml_rating'] = filtered['year_ml_rating'].astype(int)
    filtered = filtered.sort_values(by='year_ml_rating')

    # Создаём строковую колонку — но уже в правильном порядке
    filtered['year_str'] = filtered['year_ml_rating'].astype(str)

    # Построение графика
    fig = px.scatter(
        filtered,
        x='ml_num_ratings',
        y='ml_avg_rating',
        animation_frame='year_str',
        hover_data=['title_ml'],
        title='🎯 Связь между количеством голосов и средней оценкой по годам',
        labels={
            'ml_num_ratings': 'Количество голосов',
            'ml_avg_rating': 'Средняя оценка',
            'year_str': 'Год'
        },
        size_max=10,
        log_x=True
    )

    fig.update_layout(
        height=700,
        xaxis_title='Количество голосов (логарифмическая шкала)',
        yaxis_title='Средняя оценка',
        transition={'duration': 500}
    )

    return html.Div([
        html.H2("Связь между популярностью и оценкой по годам", className="slide-title"),
        html.Hr(),
        dcc.Graph(figure=fig),
        html.Div("9", className="page-number"),
        html.Div([
            dcc.Link("❮", href="/slide8", className="circle-nav-btn prev"),
            dcc.Link("❯", href="/slide10", className="circle-nav-btn next")
        ], className="circle-nav-container")
    ])
