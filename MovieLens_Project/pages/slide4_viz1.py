from dash import html, dcc, dash_table, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc

# Загружаем данные
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

layout = html.Div([
    html.H2("Визуализация 1", className="slide-title"),
    html.Hr(),

    dmc.RadioGroup(
        [dmc.Radio(i, value=i) for i in ['pop', 'lifeExp', 'gdpPercap']],
        id='my-dmc-radio-item',
        value='lifeExp',
        size="sm",
        className="mb-4"
    ),

    dmc.Grid([
        dmc.Col([
            dash_table.DataTable(
                data=df.to_dict('records'),
                page_size=10,
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'padding': '5px'},
            )
        ], span=6),

        dmc.Col([
            dcc.Graph(figure={}, id='graph-placeholder')
        ], span=6),
    ]),

    html.Div("4", className="page-number"),
    html.Div([
        dcc.Link("❮", href="/slide3", className="circle-nav-btn prev"),
        dcc.Link("❯", href="/slide5", className="circle-nav-btn next")
    ], className="circle-nav-container")
])

@callback(
    Output('graph-placeholder', 'figure'),
    Input('my-dmc-radio-item', 'value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
    return fig
