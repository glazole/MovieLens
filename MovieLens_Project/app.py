import dash
from dash import html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
import pages.slide1_intro as slide1
import pages.slide2_goal as slide2
import pages.slide3_data as slide3
import pages.slide4_viz1 as slide4
import pages.slide5_viz2 as slide5
import pages.slide6_results as slide6
import pages.slide7_thanks as slide7

app = dash.Dash(__name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.FLATLY]  # или любой другой стиль
)
server = app.server

def generate_sidebar(pathname):
    slides = [
        ("Основной", "/slide1"),
        ("Цели проекта", "/slide2"),
        ("Описание данных", "/slide3"),
        ("Визуализация 1", "/slide4"),
        ("Визуализация 2", "/slide5"),
        ("Результаты и выводы", "/slide6"),
        ("Команда", "/slide7"),
    ]
    return html.Div(
        id="sidebar",
        className="sidebar",
        children=[
            html.H2("MovieLens", className="sidebar-title"),
            html.Ul([
                html.Li(
                    dcc.Link(name, href=link, className="active" if pathname == link else "")
                ) for name, link in slides
            ])
        ]
    )

def render_page(pathname):
    if pathname == "/slide1":
        return slide1.layout
    elif pathname == "/slide2":
        return slide2.layout
    elif pathname == "/slide3":
        return slide3.layout
    elif pathname == "/slide4":
        return slide4.layout
    elif pathname == "/slide5":
        return slide5.layout
    elif pathname == "/slide6":
        return slide6.layout
    elif pathname == "/slide7":
        return slide7.layout
    else:
        return html.Div([html.H1("MovieLens Presentation", style={"textAlign": "center"})])

app.layout = html.Div([
    dcc.Location(id="url"),
    html.Button("\u2630", id="toggle-button", className="toggle-button"),
    html.Div(id="main-content")
])

@app.callback(Output("main-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    return html.Div([
        generate_sidebar(pathname),
        html.Div(render_page(pathname), className="content")
    ], className="main")

@app.callback(
    Output("sidebar", "style"),
    Input("toggle-button", "n_clicks"),
    State("sidebar", "style"),
    prevent_initial_call=True
)
def toggle_sidebar(n, current_style):
    if current_style and current_style.get("display") == "none":
        return {"display": "block"}
    else:
        return {"display": "none"}

if __name__ == "__main__":
    app.run(debug=True)