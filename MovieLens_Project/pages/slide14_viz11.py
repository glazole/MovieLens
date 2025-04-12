from dash import html, dcc
import plotly.express as px
import pandas as pd

def get_layout(data):
    # Получаем нужный датасет
    df = data["movies_total"]

    # Преобразуем типы
    df['runtimeMinutes_imdb'] = pd.to_numeric(df['runtimeMinutes_imdb'], errors='coerce')
    df['ml_avg_rating'] = pd.to_numeric(df['ml_avg_rating'], errors='coerce')
    df['avgRating_imdb'] = pd.to_numeric(df['avgRating_imdb'], errors='coerce')
    df['rating_kp'] = pd.to_numeric(df['rating_kp'], errors='coerce')

    # Удалим пропуски
    filtered = df.dropna(subset=['runtimeMinutes_imdb', 'ml_avg_rating', 'avgRating_imdb', 'rating_kp'])

    # Корреляционная матрица
    corr_matrix = filtered[['runtimeMinutes_imdb', 'ml_avg_rating', 'avgRating_imdb', 'rating_kp']].corr().round(2)

    # Визуализация
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect='auto',
        color_continuous_scale='RdBu_r',
        title='🎬 Корреляция: длительность фильма и рейтинги'
    )

    fig.update_layout(
        height=600
    )

    return html.Div([
        html.H2("Корреляция продолжительности фильма с рейтингами", className="slide-title"),
        html.Hr(),
        dcc.Graph(figure=fig),
        html.Div("14", className="page-number"),
        html.Div([
            dcc.Link("❮", href="/slide13", className="circle-nav-btn prev"),
            dcc.Link("❯", href="/slide15", className="circle-nav-btn next")
        ], className="circle-nav-container")
    ])
