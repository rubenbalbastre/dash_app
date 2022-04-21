import dash

name = "Análisis de 1 variable"
dash.register_page(__name__, path="/univariate_page", title=name, name=name)

from dash import dcc, html, Input, Output, callback, State
import plotly.express as px
import pandas as pd
import functions_for_app as ftapp
from scipy.stats import shapiro
import base64
import io



# histograma

layout = html.Div(children=[   
        html.Div(id='output-data')  
        ],
        style={'display':'inline-block', 'width':'100%', 'text-align':'center'})



# upload csv
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
    return dcc.Store(id='stored-data', data=df.to_dict('records'))


# cargar datos
@callback(Output('output-data', 'children'),
              [Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])

def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return [children[0],
                # título
                html.H4("Análisis uni-variable", style={'display':'inline-block'}),
                # histograma
                html.P('Selecciona una variable'),
                html.Div(dcc.Dropdown(id='histogram_variable', style={'width':'300px','display':'inline-block'}), style={'width':'500px', 'display':'inline-block'}), # scatter plot
                html.Br(),
                html.P('Selecciona un número de bins'), 
                html.Div(dcc.Slider(value=2, min=2, max=30, step=4, marks={x:str(x) for x in range(2,31,4)},  id='input_nbins' ), style={'width':'300px','display':'inline-block'}),
                html.Br(),
                html.Div(html.Button(id='n_clicks_histogram', children="Plot", style={'display':'inline-block'}),style={'width':'500px', 'display':'inline-block'}),
                html.Br(),html.Br(),
                html.Button(id='n_clicks_shapiro-test', children="Shapiro-test", style={'width':'500px', 'display':'inline-block'}),
                html.Br(),html.Br(),
                html.Div(id='shapiro-test',style={'width':'500px', 'display':'inline-block'}),
                html.Div(id='histogram_plot')]


# opciones histogramas - nbins

@callback(Output('histogram_variable','options'),
    Input('stored-data','data'))

def make_histograms_options(data):
    df = pd.DataFrame(data).copy(deep=True)
    return ftapp.create_dict_dropdown_columns(df)

# histograma

@callback(Output('histogram_plot','children'),
        [Input('n_clicks_histogram','n_clicks'),
        Input('histogram_variable','value'),
        Input('input_nbins','value'),
        Input('stored-data','data')])

def plot_histograms(n, variable, nbins, data):
    df = pd.DataFrame(data).copy(deep=True)
    if n != None:
        bar_fig = px.histogram(df, x=variable, nbins=nbins)
        return  dcc.Graph(figure=bar_fig)

# shapiro test

@callback(Output('shapiro-test','children'),
            [Input('n_clicks_shapiro-test','n_clicks'),
            Input('stored-data', 'data'), 
            Input('histogram_variable','value')])

def shapiro_test(n, data, var):
    df = pd.DataFrame(data).copy(deep=True).dropna()
    if n != None and n%2 != 0:
        pvalor = shapiro(df[var].to_numpy()).pvalue
        return html.P("pvalor del test de normalidad de Shapiro-Wilk: "+str(pvalor))
