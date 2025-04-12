from dash import html, dash_table
import pandas as pd
import dash_mantine_components as dmc

def get_layout(data):  # <- изменить имя функции!
    df = data["movies_total"]
    describe_df = df.describe(include='all').transpose().reset_index()
    describe_df.rename(columns={'index': 'column'}, inplace=True)

    return html.Div([
        html.H2("Статистическое описание датасета MovieLens", className="slide-title"),
        html.Hr(),
        dmc.Text("Метод describe() — сводная информация по столбцам:", className="mb-4"),
        dash_table.DataTable(
            data=describe_df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in describe_df.columns],
            style_table={
                'overflowX': 'auto',
                'maxHeight': '700px',
                'overflowY': 'scroll'
            },
            style_cell={
                'textAlign': 'left',
                'padding': '6px',
                'whiteSpace': 'nowrap',
                'height': 'auto',
                'maxWidth': '250px',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis'
            },

            style_header={
                'fontWeight': 'bold',
                'backgroundColor': '#f0f0f0'
            },
            page_size=len(describe_df)
        ),
        html.Div("4", className="page-number"),
        html.Div([
            html.A("❮", href="/slide3", className="circle-nav-btn prev"),
            html.A("❯", href="/slide5", className="circle-nav-btn next")
        ], className="circle-nav-container")
    ])
