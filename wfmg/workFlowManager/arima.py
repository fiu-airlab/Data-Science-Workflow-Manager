from .wfmg_model import WFMG_Model 
import pandas as pd
from statsmodels.tsa import arima_model 
import numpy as np  

def predict(coef, history):
    yhat = 0.0
    for i in range(1, len(coef)+1):
        yhat += coef[i-1] * history[-i]
    return yhat

def difference(dataset):
    diff = list()
    for i in range(1, len(dataset)):
        value = dataset[i] - dataset[i - 1]
        diff.append(value)
    return np.array(diff)

class ARIMA(WFMG_Model):
    def __init__(self, input_stream, output_stream, **kwargs):
        super().__init__('ARIMA', input_stream, output_stream, **kwargs)
        self.input_data = self.input_stream.load(index_name='DATE')

    def predict(self, start_index, end_index):
        """This function trains the ARIMA model to predict the fare
        Keyword arguments:
            start_date(string): start_date string with the format of yy-mm-dd.

            end_date(string): end_date string with the format of yy-mm-dd.
        """
        if self.ml_model is not None:
            X = self.input_data.values
            size = int(len(X) * 0.80)
            train, test = X[0:size], X[size:]
            history = [x for x in train]
            predictions = []
            # ARIMA rolling forecast
            for t in range(len(test)):
                model = arima_model.ARIMA(history, order=(3,1,0))
                model_fit = model.fit(disp=0)
                ar_coef, ma_coef = model_fit.arparams, model_fit.maparams
                resid = model_fit.resid
                diff = difference(history)
                yhat = history[-1] + predict(ar_coef, diff) + predict(ma_coef, resid)
                predictions.append(yhat)
                obs = test[t]
                history.append(obs)
            X = self.input_data
            test = X[size:]
            self.dataFrame = pd.DataFrame(columns=['FARE'], index=test.index, data=predictions)
        else:
            raise ValueError('No model was found. You need to apply the fit function before predicting')
        return self.dataFrame

    def fit(self, training_df=None):
        '''This function fits the loaded model
        Returns:
            model_fit (model): The trained model'''
        if training_df is None:
            input_data = self.input_data
        else:
            input_data = training_df
            self.input_data = training_df
        size = int(len(input_data)*0.80)
        data_train = input_data[0:size]
        model = arima_model.ARIMA(data_train, order=self.hyperparameters['order'])
        self.ml_model = model.fit(disp=0)
        return self.ml_model