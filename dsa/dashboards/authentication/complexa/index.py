import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from flask_login import current_user
import numpy as np
import pandas as pd

from pages import login, register, data

from app import *

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'

# ==================== Layout ==================== #

app.layout = dbc.Container(
        children=[
                dbc.Row([
                        dbc.Col([
                                dcc.Location(id='base-url', refresh=False),
                                
                                dcc.Store(id='login-state', data=''),
                                dcc.Store(id='register-state', data=''),
                                
                                html.Div(id='page-content', style={'height': '100vh', 'display': 'flex', 'justify-content': 'center'})
                        ]), 
                ])
        ], fluid=True, )

# ==================== Callbacks ==================== #
@login_manager.user_loader
def load_user(user_id):
        return Users.query.get(int(user_id))

@app.callback(
        Output('base-url', 'pathname'),
        [
                Input('login-state', 'data'),
                Input('register-state', 'data')
        ]
)
def render_page_content(login_state, register_state):
        ctx = dash.callback_context
        
        if ctx.triggered:
                trigg_idd = ctx.triggered[0]['prop_id'].split('.')[0]
                
                if trigg_idd == 'login-state' and login_state == 'success':
                        return '/data'
                if trigg_idd == 'login-state' and login_state == 'error':
                        return '/login'
                
                elif trigg_idd == 'register-state':
                        if register_state == '':
                                return '/login'
                        else:
                                return '/register'
                                

@app.callback(
        Output('page-content', 'children'),
        Input('base-url', 'pathname'),
        [
                State('login-state', 'data'),
                State('register-state', 'data')
        ]
)
def render_page_content(pathname, login_state, register_state):
        if (pathname == '/login' or pathname == '/'):
                return login.render_layout(login_state)
        
        if pathname == '/register':
                return register.render_layout(register_state)
        
        if pathname == '/data':
                if current_user.is_authenticated():
                        return data.render_layout(current_user.username)
                else:
                        return login.render_layout(register_state)



if __name__ == '__main__':
    app.run_server(debug=True, port=8051)