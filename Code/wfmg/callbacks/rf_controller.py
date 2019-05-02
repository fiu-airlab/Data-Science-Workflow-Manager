import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output, State
from .. import app, cache
from .graph_utilities import *
from datetime import datetime
from ..dash_app_model import rf_model, rf_df, fare_rf_df, today, feature_importance_df


@app.callback([Output('rf-buttons', 'style'), Output('rf-slider-container', 'style')],
              [Input('rf-graph', 'figure')])
def show_buttons_rf(figure):
    return {'visibility': 'visible'}, {'visibility': 'visible'}

@app.callback(Output('training-data-range-rf', 'children'), [Input('training-data-range-rf', 'id')])
def show_training_data_range(id):
    training_df = pd.read_json(cache.get('fare-price-rf-data'))
    size = int(len(training_df) * 0.80)
    x = str(training_df.index[0]).split(' ')[0]
    y = str(training_df.index[size]).split(' ')[0]
    result_string = str(x) + ", " + str(y)
    return "The data used to train the model is the Average Fare Price in the range: " + result_string + " Which is 80% of the data"


@app.callback(Output('rf-train-button', 'disabled'),
              [Input('rf-checkbox', 'values')])
def train_with_button_rf(values):
    if 'button' in values:
        return ""
    else:
        return "true"


@app.callback(Output('rf-data', 'data'),
              [Input('rf-train-button', 'n_clicks')])
def train_model_rf(clicks):
    # we need to train the data and
    training_df = pd.read_json(cache.get('fare-price-rf-data'))
    rf_model.fit(training_df)
    new_model_df = rf_model.predict()
    cache.set('rf-data', new_model_df.to_json())
    return str(datetime.now())


@app.callback(Output('rf-reset-button', 'name'),
              [Input('rf-reset-button', 'n_clicks')])
def reset_data_rf(n_clicks):
    """ Reset the graph on click. This function sets the data in the cache to the data comming from the inputhandler

        Parameters
        ----------
        n_clicks: int
            A string containing the name of the model. this value is used to create the id's for the components.

        Returns
        -------
        The current date and time and sets the name of the reset button
    """
    cache.set('fare-price-rf-data', fare_rf_df.to_json())
    cache.set('rf-data', rf_model.predict().to_json())
    return str(datetime.now())


@app.callback([Output('rf-point-slider', 'disabled'),
               Output('rf-point-slider', 'max'),
               Output('rf-point-slider', 'min'),
               Output('rf-point-slider', 'value'),
               Output('rf-point-slider', 'marks')],
              [Input('rf-graph', 'selectedData'), Input('rf-reset-button', 'n_clicks')])
def set_slider_rf(selectedData, click):
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


@app.callback(Output('fare-price-rf-data', 'data'),
              [Input('rf-point-slider', 'value'),
               Input('rf-reset-button', 'name')],
              [State('rf-graph', 'selectedData'), State('rf-checkbox', 'values')])
def update_training_data_rf(value, update_on_reset, selectedData, disabled_checkbox):
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
    cached_data = [cache.get('fare-price-rf-data'), cache.get('rf-data')]
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
                rf_model.fit(training_df)
                new_model_df = rf_model.predict()
                cache.set('rf-data', new_model_df.to_json())
            cache.set('fare-price-rf-data', training_df.to_json())
    updated_on = str(datetime.now())
    return {'fare-price-rf-data': updated_on}


@app.callback(Output('rf-graph', 'figure'),
              [Input('fare-price-rf-data', 'data'),
               Input('rf-data', 'data'),
               Input('rf-graph', 'relayoutData'),
               Input('rf-reset-button', 'name'),
               Input('columns', 'value')],
              [State('rf-graph', 'selectedData'),
               State('rf-graph', 'figure')])
def make_fare_price_graph_rf(fare_data_update, arima_data, relayout_data, name, columns, selectedData, figure):
    """ This function creates the figure property of the main graph for this model. It draws the graph every time the data
        comming from the cache changes.
    """
    training_dataframe = pd.read_json(cache.get('fare-price-rf-data'))

    model_dataframe = pd.read_json(cache.get('rf-data'))
    model_dataframe = model_dataframe.set_index(training_dataframe[int(len(training_dataframe) * 0.8):].index)

    model_y_axis = model_dataframe['FARE']
    model_x_axis = model_dataframe.index

    t_df = training_dataframe[:cutoff_date]
    training_x_axis = t_df.index
    training_y_axis = t_df['AVG_FARE']

    figure = create_model_plot(model_xaxis=model_x_axis, model_yaxis=model_y_axis, train_xaxis=training_x_axis,
                               train_yaxis=training_y_axis, relayout_data=relayout_data, selectedData=selectedData,
                               model_df=model_dataframe, training_df=t_df, model_name='Random Forest (Predictive model)',
                               training_data_name='Average Fare Price (Actual price)',
                               title='Average Fare Price with Random Forest Model', columns=columns)

    return figure


@app.callback(Output("fare-price-rf-error", "figure"),
              [Input("fare-price-rf-error", "id"),
               Input('fare-price-rf-data', 'data'),
               Input('rf-graph', 'figure'),
               Input('columns', 'value')])
def make_error_graph_rf(id, data, figure, columns):
    nvar_df = pd.read_json(cache.get('rf-data'))
    fare_df2 = pd.read_json(cache.get('fare-price-rf-data'))
    nvar_df['AVG_FARE'] = nvar_df['FARE']
    nvar_df = nvar_df.set_index(fare_df2[int(len(fare_df2) * 0.8):].index)
    dif_df = nvar_df.subtract(fare_df2)
    dif_df = dif_df.dropna(how='all').dropna(axis=1, how='all')[:cutoff_date]

    data = [
        go.Scatter(
            name="Error",
            x=dif_df.index,
            y=dif_df['AVG_FARE'],
            mode="lines+markers",
            showlegend=True, line={'color': '#EFE031'}
        )
    ]

    layout = {
        'title': {'text': "Error graph for the Random Forest Model", 'font': {'color': 'white'}},
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


@app.callback(Output("feature-importance-rf", "figure"),
              [Input("feature-importance-rf", "id"), Input('fare-price-rf-data', 'data'), Input('columns', 'value')])
def make_feature_importance_graph_rf(id, data, columns):
    data = [
        go.Bar(
            x=['Date', 'CPI', 'Oil Price'],
            y=feature_importance_df['importance'],
            marker=dict(
                color='#F3DF2B',
            ),
            opacity=0.6
        )
    ]
    layout = {
        'title': {'text': "Feature Importance", 'font': {'color': 'white'}},
        'xaxis': dict(
            ticks="outside",
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
