from dash import html, dcc
from pathlib import Path
import os

markdown_path = Path(__file__).resolve().parent / "texts" / "members.md"

layout = html.Div([
    html.H2("Спасибо за внимание!", className="slide-title"),
    html.Hr(),
    dcc.Markdown(markdown_path.read_text(encoding="utf-8"), className="markdown-block"),
    html.P("GitHub: https://github.com/glazole/MovieLens.git"),
    html.P("Email: o.glazkov@innopolis.university"),
    html.Div("7", className="page-number"),
    html.Div([
        dcc.Link("❮", href="/slide6", className="circle-nav-btn prev"),
    ], className="circle-nav-container")
])
