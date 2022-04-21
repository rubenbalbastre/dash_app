import dash

name = "Página principal"

dash.register_page(__name__, path="/", title=name, name=name)

from dash import dcc, html, Input, Output, State, callback, dash_table
import pandas as pd
from dash import dcc
from dash import html
import pandas as pd
from dash.dependencies import Input, Output, State
import base64
import io
from dash import dash_table
import functions_for_app as ftapp
import plotly.express as px


# image
logo_link = "https://www.uv.es/fatwireed/userfiles/file/logo_UV_ETSEUV_4lineas.gif" 

description = """Esto es una aplicación desarrollada para la exploración de un csv.
Se incluyen tres páginas: la principal para explorar los datos perdidos, la segunda para explorar la relación
entre 2 variables y la tercera para examinar la distribución de 1 variable."""

# layout

layout = html.Div(children=[
    *ftapp.make_break_lines(1),
   # cabecera
    html.Div( 
        children=[
        # UV logo
        html.Div(
             html.Img(src=logo_link, 
            style={ 'width':'250px' , 'border':'1px solid black'} ),style={'display':'inline-block', 'padding-right':'10%'} # 'width': '400px' ,'padding-right':'55%'
                 ), 
        # título
        html.Div(
            children=[html.H2('Visualización Avanzada de Datos - Análisis CSV'), html.H3("Máster Ciencia de Datos - UV"), html.H3("Rubén Balbastre Alcocer - rubalal@alumni.uv.es")], 
            style={"border":'1px solid black','vertical-align':'top','width':'750px','height':'150px' ,'display':'inline-block'}) ]
            ),
    *ftapp.make_break_lines(1),

    # descripción
    html.Div(children=html.P(description),style={'width':'1000px','display':'inline-block'}),

    # submit csv
    html.Div(children=[
        
        html.Div(id='output-datatable')
    ])
], style={'text-align':'center', 'display':'inline-block', 'width':'100%', 'height':'100%'}) #, 'backgroundColor':'lightblue'


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
    return html.Div([
        # info
        html.Hr(),
        html.H3(filename),
        # table information
        html.H5(children=[str(df.shape[0])+" filas y "+str(df.shape[1])+" columnas"]),
        html.H5(children=["Número total de datos faltantes: "+str(df.isnull().sum().sum())]),
        html.Hr(),
        html.Button(id='info-NA-button', children='Mostrar NA info', style={'width':'500px','height':'50px', 'display':'inline-block'}),
        html.Div(id='info-NA'),
        # html.Hr(),
        # html.Button(id='na-remove-button', children='Imputar NA con la media', style={'width':'500px','height':'50px', 'display':'inline-block'}),
        # html.Hr(),
        html.Br(),
        # table
        dash_table.DataTable(data=df.to_dict('records'), columns=[{'name':i,'id':i} for i in df.columns], page_size=10),
        html.Hr(),
        dcc.Store(id="stored-data", data=df.to_dict('records')) 
        ])
   
# mostrar NA info

def show_na(df):
    x = df.isnull().sum()
    list = []
    vars = []
    for i in range(df.shape[1]):
        if x[i] !=0:
            list.append(x[i])
            vars.append( df.columns[i] )
    dataframe = pd.DataFrame({'variables':vars, 'cuentas':list})
    return dataframe

@callback(Output('info-NA','children'), [Input('info-NA-button', 'n_clicks'), Input('stored-data', 'data')])

def show_na_info(n, data):
    data2 = pd.DataFrame(data).copy(deep=True)
    df = show_na(data2)
    fig = px.bar(df, x='variables', y='cuentas', title="Número de NA por variable")
    if n !=None and n % 2 != 0:
        return dcc.Graph(figure=fig)

# # eliminar NA

# @callback(Output('stored-data-post', 'data'), [Input('stored-data', 'data'), Input('na-remove-button', 'n_clicks')])

# def update_data(data, n):
#     df = pd.DataFrame(data).copy(deep=True)
#     if n !=None and n % 2 != 0:
#         dataframe = show_na(df)
#         for var in dataframe['variables']:
#             df[var][df[var].isna()] = np.mean(df[var].dropna())
#         return df.to_dict('records')
#     else:
#         return df.to_dict('records')


# mostrar tabla

@callback(Output('output-datatable', 'children'),
              [Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])

def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

