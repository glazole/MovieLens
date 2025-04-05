from dash import html, dcc

layout = html.Div([
    html.H2("Результаты и выводы", className="slide-title"),
    html.Hr(),
    html.Ul([
        html.Li("Построена адаптивная презентация с помощью Dash"),
        html.Li("Интерактивные графики и таблицы на основе MovieLens"),
        html.Li("Удобная навигация и markdown-контент")
    ]),
    html.Div("6", className="page-number"),
    html.Div([
        dcc.Link("❮", href="/slide5", className="circle-nav-btn prev"),
        dcc.Link("❯", href="/slide7", className="circle-nav-btn next")
    ], className="circle-nav-container")
])
