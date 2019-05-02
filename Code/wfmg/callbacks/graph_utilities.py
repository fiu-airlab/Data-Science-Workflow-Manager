import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
import plotly.graph_objs as go
import numpy as np
from .. import cache

selected_curve_number = 1
marker_size = 7
selected_marker_size = 13
height = 500
colors = ['#EFE031', '#045EA4']
selected_point_color = '#FAB70D'
cutoff_date = datetime(2017, 1, 1)  # The last value is 2017-10-01
today = cutoff_date
timeout = 60


def sub_months(date):
    if date.month < 6:
        months = 12 + (date.month - 6)
        year = date.year - 1
        new_date = datetime(year, months, date.day)
    else:
        new_date = datetime(date.year, date.month - 6, date.day)
    return np.datetime64(new_date)


def get_average(lst):
    if len(lst) == 0:
        return 0
    return sum(lst) / len(lst)


def add_months(date):
    if date.month > 6:
        months = (date.month + 6) - 12
        year = date.year + 1
        new_date = datetime(year, months, date.day)
    else:
        new_date = datetime(date.year, date.month + 6, date.day)
    return np.datetime64(new_date)


def get_index_numbers(selected_data, curve_number):
    if selected_data is None:
        return []
    selected_points = []
    for point in selected_data['points']:
        if point['curveNumber'] == curve_number:
            selected_points.append(point['pointIndex'])
    return selected_points


def get_y_values(selected_data, curve_number):
    if selected_data is None:
        return []
    selected_points = []
    for point in selected_data['points']:
        if point['curveNumber'] == curve_number:
            selected_points.append(point['y'])
    return selected_points

@cache.memoize(60)
def find_ranges(df1, df2, relayout_data):
    if relayout_data is not None and 'xaxis.range' in relayout_data:
        start = np.datetime64(relayout_data['xaxis.range'][0])
        end = np.datetime64(relayout_data['xaxis.range'][1])
        df1 = df1.loc[start:end]
        df2 = df2.loc[start:end]
    # We need some logic for the cases  where df1 or df2 are empty
    if df2.empty and not df1.empty:  # There is no data in the range
        range_x = [min(df1.index), max(df1.index)]
        range_y = [min(df1[df1.columns[0]]), max(df1[df1.columns[0]])]
    elif df1.empty and not df2.empty:
        range_x = [min(df2.index), max(df2.index)]
        range_y = [min(df2[df2.columns[0]]), max(df2[df2.columns[0]])]
    elif df1.empty and df2.empty:
        return None, None
    else:
        range_x = [min(min(df1.index), min(df2.index)),
                   max(max(df1.index), max(df2.index))]
        range_y = [min(min(df1[df1.columns[0]]), min(df2[df2.columns[0]])),
                   max(max(df1[df1.columns[0]]), max(df2[df2.columns[0]]))]
    range_y[0] -= 20
    range_y[1] += 40
    if relayout_data is not None and 'xaxis.range' in relayout_data:
        range_x[0] = start
        range_x[1] = end
    else:
        range_x = [np.datetime64('2010-07-01'), np.datetime64('2017-11-01')]
    # range_x[0] = range_x[0] - np.timedelta64(30, 'D')
    # range_x[1] = range_x[1] + np.timedelta64(30, 'D')
    return range_x, range_y


def create_interactive_graph(name, store_component_names=[]):
    """ This function creates a div element containing dash_core_component objects. This components can be manipulated
        using callbacks to create user interactions such as point movement, resetting the graph, hovering over points,
        adjusting the range of the graph, etc.

        Parameters
        ----------
        name: str
            A string containing the name of the model. this value is used to create the id's for the components.
        store_component_names: list
            A list containing the store components that are going to be needed in the callbacks.

        Returns
        -------
        dash_html_component.Div
            a div containing all the elements required for the interactive graph
    """
    stores = []
    for store in store_component_names:
        stores.append(dcc.Store(id=f"{store}-data", storage_type='session'))

    element = html.Div(id=f"{name}", className='interactive-graph-container', children=[
        html.Div([
            dcc.Graph(id=f"{name}-graph", className='my-column', animate=False,
                      config={'edits': {'shapePosition': False}, 'displayModeBar': False},
                      figure={'layout': {'paper_bgcolor': '#00004d',
                                         'plot_bgcolor': '#00004d'}})
        ], className='graph-model-container'),
        html.Div(className='vertical-slider', children=[
            dcc.Slider(id=f"{name}-point-slider", className='point-slider', updatemode='mouseup', vertical=True)
        ], style={'visibility': 'hidden'}, id=f"{name}-slider-container"),
        html.Div([
            html.Button(id=f"{name}-reset-button", children='Reset', className='reset-button'),
            html.Button(id=f"{name}-train-button", children='Train', className='train-button'),
            dcc.Checklist(id=f"{name}-checkbox", options=[{'label': 'Click to Train', 'value': 'button'}],
                          values=['button']),
        ], className='graph-buttons', id=f"{name}-buttons"),
        html.Div([
            html.P(id=f"training-data-range-{name}")
        ], style={'margin': '0 auto'})
    ], style = {'width': '100%', 'display': 'inline-block'})
    element.children = element.children + stores
    return element

@cache.memoize(60)
def create_model_plot(model_xaxis, model_yaxis, train_xaxis, train_yaxis, relayout_data, selectedData, model_df,
                      training_df, model_name, training_data_name, title, columns):
    training_dataframe = training_df
    model_dataframe = model_df

    # Objects for the plots
    selected = go.scatter.Selected(marker={'color': selected_point_color, 'size': selected_marker_size})
    selected_points = get_index_numbers(selectedData, selected_curve_number)

    min_yrange_value = min(min(train_yaxis), min(model_yaxis)) - 50
    max_yrange_value = max(max(train_yaxis), max(model_yaxis)) + 50
    slider_range = [min_yrange_value, max_yrange_value]

    # Plots 
    training = go.Scatter(name=training_data_name, x=train_xaxis, y=train_yaxis, mode='lines+markers',
                          selected=selected, selectedpoints=selected_points, marker={'size': marker_size},
                          hoverinfo='x+y', line={'color': colors[0]})

    model = go.Scatter(name=model_name, x=model_xaxis, y=model_yaxis, mode='lines+markers',
                       marker={'size': marker_size},
                       hoverinfo='x+y', line={'color': colors[1]})

    current_date = go.Scatter(name='Current Date', visible=True, showlegend=True, hoverinfo="x", y=[0, 800],
                              x=[today, today], mode='lines', line={'color': '#B22222', 'width': 3.5},
                              hoverlabel={'bgcolor': '#B22222'})

    x_range, y_range = find_ranges(training_dataframe, model_dataframe, relayout_data)

    layout = {'clickmode': 'select+event',
              'dragmode': 'select',
              'hovermode': 'x',
              'height': height,
              'autosize': True,
              'title': {'text': title, 'font': {'color': 'white'}},
              'xaxis': dict(
                  showline=True,
                  ticks="outside",
                  range=x_range,
                  fixedrange=True,
                  rangeslider=dict(
                      visible=True,
                      thickness=0.10,
                      yaxis={
                          'rangemode': 'fixed',
                          'range': slider_range
                      },
                  ),
                  color='#ffffff'
              ),
              'yaxis': dict(
                  range=y_range,
                  fixedrange=True,
                  title='Fare Price',
                  color='#ffffff'
              ),
              'gridcolor': "white",
              'legend': dict(
                  font=dict(
                      color='#ffffff'
                  )
              ),
              'paper_bgcolor': '#00004d',
              'plot_bgcolor': '#00004d'
              }

    return {'data': [current_date, training, model], 'layout': layout}
