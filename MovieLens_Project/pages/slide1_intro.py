from dash import html, dcc

layout = html.Div([
    html.H1("MovieLens Presentation", className="slide-title"),
    html.Hr(),
    html.P("Добро пожаловать в интерактивную презентацию проекта MovieLens."),
    html.Div("1", className="page-number"),
    html.Div([
        dcc.Link("❯", href="/slide2", className="circle-nav-btn next")
    ], className="circle-nav-container")
])
