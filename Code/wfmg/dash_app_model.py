""" This File should be replaced with a database"""
import pandas as pd
from . import cache
import datetime
from .workFlowManager.arima import ARIMA
from .workFlowManager.var import VAR
from .workFlowManager.random_forest_regressor import RandomForest
from .workFlowManager.input_stream_handler import InputStreamHandler
from .workFlowManager.output_stream_handler import OutputStreamHandler
import numpy as np
from .workFlowManager.frequency_distribution import *
from .workFlowManager.probability_distribution import *
import datetime
from .callbacks.graph_utilities import create_interactive_graph

today = datetime.datetime(2017, 1, 1)

# dictionary of hyper-parameters to be used. Hyperparameters will be set by each distribution
arima_input_handler = InputStreamHandler('./Data/Fare_senior_project.csv')
arima_output_handler = OutputStreamHandler('arima.pkl')
arima_model = ARIMA(arima_input_handler, arima_output_handler, order=[3, 1, 0])
start_index = '2015-01-01'
end_index = '2017-10-01'
arima_model.fit()
arima_df = arima_model.predict(start_index, end_index)
fare_arima_df = arima_input_handler.load(index_name='DATE')
cache.set('fare-price-arima-data', fare_arima_df.to_json())
cache.set('arima-data', arima_df.to_json())

var_input = InputStreamHandler('./Data/Merged_senior_project.csv')
var_output = OutputStreamHandler('var.pkl')
var_model = VAR(var_input, var_output)
var_model.fit()
var_df = var_model.predict()
fare_var_df = var_input.load(index_name='Date')
cache.set('fare-price-var-data', fare_var_df.to_json())
cache.set('var-data', var_df.to_json())

custom_input = InputStreamHandler('./Data/Merged_senior_project.csv')
test_ouput_handler = OutputStreamHandler('rf.pkl')
rf_model = RandomForest(custom_input, test_ouput_handler)
rf_model.fit()
feature_importance_df = rf_model.get_feature_importance()
rf_df = rf_model.predict()
fare_rf_df = arima_input_handler.load(index_name='DATE')
cache.set('fare-price-rf-data', fare_rf_df.to_json())
cache.set('rf-data', rf_df.to_json())
cache.set('feature-importance', feature_importance_df.to_json())

# dataframe for the Oil Price
df_oil = pd.read_csv('./Data/Oil_senior_project.csv')

# dataframe for the CPI
df_cpi = pd.read_csv('./Data/CPI_senior_project.csv')

# Fare Class distribution
coupon_input_handler = InputStreamHandler('./Data/filtered_coupon_data_2018_demo.csv')
coupon_input_handler = coupon_input_handler.load()
coupon_output_handler = OutputStreamHandler('./Data/filtered_coupon_data_2018_demo.csv')
fare_class_data = FrequencyDistribution('FareClass', coupon_input_handler, coupon_output_handler, distrib='FareClass')
fare_class_data = fare_class_data.proc()

# State Of Departure Distrbution
state_data = FrequencyDistribution('State', coupon_input_handler, coupon_output_handler, distrib='OriginState')
state_data = state_data.proc()
state_data = ProbabilityDistribution('Coupon', state_data, state_data,
                                     distrib='OriginState')
state_data = state_data.proc()

# Coupon Distrbution
coupon_data = FrequencyDistribution('Coupon', coupon_input_handler, coupon_output_handler, distrib='Coupons')
coupon_data = coupon_data.proc()
coupon_data = ProbabilityDistribution('Coupon', coupon_data, coupon_data,
                                      distrib='Coupons')
coupon_data = coupon_data.proc()

carrier_distrib = coupon_input_handler.groupby(['RPCarrier'])['Passengers'].sum().sort_values(ascending=False)
carrier_key = pd.read_csv('./Data/L_CARRIERS.csv')
carrier_key = carrier_key.rename(columns={'Code': 'RPCarrier'})
carrier_distrib = pd.merge(carrier_distrib, carrier_key, on='RPCarrier')
carrier_distrib['Percent'] = carrier_distrib['Passengers'] / carrier_distrib['Passengers'].sum() * 100
carrier_distrib = carrier_distrib.sort_values(by='Passengers', ascending=True)
