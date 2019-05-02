# All the callbacks are placed in this file to avoid having everything in app.py
#
# We also need to create all the graphs with callbacks to follow the MVC design pattern
# The mvc pattern states that we should keep the controller and the view separated
#
# This will be important for updating graphs with events and intervals
from .. import app
import dash
from ..dash_app_model import *
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import datetime
import numpy as np
from abc import *
import datetime
import numpy as np

# =============================
# Filter Data
# =============================


def filter_daterange(df, start_date, end_date):
    dates = df[(df['DATE'] >= start_date) & (df['DATE'] <= end_date)]
    return dates


# All the callbacks are in this file to avoid having everything in app.py
# We also need to create all the graphs with callbacks to follow the MVC design
# pattern The mvc pattern states that we should keep the controller and the
# view separate. This will be important for updating graphs with events and
# intervals
@app.callback(
    dash.dependencies.Output(component_id='cpi-graph',
                             component_property='figure'),
    [dash.dependencies.Input(component_id='cpi-date_input',
                             component_property='start_date'),
     dash.dependencies.Input(component_id='cpi-date_input',
                             component_property='end_date'),
     dash.dependencies.Input(component_id='columns',
                             component_property='value')
     ])
def create_cpi_graph(start_date, end_date, column):
    data = filter_daterange(df_cpi, start_date, end_date)
    if column == None:
        column = 1
    figure = {
        'data': [
            go.Scatter(
                x=data['DATE'],
                y=data['cpi unadjusted'],
                mode='markers+lines',
                marker=dict(
                    color='rgb(158,202,225)',
                    line=dict(
                        color='#ffdd1a',
                        width=1.5,
                    )
                ),
            )
        ],
        'layout': go.Layout(
            xaxis={'title': 'Date', 'color': '#ffffff'},
            yaxis={'title': 'Consumer Price Index', 'color': '#ffffff'},
            hovermode='closest',
            autosize=True,
            paper_bgcolor='#00004d',
            plot_bgcolor='#00004d'
        )
    }
    return figure


@app.callback(
    Output(component_id='oil-graph',
           component_property='figure'),
    [Input(component_id='oil-date_input',
           component_property='start_date'),
     Input(component_id='oil-date_input',
           component_property='end_date'),
     Input(component_id='columns',
           component_property='value')
     ])
def create_oil_graph(start_date, end_date, column):
    data = filter_daterange(df_oil, start_date, end_date)
    if column == None:
        column = 1
    figure = {
        'data': [
            go.Scatter(
                x=data['DATE'],
                y=data['crude oil price'],
                mode='lines',
                marker=dict(
                    color='#ffdd1a',
                    line=dict(
                        color='#ffdd1a',
                        width=1.5,
                    )
                ),
            )
        ],
        'layout': go.Layout(
            xaxis={'title': 'Date', 'color': '#ffffff'},
            yaxis={'title': 'Crude Oil', 'color': '#ffffff'},
            hovermode='closest',
            autosize=True,
            paper_bgcolor='#00004d',
            plot_bgcolor='#00004d'
        )
    }

    return figure


@app.callback(
    Output(component_id='distribution', component_property='figure'),
    [Input(component_id='distribution-selector', component_property='value'),
     Input(component_id='columns', component_property='value')])
def make_distribution_graph(selected_graph, columns):
    """ Returns the graph with the distribution specified by the user.
    At this moment we can accept 'Coupon Distribution',
    Fare Class Distribution', 'State of Departure Distribution',
    'Market Share Distribution' """
    if columns == None:
        columns = 1
    data = []
    layout = []
    if selected_graph == 'Fare Class Distribution':
        # Create a pie chart with the different types of fare classes
        data = [go.Pie(
            labels=[str(i) for i in fare_class_data.FareClass],
            values=fare_class_data.Count,
        )]
        layout = go.Layout(
            autosize=True,
            height=400,
            title={'text': "Fare Class Distribution", 'font': {'color': '#ffffff'}},
            font=dict(color='white'),
            xaxis=dict(color='#ffffff'),
            yaxis=dict(color='#ffffff'),
            legend=dict(font=dict(color='#ffffff')),
            paper_bgcolor='#00004d',
            plot_bgcolor='#00004d'
        )
    elif selected_graph == 'State of Departure Distribution':
        # Create a bar graph with the states and how many planes are departing from each one
        data = [go.Bar(
            x=[str(i) for i in state_data.OriginState],
            y=state_data.Count,
            text=state_data['Percent'].round(2).astype(str) + '%',
            hoverinfo='y+text',
            marker=dict(
                color='#ffdd1a',
                line=dict(
                    color='#ffdd1a',
                    width=1.5,
                )
            ),
        )]
        # This layout is only for graphing the data with the same order as the dataframe in pandas
        layout = go.Layout(
            autosize=True,
            height=400,
            title={'text': "State of Departure Distribution", 'font': {'color': '#ffffff'}},
            xaxis=dict(
                type='category',
                color='#ffffff',
                title='State',
                tickangle=45
            ),
            yaxis=dict(
                color='#ffffff'

            ),

            paper_bgcolor='#00004d',
            plot_bgcolor='#00004d'
        )
    elif selected_graph == 'Market Share Distribution':
        # Make a bar graph with the market share distribution.
        data = [go.Bar(
            y=[str(i) for i in carrier_distrib.Description],
            x=carrier_distrib.Passengers,
            text=carrier_distrib['Percent'].round(2).astype(str) + '%',
            hoverinfo='x+text',
            marker=dict(
                color='rgb(158,202,225)',
                line=dict(
                    color='rgb(8,48,107)',
                    width=1.5,
                )
            ),
            orientation='h'
        )]
        # Since the names the carriers are long, we need to have a large left margin
        layout = go.Layout(
            autosize=True,
            height=800,
            title={'text': "Market Share Distribution", 'font': {'color': '#ffffff'}},
            yaxis=dict(
                type='category',
                title='Carriers ',
                color='#ffffff'
            ),
            xaxis=dict(
                type='category',
                color='#ffffff',
                title='Market Share'
            ),
            margin=go.layout.Margin(
                l=250,
                r=50
            ),
            paper_bgcolor='#00004d',
            plot_bgcolor='#00004d'
        )

    elif selected_graph == 'Coupon Distribution':
        # It would be nice to get the percentages of each coupon
        data = [go.Bar(
            x=[str(i) for i in coupon_data.Coupons],
            y=coupon_data.Count,
            text=coupon_data.Percent.round(2).astype(str) + '%',
            hoverinfo='y+text',
            marker=dict(
                color='#ffdd1a',
                line=dict(
                    color='#ffdd1a',
                    width=1.5,
                )
            ),
        )]
        layout = go.Layout(
            autosize=True,
            height=400,
            title={'text': "Coupon Distribution", 'font': {'color': '#ffffff'}},
            xaxis=dict(
                type='category',
                color='#ffffff',
                title="Number of Coupons"
            ),
            yaxis=dict(
                color='#ffffff',
                title="Number of Tickets sold"
            ),
            paper_bgcolor='#00004d',
            plot_bgcolor='#00004d'
        )
    # Now we just return the dictionary with the data and the layout for the figure value of the distribution graph
    return {
        'data': data,
        'layout': layout
    }


@app.callback(
    [Output('cpi-graph-container', 'style'),
     Output('distribution-graph-container', 'style'),
     Output('oil-graph-container', 'style'),
     Output('main_dashboard', 'style')],
    [Input('columns', 'value')])
def separate_graph_columns(columns):
    style = {'marginBottom': '70px', 'display': 'inline-block','width': str(100 // columns) + '%'}
    return style, style, style, style