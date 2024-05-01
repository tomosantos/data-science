from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import *

import numpy as np
import plotly.express as px


card_style = {
    'width': '300px',
    'min-height': '300px',
    'padding-top': '25px',
    'padding-right': '25px',
    'padding-left': '25px',
    'align-self': 'center'
}


def render_layout():
    login = dbc.Card([
        html.Legend('Login'),
        
        dbc.Input(id='user-login', placeholder='Username', type='text'),
        dbc.Input(id='pwd-login', placeholder='Password', type='password'),
        dbc.Button('Login', id='login-button'),
        
        html.Span(style={'text-align': 'center'}),
        
        html.Div([
            html.Label('Ou', style={'margin-right': '5px'}),
            dcc.Link('Registre-se', href='/register'),
        ], style={'padding': '20px', 'justify-content': 'center', 'display': 'flex'}),
        
    ], style=card_style)
    
    return login