from dash import Dash, html, dcc
from dash.dependencies import Input,Output, State
import yfinance as yf
from datetime import datetime #https://stackoverflow.com/questions/15707532/import-datetime-v-s-from-datetime-import-datetime
import pandas as pd
import dash_auth

USERNAME_PASSWORD_PAIRS=[['username', 'password'], ['derrick', 'dadzie']]

app = Dash(__name__)
server = app.server
dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)

nsdq = pd.read_csv('NASDAQcompanylist.csv')
nsdq.set_index('Symbol', inplace = True)

options = []

for tic in nsdq.index:
    mydict = {}
    mydict['label'] = nsdq.loc[tic]['Name']+' '+tic
    mydict['value'] = tic
    options.append(mydict)

#https://www.w3schools.com/css/css_dropdowns.asp
app.layout = html.Div([
            html.H1('Stock Ticker Dashboard'),
            html.Div([
                html.H3('Enter a Stock Ticker:', style = {'paddingRight':'30px'}),
                dcc.Dropdown(id = 'my-ticker-symbol',
                          options = options,
                          value = ['TSLA'],
                          multi = True,
                          style = {'fontSize':20}
                          )],#style={'fontSize': 20, 'width': 150}
                style={'display': 'inline-block', 'verticalAlign': 'top', 'color': 'blue', 'marginLeft': '10px'}),
            html.Div([html.H3('Select a start and end date:'),
                     dcc.DatePickerRange(id = 'my_date_picker',
                                         initial_visible_month= datetime.today(),
                                         min_date_allowed='2015-1-1',
                                         max_date_allowed=datetime.today(),
                                         start_date = '2020-1-1',
                                         end_date = datetime.today(),
                                         with_portal = True)
                      ], style = {'display': 'inline-block'}),
            html.Button(id = 'submit-button',
                        n_clicks = 0,
                        children = 'Submit',
                        style={'fontSize': 15,'marginLeft':'10px', 'color':'white', 'color-scheme': 'dark'}),
            dcc.Graph(id='my-graph',
                        figure={'data': [
                                 {'x': [1, 2], 'y': [3, 1]}
                                ], 'layout': {'title': 'Default Title'}})
])

@app.callback(Output('my-graph', 'figure'),
              [Input('submit-button', 'n_clicks')],
              [State('my-ticker-symbol', 'value'),
               State('my_date_picker','start_date'),
               State('my_date_picker','end_date')
               ])

def update_graph(n_clicks, stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10],'%Y-%m-%d')
    end  = datetime.strptime(end_date[:10],'%Y-%m-%d')

    traces = []
    for tic in stock_ticker:
        df = yf.download(tic, start, end)
        traces.append({'x': df.index, 'y': df['Close'],'name': tic})

    fig = {
            'data': traces,
            'layout': {'title': stock_ticker}}
    return fig

if __name__ == '__main__':
    app.run(debug = True, port = 8070)