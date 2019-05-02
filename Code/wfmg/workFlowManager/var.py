# Code for the VAR model
from .wfmg_model import WFMG_Model
import pandas as pd
from statsmodels.tsa.vector_ar import var_model
import numpy as np


class VAR(WFMG_Model):
    def __init__(self, input_stream, output_stream, **kwargs):
        super().__init__('VAR', input_stream, output_stream, **kwargs)
        self.training_data = self.input_stream.load(index_name='Date')

    def fit(self, training_df=None):
        """This function fits the loaded model
        Returns:
            model_fit (model): The trained model
        """
        # First load the training data
        if training_df is None:
            train = self.training_data[:int(0.8 * (len(self.training_data)))]
        else:
            train = training_df[:int(0.8 * (len(training_df)))]
            self.training_data = training_df
        # Now fit the model
        model = var_model.VAR(endog=train)
        self.ml_model = model.fit()
        return self.ml_model

    def predict(self, steps=10, start_index=None, end_index=None):
        """This function trains the VAR model to predict the fare
        Keyword arguments:
            start_index(string): start_date string with the format of yy-mm-dd.

            end_index(string): end_date string with the format of yy-mm-dd.
        """
        if self.ml_model is not None:
            self.dataFrame = pd.DataFrame(self.ml_model.forecast(self.ml_model.y, steps=steps))
            self.dataFrame.index = self.training_data[int(0.8 * (len(self.training_data))):].index
        else:
            raise ValueError('No model was found. You need to apply the fit function before predicting')
        return self.dataFrame
