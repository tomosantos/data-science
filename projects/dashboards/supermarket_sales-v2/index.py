import dash
from dash import html, dcc
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from dash_bootstrap_templates import load_figure_template

load_figure_template('minty')


app = dash.Dash(
    external_stylesheets=[
        dbc.themes.MINTY,
        'https://fonts.googleapis.com/css2?family=Voltaire&display=swap'
    ]
    
)
server = app.server


# =========== Ingestão de dados =========== #
df_data = pd.read_csv('supermarket_sales.csv')
df_data['Date'] = pd.to_datetime(df_data['Date'])


# =========== Layout =========== #
app.layout = html.Div(children=[
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H2('ASIMOV', style={'font-family': "Voltaire", 'font-size': '55px'}),
                html.Hr(),
                html.H5("Cidades:"),
                dcc.Checklist(
                    df_data['City'].value_counts().index, 
                    df_data['City'].value_counts().index, 
                    id='check-city', inputStyle={'margin-right': '5px', 'margin-left': '5px'}
                ),
            
                html.H5("Variável de Análise: ", style={'margin-top': '30px'}),
                dcc.RadioItems(['gross income', 'Rating'], "gross income", id='main-variable', inputStyle={'margin-right': '5px', 'margin-left': '5px'}),
                
            ], style={'height': '90vh', 'margin': '20px', 'padding': '20px'})
        ], sm=2),
        
        dbc.Col([
            dbc.Row([
                dbc.Col([dcc.Graph(id='city-fig'),], sm=4),
                dbc.Col([dcc.Graph(id='gender-fig'),], sm=4),
                dbc.Col([dcc.Graph(id='pay-fig'),], sm=4),
            ]),
            dbc.Row([dcc.Graph(id='income-per-date-fig'),]),
            dbc.Row([dcc.Graph(id='income-per-product-fig'),]),
                    
        ], sm=10)
    ])
    
    
])


# =========== Callbacks =========== #
@app.callback([
        Output('city-fig', 'figure'),
        Output('pay-fig', 'figure'),
        Output('gender-fig', 'figure'),
        Output('income-per-date-fig', 'figure'),
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
    df_gender = df_filtered.groupby(['Gender', 'City'])[main_variable].apply(operation).to_frame().reset_index()
    df_payment = df_filtered.groupby(['Payment'])[main_variable].apply(operation).to_frame().reset_index()
    
    df_product_income = df_filtered.groupby(["Product line", "City"])[main_variable].apply(operation).to_frame().reset_index()
    df_income_time = df_filtered.groupby('Date')[main_variable].apply(operation).to_frame().reset_index()

    fig_city = px.bar(df_city, x='City', y=main_variable)
    fig_payment = px.bar(df_payment, y='Payment', x=main_variable, orientation='h')
    fig_gender = px.bar(df_gender, x='Gender', y=main_variable, color="City", barmode='group')
    fig_product_income = px.bar(df_product_income, x=main_variable, y="Product line", color="City", orientation="h", barmode='group')
    fig_income_date = px.bar(df_income_time, y=main_variable, x="Date")
    
    for fig in [fig_city, fig_payment, fig_gender, fig_income_date]:
        fig.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=200, template='minty')
    
    fig_product_income.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=500, template='minty')
    
    return fig_city, fig_payment, fig_gender, fig_income_date, fig_product_income


# =========== Run Server =========== #
if __name__ == '__main__':
    app.run_server(port=8050, debug=True)

