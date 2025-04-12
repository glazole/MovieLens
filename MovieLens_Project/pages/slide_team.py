from dash import html, dcc
from pathlib import Path
import os

markdown_path = Path(__file__).resolve().parent / "texts" / "members.md"

layout = html.Div([
    html.H2("Команда", className="slide-title"),
    html.Hr(),
    dcc.Markdown(markdown_path.read_text(encoding="utf-8"), className="markdown-block"),
    html.Div("16", className="page-number"),
    html.Div([
        dcc.Link("❮", href="/slide15", className="circle-nav-btn prev"),
        dcc.Link("❯", href="/slide1", className="circle-nav-btn next")
    ], className="circle-nav-container")
])