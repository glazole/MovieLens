from dash import html, dcc
import plotly.express as px
import pandas as pd

# Тестовая визуализация
df = px.data.gapminder().query("year == 2007")
fig = px.scatter(df, x="gdpPercap", y="lifeExp", size="pop", color="continent", log_x=True)

layout = html.Div([
    html.H2("Визуализация 2", className="slide-title"),
    html.Hr(),
    dcc.Graph(figure=fig),
    html.Div("5", className="page-number"),
    html.Div([
        dcc.Link("❮", href="/slide4", className="circle-nav-btn prev"),
        dcc.Link("❯", href="/slide6", className="circle-nav-btn next")
    ], className="circle-nav-container")
])

