from dash import html, dcc
import plotly.express as px
import pandas as pd

def get_layout(data):
    df = data["movielens"]
    df['ml_num_ratings'] = pd.to_numeric(df['ml_num_ratings'], errors='coerce')
    df['title_ml'] = df['title_ml'].astype(str)

    # Агрегируем и выбираем топ-20
    top20 = (
        df.groupby('title_ml', as_index=False)['ml_num_ratings']
        .sum()
        .dropna()
        .sort_values(by='ml_num_ratings', ascending=False)
        .head(20)
        .reset_index(drop=True)
    )

    # Формат подписей
    top20['text_label'] = top20['ml_num_ratings'].apply(lambda x: f"{x/1000:.1f}K")

    # Явно задаём порядок
    category_order = top20.sort_values('ml_num_ratings', ascending=False)['title_ml'].tolist()

    fig = px.bar(
        top20,
        x='ml_num_ratings',
        y='title_ml',
        orientation='h',
        text='text_label',
        title='🔥 ТОП-20 самых популярных фильмов по количеству голосов',
        labels={'ml_num_ratings': 'Количество голосов', 'title_ml': 'Фильм'},
        category_orders={'title_ml': category_order}  # 👈 Устанавливаем порядок
    )

    fig.update_traces(textposition='outside')
    fig.update_layout(
        height=800,
        yaxis_title='Фильм',
        xaxis_title='Количество голосов'
    )

    return html.Div([
        html.H2("ТОП-20 самых популярных фильмов", className="slide-title"),
        html.Hr(),
        dcc.Graph(figure=fig),
        html.Div("7", className="page-number"),
        html.Div([
            dcc.Link("❮", href="/slide6", className="circle-nav-btn prev"),
            dcc.Link("❯", href="/slide8", className="circle-nav-btn next")
        ], className="circle-nav-container")
    ])
