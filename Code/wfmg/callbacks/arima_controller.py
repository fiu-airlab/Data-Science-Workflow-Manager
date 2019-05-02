from .. import app, cache
from ..dash_app_model import arima_model, arima_df, fare_arima_df, start_index, end_index, today
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output, State
from datetime import datetime
import numpy as np
from .graph_utilities import *

@app.callback([Output('arima-buttons', 'style'), Output('arima-slider-container', 'style')],
              [Input('arima-graph', 'figure')])
@cache.memoize(timeout=timeout) 
def show_buttons_arima(figure):
    return {'visibility': 'visible'}, {'visibility': 'visible'}


@app.callback(Output('training-data-range-arima', 'children'), [Input('training-data-range-arima', 'id')])
def show_training_data_range(id):
    training_df = pd.read_json(cache.get('fare-price-arima-data'))
    size = int(len(training_df) * 0.80)
    x = str(training_df.index[0]).split(' ')[0]
    y = str(training_df.index[size]).split(' ')[0]
    result_string = str(x) + ", " + str(y)
    return "The data used to train the model is the Average Fare Price in the range: " + result_string + " Which is 80% of the data"


@app.callback(Output('arima-train-button', 'disabled'),
              [Input('arima-checkbox', 'values')])
def train_with_button_arima(values):
    if 'button' in values:
        return ""
    else:
        return "true"


@app.callback(Output('arima-data', 'data'),
              [Input('arima-train-button', 'n_clicks')])
def train_model_arima(clicks):
    training_df = pd.read_json(cache.get('fare-price-arima-data'))
    arima_model.fit(training_df)
    new_model_df = arima_model.predict(start_index, end_index)
    cache.set('arima-data', new_model_df.to_json())
    return str(datetime.now())


@app.callback(Output('arima-reset-button', 'name'),
              [Input('arima-reset-button', 'n_clicks')])
def reset_data_arima(n_clicks):
    """ Reset the graph on click. This function sets the data in the cache to the data comming from the inputhandler

        Parameters
        ----------
        n_clicks: int
            A string containing the name of the model. this value is used to create the id's for the components.

        Returns
        -------
        The current date and time and sets the name of the reset button
    """
    cache.set('fare-price-arima-data', fare_arima_df.to_json())
    cache.set('arima-data', arima_df.to_json())
    return str(datetime.now())


@app.callback([Output('arima-point-slider', 'disabled'),
               Output('arima-point-slider', 'max'),
               Output('arima-point-slider', 'min'),
               Output('arima-point-slider', 'value'),
               Output('arima-point-slider', 'marks')],
              [Input('arima-graph', 'selectedData'), Input('arima-reset-button', 'n_clicks')])
@cache.memoize(timeout=timeout) 
def set_slider(selectedData, n_clicks):
    """ Enable the slider when the user clicks on a point in the graph. This function sets the disabled, min, max, and value
        property for the slider component.

        Parameters
        ----------
        selectedData: dict
            A dictionary containing the selected points. this dictionary can be None or it can be a dictionary containing
            the key "points" and the value for this key is a list of points

        Returns
        -------
        The value for the disable, max, min, and the value of the Slider object
    """
    r = 100
    indices = []
    for i in range(-r, r + 1):
        if i % 25 == 0:
            indices.append(i)

    # If the user has not selected any points, then disable the slider
    if selectedData is None:
        return True, r, -r, 0, {i: f"{i}" for i in range(-100, 100 + 1) if i % 25 == 0}

    # If the user selected some points then enable the slider
    points = []
    for i in selectedData['points']:
        if i['curveNumber'] == selected_curve_number:
            points.append(i['y'])

    # get the average of the selected points
    avg = get_average(points)
    if len(points) == 1:
        my_marks = {}
        for m in indices:
            if m == 0:
                my_marks[int(m + avg)] = str(round(m + avg, 2))
            else:
                my_marks[int(m + avg)] = str(round(m + avg))
        return False, avg + r, avg - r, avg, my_marks

    return False, avg + r, avg - r, avg, {int(avg + i): f"{i}" for i in indices}


@app.callback(Output('fare-price-arima-data', 'data'),
              [Input('arima-point-slider', 'value'),
               Input('arima-reset-button', 'name')],
              [State('arima-graph', 'selectedData'), State('arima-checkbox', 'values')])
@cache.memoize(timeout=timeout) 
def update_training_data_arima(value, update_on_reset, selectedData, disabled_checkbox):
    """ Update the fare price data for the visualization and for the training data when the user moves the slider.
        This function is also triggered when the user clicks on the reset button.

        Parameters
        ----------
        value: int
            A dictionary containing the selected points. this dictionary can be None or it can be a dictionary containing
            the key "points" and the value for this key is a list of points.

        update_on_reset: list
            The list of children components in the div with id "modified-data"

        selectedData dict
            A dictionary containing the selected points. this dictionary can be None or it can be a dictionary containing
            the key "points" and the value for this key is a list of points.

        Returns
        -------
        The data that the visualizations are going to consume
    """
    # Get the data from the cache
    cached_data = [cache.get('fare-price-arima-data'), cache.get('arima-data')]
    training_df = pd.read_json(cached_data[0])
    new_model_df = pd.read_json(cached_data[1])
    disabled = True
    if 'button' in disabled_checkbox:
        disabled = False
    # Get the values of the selected points and the index of the points
    y_values = get_y_values(selectedData, selected_curve_number)
    point_indices = get_index_numbers(selectedData, selected_curve_number)
    # get the average to ge the difference and update the real value
    if len(y_values) != 0:
        avg = sum(y_values) / len(y_values)
    else:
        avg = 0
    # Change the dataframe and put it in the cache
    if selectedData is not None:
        updated_value = value - avg
        if updated_value != 0:
            # Update all the changed values
            for i in range(len(point_indices)):
                index = point_indices[i]
                training_df.iloc[index] = y_values[i] + updated_value
            if disabled:
                arima_model.fit(training_df)
                new_model_df = arima_model.predict(start_index, end_index)
                cache.set('arima-data', new_model_df.to_json())
            cache.set('fare-price-arima-data', training_df.to_json())
    updated_on = str(datetime.now())
    return {'fare-price-arima-data': updated_on}


@app.callback(Output('arima-graph', 'figure'),
              [Input('fare-price-arima-data', 'data'),
               Input('arima-data', 'data'),
               Input('arima-graph', 'relayoutData'), Input('arima-graph', 'clickData'),
               Input('columns', 'value')],
              [State('arima-graph', 'selectedData'),
               State('arima-graph', 'figure')])
def make_arima_graph(fare_data_update, arima_data, relayout_data, clickData, columns, selectedData, figure):
    """ This function creates the figure property of the main graph for this model. It draws the graph every time the data
        comming from the cache changes."""
    training_dataframe = pd.read_json(cache.get('fare-price-arima-data'))[:cutoff_date]
    model_dataframe = pd.read_json(cache.get('arima-data'))
    model_y_axis = model_dataframe['FARE']
    model_x_axis = model_dataframe.index
    training_x_axis = training_dataframe.index
    training_y_axis = training_dataframe['AVG_FARE']

    figure = create_model_plot(model_xaxis=model_x_axis, model_yaxis=model_y_axis, train_xaxis=training_x_axis,
                               train_yaxis=training_y_axis, relayout_data=relayout_data, selectedData=selectedData,
                               model_df=model_dataframe, training_df=training_dataframe, model_name='Arima model (Predictive model)',
                               training_data_name='Average Fare Price (Actual price)', title='Average Fare Price with ARIMA Model', columns=columns)
    return figure


@app.callback(Output("fare-price-arima-error", "figure"),
              [Input("fare-price-arima-error", "id"),
               Input('fare-price-arima-data', 'data'),
               Input('arima-graph', 'figure'),
               Input('columns', 'value')])
@cache.memoize(timeout=timeout) 
def make_error_graph_arima(id, data, figure, columns):
    # Get the difference between the fare_price data and the arima model
    narima_df = pd.read_json(cache.get('arima-data'))
    fare_df2 = pd.read_json(cache.get('fare-price-arima-data'))[:cutoff_date]
    narima_df['AVG_FARE'] = narima_df.FARE
    dif_df = narima_df.subtract(fare_df2)
    dif_df = dif_df.dropna(how='all').dropna(axis=1, how='all')
    dif_df

    data = [
        go.Scatter(
            name="ARIMA Error",
            x=dif_df.index,
            y=dif_df['AVG_FARE'],
            mode="lines+markers",
            showlegend=True, line={'color': '#EFE031'}
        )
    ]

    layout = {
        'title': {'text': "Error graph for the ARIMA model", 'font': {'color': '#ffffff'}},
        'xaxis': dict(
            # showline=True,
            ticks="outside",
            type='date',
            color='#ffffff'
        ),
        'yaxis': dict(
            color='#ffffff'
        ),
        'legend': dict(
            font=dict(
                color='#ffffff'
            )
        ),
        'autosize': True,
        'paper_bgcolor': '#00004d',
        'plot_bgcolor': '#00004d'
    }
    return {'data': data, 'layout': layout}
