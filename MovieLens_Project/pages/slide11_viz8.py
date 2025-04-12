from dash import html, dcc
import plotly.graph_objects as go
import pandas as pd

def get_layout(data):
    df = data["movies_total"]

    # Преобразуем нужные столбцы
    df['ml_num_ratings'] = pd.to_numeric(df['ml_num_ratings'], errors='coerce')
    df['numVotes_imdb'] = pd.to_numeric(df['numVotes_imdb'], errors='coerce')
    df['title_ml'] = df['title_ml'].astype(str)

    # Удаляем строки с пропущенными значениями
    filtered = df.dropna(subset=['ml_num_ratings', 'numVotes_imdb'])

    # Построение графика
    fig_votes = go.Figure()

    fig_votes.add_trace(go.Scatter(
        x=filtered['numVotes_imdb'],
        y=filtered['ml_num_ratings'],
        mode='markers',
        marker=dict(size=6, opacity=0.6),
        text=filtered['title_ml'],
        hovertemplate='<b>%{text}</b><br>IMDb: %{x}<br>MovieLens: %{y}<extra></extra>'
    ))

    # Диагональная линия
    min_val = min(filtered['numVotes_imdb'].min(), filtered['ml_num_ratings'].min())
    max_val = max(filtered['numVotes_imdb'].max(), filtered['ml_num_ratings'].max())

    fig_votes.add_trace(go.Scatter(
        x=[min_val, max_val],
        y=[min_val, max_val],
        mode='lines',
        line=dict(dash='dash', color='gray'),
        showlegend=False
    ))

    fig_votes.update_layout(
        title='🔢 Сравнение количества голосов: MovieLens и IMDb',
        xaxis_title='IMDb (numVotes)',
        yaxis_title='MovieLens (ml_num_ratings)',
        height=650,
        xaxis_type='log',
        yaxis_type='log'
    )

    return html.Div([
        html.H2("Сравнение количества голосов: MovieLens и IMDb", className="slide-title"),
        html.Hr(),
        dcc.Graph(figure=fig_votes),
        html.Div("11", className="page-number"),
        html.Div([
            dcc.Link("❮", href="/slide10", className="circle-nav-btn prev"),
            dcc.Link("❯", href="/slide12", className="circle-nav-btn next")
        ], className="circle-nav-container")
    ])
