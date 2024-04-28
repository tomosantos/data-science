import dash
from dash import html, dcc
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc


app = dash.Dash(
    external_stylesheets=[dbc.themes.DARKLY]
)
server = app.server


# =========== Ingestão de dados =========== #
df_data = pd.read_csv('supermarket_sales.csv')
df_data['Date'] = pd.to_datetime(df_data['Date'])


# =========== Layout =========== #
app.layout = html.Div(children=[
    html.H5("Cidades:"),
    dcc.Checklist(df_data['City'].value_counts().index, df_data['City'].value_counts().index, id='check-city'),
    
    html.H5("Variável de Análise: "),
    dcc.RadioItems(['gross income', 'Rating'], "gross income", id='main-variable'),
    
    dcc.Graph(id='city-fig'),
    dcc.Graph(id='pay-fig'),
    dcc.Graph(id='income-per-product-fig'),
    
])


# =========== Callbacks =========== #
@app.callback([
        Output('city-fig', 'figure'),
        Output('pay-fig', 'figure'),
        Output('income-per-product-fig', 'figure'),
    ],
    [
        Input('check-city', 'value'),
        Input('main-variable', 'value'),
    ]
)
def render_graphs(cities, main_variable):
    operation = np.sum if main_variable == 'Gross Income' else np.mean
    df_filtered = df_data[df_data['City'].isin(cities)]
    
    df_city = df_filtered.groupby('City')[main_variable].apply(operation).to_frame().reset_index()
    df_payment = df_filtered.groupby(['Payment'])[main_variable].apply(operation).to_frame().reset_index()
    df_product_income = df_filtered.groupby(["Product line", "City"])[main_variable].apply(operation).to_frame().reset_index()

    fig_city = px.bar(df_city, x='City', y=main_variable)
    fig_payment = px.bar(df_payment, y='Payment', x=main_variable, orientation='h')
    fig_product_income = px.bar(df_product_income, x=main_variable, y="Product line", color="City", orientation="h", barmode='group')
    
    for fig in [fig_city, fig_payment]:
        fig.update_layout(margin=dict(l=0, r=20, t=20, b=20), height=200, template='plotly_dark')
    fig_product_income.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=500, template='plotly_dark')
    
    return fig_city, fig_payment, fig_product_income


# =========== Run Server =========== #
if __name__ == '__main__':
    app.run_server(port=8050, debug=True)

