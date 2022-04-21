import dash

name= "Análisis de 2 variables"
dash.register_page(__name__, path="/bivariate_page", title=name, name=name)

from dash import dcc, html, Input, Output, callback, State
import plotly.express as px
import pandas as pd
import base64
import io



# ANÁLISIS BI VARIBLE

layout = html.Div(children=[    
        html.Div(id='output-data2')
        ],
        style={'display':'inline-block', 'width':'100%', 'text-align':'center'} )

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
@callback(Output('output-data2', 'children'),
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
                html.H4("Análisis de dos variables", style={'display':'inline-block'}),
                # seleccionar ejes
                html.Div([
                        html.Div([
                            html.P("Seleccione la variable X"),
                            dcc.Dropdown(id="xaxis", style={'width':'300px','display':'inline-block'})],
                            style={'display':'inline-block', 'margin':'10px'})
                        , 
                        html.Div([
                            html.P("Seleccione la variable Y"),
                            dcc.Dropdown(id="yaxis", style={'width':'300px','display':'inline-block'})],
                            style={'display':'inline-block', 'margin':'10px'}), 
                ]),

                # log-scale
                html.Div([
                    html.Div([
                        html.P("Selecciona la escala X"),
                        dcc.Dropdown(id='log-scale-x',options=[{'label':v,'value':v} for v in ["Lineal","Log"]], value="Lineal", children="Log Scale Y", style={'width':'300px','display':'inline-block'}),
                    ],
                    style={'display':'inline-block', 'margin':'10px'}),
                    html.Div([
                        html.P("Selecciona la escala Y"),
                        dcc.Dropdown(id='log-scale-y', options=[{'label':v,'value':v} for v in ["Lineal","Log"]], value="Lineal", children="Log Scale X", style={'width':'300px','display':'inline-block'})
                    ],
                    style={'display':'inline-block','margin':'10px'})
                    
                ]),
                
                # tipo de plot
                html.Div([
                    html.Button(id="scatter-plot-button", children="Scatter plot", style={'display':'inline-block','margin':'10px'}),
                    html.Button(id="box-plot-button", children="Box plot", style={'display':'inline-block','margin':'10px'}),
                    html.Button(id="trend-line-button", children="Regresión Lineal", style={'display':'inline-block','margin':'10px'})
                    #html.Button(id="mosaic-plot-button", children="Mosaic plot", style={'display':'inline-block','margin':'10px'})
                    ]),
                # plot
                html.Div(id='scatter-plot')]

# x
@callback(Output('xaxis','options'),
    Input('stored-data','data'))

def select_xaxis(data):
    df = pd.DataFrame(data).copy(deep=True)
    return [{'label':x, 'value':x} for x in df.columns]

# y
@callback(Output('yaxis','options'),
    Input('stored-data','data'))

def select_yaxis(data):
    df = pd.DataFrame(data).copy(deep=True)
    return [{'label':x, 'value':x} for x in df.columns]

# plot
@callback(Output('scatter-plot', 'children'),
            [Input('xaxis', 'value'),
            Input('yaxis', 'value'),
            Input('scatter-plot-button', 'n_clicks'),
            Input('box-plot-button', 'n_clicks'),
            Input('stored-data', 'data'),
            Input('log-scale-y','value'),
            Input('log-scale-x','value'),
            Input('trend-line-button','n_clicks')
            # Input('mosaic-plot-button', 'n_clicks'),
            ])


def plot_histogram(x_data, y_data, n_scatter, n_box, data, n_logy, n_logx, ntrendline):
    df = pd.DataFrame(data).copy(deep=True)
    # scatter plot
    if n_scatter != None and n_scatter % 2 != 0:

        if ntrendline != None and ntrendline % 2 != 0:
            fig = px.scatter(df,x=x_data, y=y_data)
        else:
            fig = px.scatter(df,x=x_data, y=y_data , trendline="ols")

        if n_logx == "Log" and n_logy =="Lineal":
            if ntrendline != None and ntrendline % 2 != 0:
                fig = px.scatter(df,x=x_data, y=y_data, log_x=True, trendline="ols")
            else:
                fig = px.scatter(df,x=x_data, y=y_data, log_x=True)

        if n_logy =="Log" and n_logx == "Lineal":
            if ntrendline != None and ntrendline % 2 != 0:
                fig = px.scatter(df,x=x_data, y=y_data, log_y=True, trendline="ols")
            else:
                fig = px.scatter(df,x=x_data, y=y_data, log_y=True)

        if n_logy == "Log" and n_logx == "Log":
            if ntrendline != None and ntrendline % 2 != 0:
                fig = px.scatter(df,x=x_data, y=y_data, log_y=True, log_x=True)
            else:
                fig = px.scatter(df,x=x_data, y=y_data, log_y=True, log_x=True)

        return dcc.Graph(figure=fig)
    
    # boxplot
    elif n_box != None and n_box % 2 != 0:
        fig = px.box(df,x=x_data, y=y_data)
        return dcc.Graph(figure=fig)
    # elif n_mosaic != None and n_mosaic % 2 != 0:
        # fig, rects = mosaic(df, [x_data, y_data])
        # return dcc.Graph(figure=mpl_to_plotly(fig))
