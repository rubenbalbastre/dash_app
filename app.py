
#  Proyecto de Dash capaz de cargar un dataset (csv) y explorarlo mediante gráficas      interactivas (selección de columnas, tipo de gráfico, etc ...)

import dash
import dash_labs as dl  # pip install dash-labs
import dash_bootstrap_components as dbc
from dash import dcc, html

# app
app = dash.Dash(__name__, plugins=[dl.plugins.pages], external_stylesheets=[dbc.themes.SPACELAB], suppress_callback_exceptions=True) 

# menú
navbar = dbc.NavbarSimple(
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page["module"] != "pages.not_found_404"
        ],
        nav=True,
        label="Páginas",
    ),
    brand="Rubén Balbastre Alcocer App",
    color="primary",
    dark=True,
    className="mb-2",
)

# layout
app.layout = dbc.Container(
    [navbar,
    dcc.Upload(id='upload-data',
                children=html.Div([
                'Por favor, seleccione un archivo a examinar'
                ], style={'width':'500px','display':'inline-block', 'text-align': 'center'}), 
                style={'width': '500px', 'height': '60px', 'lineHeight': '60px', 'borderWidth': '1px',
                'borderStyle': 'dashed', 'borderRadius': '5px', 'text-align': 'center', 'margin': '10px', 'display':'inline-block'},
                # Allow multiple files to be uploaded
                multiple=True
        ),
     dl.plugins.page_container] ,
    fluid=True,
)

# run app
if __name__ == '__main__':
    app.run_server(debug=True)