from . import app, server
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from .dash_app_model import *
from .callbacks.graph_utilities import create_interactive_graph

app.index_string = open('./wfmg/templates/dash_view.html', mode='r').read()
background_color = '#00004d'

arima_graph = create_interactive_graph(name='arima', store_component_names=['arima', 'fare-price-arima'])
var_graph = create_interactive_graph(name='var', store_component_names=['var', 'fare-price-var'])
randomforest_graph = create_interactive_graph(name='rf', store_component_names=['rf', 'fare-price-rf'])

tabs_styles = {
    'height': '60px',
    'margin-bottom': '20px',
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'height': '80px',
    'display': 'inline-block'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#c39f34',
    'color': 'white',
    'padding': '6px',
    'height': '80px',
    'display': 'inline-block'
}

app.layout = html.Div([
     html.Div([
        dcc.Dropdown(
            id='columns',
            options=[{'label': i, 'value': i} for i in range(1, 6)],
            value=1,
            style={'width': '5%', 'backgroundColor': background_color, 'color': '#000000'},
            searchable=False
        )
    ]),
    html.Div([
        html.H1('Workflow Manager Dashboard', style={'color': '#ffffff'})
    ], style={'text-align': 'center'}),
    html.Div([
        html.H2('Predictive Models', style={'color': '#ffffff'}),
        html.P("The graphs shown in this section use machine learning models to make predictions about the future price of airline tickets. You can find more information about the models in the sidebar. These graphs are interactive so you can click on any point in the graph that is part of the data used to train the model and change the price value for that specific date. Then you can move the slider to set the value that you want for that point.")
    ]),

    # Main div for the dashboard
    html.Div([
        html.Div([
            dcc.Tabs(id='tabs', children=[
                dcc.Tab(label='AutoRegressive Integrated Moving Average', children=[
                    html.Div([
                        arima_graph,
                        dcc.Graph(id='fare-price-arima-error', figure={'layout': {'paper_bgcolor': background_color,
                                                                                  'plot_bgcolor': background_color}},
                                  className='error-graph')
                    ])
                ], style=tab_style, selected_style=tab_selected_style, className='custom-tab'),
                dcc.Tab(label='Vector autoregression', children=[
                    html.Div([
                        var_graph,
                        dcc.Graph(id='fare-price-var-error', figure={'layout': {'paper_bgcolor': background_color,
                                                                                'plot_bgcolor': background_color}},
                                  className='error-graph')

                    ])
                ], style=tab_style, selected_style=tab_selected_style, className='custom-tab'),
                dcc.Tab(label='Random Forest', children=[
                    html.Div([
                        randomforest_graph,
                        html.Div([
                            dcc.Graph(id='feature-importance-rf', figure={'layout': {'paper_bgcolor': background_color,
                                                                                     'plot_bgcolor': background_color}},
                                      className='feature-importance-graph'),
                            dcc.Graph(id='fare-price-rf-error', figure={'layout': {'paper_bgcolor': background_color,
                                                                                   'plot_bgcolor': background_color}},
                                      className='error-graph')
                        ])
                    ])
                ], style=tab_style, selected_style=tab_selected_style, className='custom-tab')
            ], style=tabs_styles)
        ], id='main_dashboard',),
html.Div([
            html.H2("Distributions", style={'marginTop': '10px', 'color': '#ffffff'}),
            dcc.Dropdown(
                id='distribution-selector',
                value='Coupon Distribution',
                options=[{'label': i, 'value': i} for i in
                         ['Coupon Distribution', 'Fare Class Distribution',
                          'State of Departure Distribution',
                          'Market Share Distribution']],
            ),
            dcc.Graph(id='distribution', figure={'layout': {'paper_bgcolor': background_color,
                                                            'plot_bgcolor': background_color}},
                      className='custom-class-container')
        ], id='distribution-graph-container', style={'marginBottom': '70px', 'display': 'inline-block'}),
        html.Div([
            dcc.DatePickerRange(
                id='cpi-date_input',
                min_date_allowed=df_cpi.DATE.min(),
                max_date_allowed=df_cpi.DATE.max(),
                start_date=df_cpi.DATE.min(),
                end_date=df_cpi.DATE.max(),
                display_format='MM-DD-YYYY',
                start_date_placeholder_text='MM-DD-YYYY'
            ),
            html.H2("Consumer Price Index", style={'marginTop': '10px', 'color': '#ffffff'}),
            dcc.Graph(id='cpi-graph', figure={'layout': {'paper_bgcolor': background_color,
                                                         'plot_bgcolor': background_color}}, #style={'width': '100%'},
                      className='custom-class-container')
        ], id='cpi-graph-container', style={'marginBottom': '40px',
                                            'display': 'inline-block', 'width': '100%'}),

        # Third graph
        html.Div([
            dcc.DatePickerRange(
                id='oil-date_input',
                min_date_allowed=df_oil.DATE.min(),
                max_date_allowed=df_oil.DATE.max(),
                start_date=df_oil.DATE.min(),
                end_date=df_oil.DATE.max(),
                display_format='MM-DD-YYYY',
                start_date_placeholder_text='MM-DD-YYYY'
            ),
            html.H2("Crude Oil Price", style={'marginTop': '10px', 'color': '#ffffff'}),
            dcc.Graph(id='oil-graph', figure={'layout': {'paper_bgcolor': background_color,
                                                         'plot_bgcolor': background_color}}, style={'width': '100%'},
                      className='custom-class-container')
        ], id='oil-graph-container',
            style={'marginBottom': '70px', 'display': 'inline-block', 'width': '100%'}),



    ])
])

from .callbacks import controller
from .callbacks import arima_controller
from .callbacks import var_controller
from .callbacks import rf_controller
