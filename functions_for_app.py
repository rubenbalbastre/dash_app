from dash import dcc
from dash import html
import numpy as np

# make break lines
def make_break_lines(num_breaks):
    br_list = [html.Br()] * num_breaks
    return br_list

# select variable
def select_show_variable(data, variable):
    uniques = np.unique(data[variable])
    list = [html.H3('Selecciona un/una'+str(variable)), dcc.Dropdown(options=uniques, value=uniques[0], id=str(variable)+"_dropdown")]
    return list

# create dic
def create_dict_dropdown(data, variable):
    uniques = np.unique(data[variable])
    dict = [{'label':x, 'value':x} for x in uniques]
    return dict

# create dic for columns dropdown
def create_dict_dropdown_columns(data):
    uniques = np.unique(data.columns)
    dict = [{'label':x, 'value':x} for x in uniques]
    return dict
