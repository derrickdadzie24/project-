from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import yfinance as yf
from datetime import datetime
import pandas as pd
import dash_auth

# Define username-password pairs for basic authentication
USERNAME_PASSWORD_PAIRS = [['username', 'password'], ['derrick', 'dadzie']]

# Initialize Dash app
app = Dash(__name__)
server = app.server

# Apply basic authentication to the app
dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)

# Read NASDAQ company list from CSV and set index
nsdq = pd.read_csv('NASDAQcompanylist.csv')
nsdq.set_index('Symbol', inplace=True)

# Create options for dropdown menu
options = [{'label': f'{nsdq.loc[tic]["Name"]} ({tic})', 'value': tic} for tic in nsdq.index]

# Define external stylesheets for custom CSS
external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css']

# Define the layout of the app with warm background color
app.layout = html.Div(
    style={'backgroundColor': '#5e433e', 'color': '#ffffff', 'padding': '20px'},  # Warm background color and white text
    children=[
        html.H1('Stock Ticker Dashboard', style={'textAlign': 'center', 'marginBottom': '30px'}),

        html.Div([
            html.H3('Enter Stock Ticker(s):', style={'marginRight': '30px'}),
            dcc.Dropdown(
                id='my-ticker-symbol',
                options=options,
                value=['TSLA'],
                multi=True,
                style={'fontSize': 20, 'backgroundColor': '#7c5d57', 'color': '#ffffff', 'border': 'none'}
            ),
        ], style={'display': 'inline-block', 'verticalAlign': 'top', 'marginLeft': '10px'}),

        html.Div([
            html.H3('Select Date Range:'),
            dcc.DatePickerRange(
                id='my_date_picker',
                initial_visible_month=datetime.today(),
                min_date_allowed='2015-01-01',
                max_date_allowed=datetime.today(),
                start_date='2020-01-01',
                end_date=datetime.today(),
                with_portal=True,
                style={'backgroundColor': '#7c5d57', 'color': '#ffffff', 'border': 'none'}
            ),
        ], style={'display': 'inline-block', 'marginLeft': '10px'}),

        html.Button(
            id='submit-button',
            n_clicks=0,
            children='Submit',
            style={'fontSize': 15, 'marginLeft': '10px', 'backgroundColor': '#ff7f50', 'color': '#ffffff',
                   'border': 'none', 'padding': '10px 15px', 'cursor': 'pointer'}
        ),

        dcc.Graph(
            id='my-graph',
            figure={'data': [{'x': [1, 2], 'y': [3, 1], 'type': 'scatter', 'name': 'Default Plot'}],
                    'layout': {'title': 'Default Title', 'plot_bgcolor': '#5e433e', 'paper_bgcolor': '#5e433e'}}
        )
    ]
)


# Callback to update graph based on user input
@app.callback(
    Output('my-graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('my-ticker-symbol', 'value'),
     State('my_date_picker', 'start_date'),
     State('my_date_picker', 'end_date')]
)
def update_graph(n_clicks, stock_ticker, start_date, end_date):
    # Convert start_date and end_date to datetime objects
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')

    traces = []
    for tic in stock_ticker:
        # Fetch data from Yahoo Finance
        df = yf.download(tic, start, end)
        traces.append({'x': df.index, 'y': df['Close'], 'name': tic})

    fig = {
        'data': traces,
        'layout': {
            'title': ', '.join(stock_ticker),
            'plot_bgcolor': '#5e433e',  # Plot background color
            'paper_bgcolor': '#5e433e',  # Paper background color
            'font': {'color': '#ffffff'},  # Text color
            'xaxis': {'tickfont': {'color': '#ffffff'}},  # X-axis tick color
            'yaxis': {'tickfont': {'color': '#ffffff'}}  # Y-axis tick color
        }
    }
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8070)
