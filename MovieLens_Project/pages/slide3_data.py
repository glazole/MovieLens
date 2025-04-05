from dash import html, dcc

layout = html.Div([
    html.H2("Описание данных", className="slide-title"),
    html.Hr(),
    html.P("В этом проекте используются данные MovieLens (movies.csv, ratings.csv и др)."),
    html.Div("3", className="page-number"),
    html.Div([
        dcc.Link("❮", href="/slide2", className="circle-nav-btn prev"),
        dcc.Link("❯", href="/slide4", className="circle-nav-btn next")
    ], className="circle-nav-container")
])
