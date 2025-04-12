import dash
from dash import html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
from data_loader import load_data

import pages.slide1_intro as slide1
import pages.slide2_goal as slide2
import pages.slide3_data as slide3
import pages.slide4_viz1 as slide4
import pages.slide5_viz2 as slide5
import pages.slide6_viz3 as slide6
import pages.slide7_viz4 as slide7
import pages.slide8_viz5 as slide8
import pages.slide9_viz6 as slide9
import pages.slide10_viz7 as slide10
import pages.slide11_viz8 as slide11
import pages.slide12_viz9 as slide12
import pages.slide13_viz10 as slide13
import pages.slide14_viz11 as slide14
import pages.slide_results as slide15
import pages.slide_team as slide16

data = load_data()

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.FLATLY]
)
server = app.server

def generate_sidebar(pathname):
    slides = [
        ("Основной", "/slide1"),
        ("Цели проекта", "/slide2"),
        ("Описание данных", "/slide3"),
        ("Статистика", "/slide4"),
        ("Оценки", "/slide5"),
        ("Оценки по сезонам", "/slide6"),
        ("ТОП-20 фильмов", "/slide7"),
        ("ТОП-20 жанров", "/slide8"),
        ("Голоса/оценка", "/slide9"),
        ("Жанры/оценки", "/slide10"),
        ("Сравнение голосов", "/slide11"),
        ("Жанры/длительность", "/slide12"),
        ("Жанры/рейтинги", "/slide13"),
        ("Длительность и рейтинги", "/slide14"),
        ("Результаты и выводы", "/slide15"),
        ("Команда", "/slide16"),
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
    page_map = {
        "/slide1": slide1,
        "/slide2": slide2,
        "/slide3": slide3,
        "/slide4": slide4,
        "/slide5": slide5,
        "/slide6": slide6,
        "/slide7": slide7,
        "/slide8": slide8,
        "/slide9": slide9,
        "/slide10": slide10,
        "/slide11": slide11,
        "/slide12": slide12,
        "/slide13": slide13,
        "/slide14": slide14,
        "/slide15": slide15,
        "/slide16": slide16,
    }

    page = page_map.get(pathname)
    if not page:
        return html.Div([html.H1("MovieLens Presentation", style={"textAlign": "center"})])

    # Пытаемся вызвать get_layout(data), если она есть
    if hasattr(page, "get_layout"):
        return page.get_layout(data)
    elif hasattr(page, "layout"):
        return page.layout
    else:
        return html.Div([html.H2("❌ Ошибка: Слайд не содержит layout или get_layout()")])


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
    # app.run(debug=True)
    app.run(debug=True, host="0.0.0.0")


