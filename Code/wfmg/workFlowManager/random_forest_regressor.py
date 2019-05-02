from .wfmg_model import WFMG_Model
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import numpy as np
from datetime import datetime


class RandomForest(WFMG_Model):
    def __init__(self, input_stream, output_stream, **kwargs):
        super().__init__('VAR', input_stream, output_stream, **kwargs)
        self.ml_model = RandomForestRegressor()
        self.input_data = self.input_stream.load()
        self.training_data = None
        self.feature_importance = None

    def fit(self, training_df=None):
        '''This function fits the loaded model
        Returns:
            model_fit (model): The trained model'''
        # First load the training data
        df_rf = self.input_data
        if training_df is not None:
            avg_fare = training_df['AVG_FARE']
        else:
            avg_fare = df_rf['AVG_FARE']
        df_rf.rename(columns={'key_0': 'Date'}, inplace=True)
        df_rf['Date'] = pd.to_datetime(df_rf['Date']).apply(lambda x: x.toordinal())
        # df_rf['Date'] = df_rf['Date'].apply(datetime.toordinal)
        X_train, X_test, y_train, y_test = train_test_split(df_rf[['Date', 'oil', 'cpi']], avg_fare,
                                                            test_size=0.2, random_state=42)
        self.training_data = X_test # this might have to be the X_train instead
        # Now create and fit the model
        self.ml_model = self.ml_model.fit(X_train, y_train)
        return self.ml_model

    def predict(self, start_index=None, end_index=None):
        """This function trains the VAR model to predict the fare
        Keyword arguments:
            start_date(string): start_date string with the format of yy-mm-dd.

            end_date(string): end_date string with the format of yy-mm-dd.
        """
        model_fit = self.ml_model
        index = self.input_data[int(len(self.input_data)*0.8):].index
        data = model_fit.predict(self.training_data)
        self.dataFrame = pd.DataFrame(columns=['FARE'], data=data)
        return self.dataFrame 
        # if self.ml_model is not None:
        #     model_fit = self.ml_model.fit()
        #     self.dataFrame = pd.DataFrame(model_fit.forecast(model_fit.y, steps=10)
        # else:
        #     raise ValueError('No model was found. You need to apply the fit function before predicting')
        # return self.dataFrame

    def get_feature_importance(self):
        importances = self.ml_model.feature_importances_
        std = np.std([attr.feature_importances_ for attr in self.ml_model.estimators_], axis=0)
        indices = np.argsort(importances)[::-1]

        all_attr = list(self.input_data.columns)
        all_attr.remove('AVG_FARE')  # why do we need to remove the average fare price from the list?
        feature_importance = {'feature': [], 'importance': []}
        for f in range(len(all_attr)):
            feature_importance['feature'].append(all_attr[indices[f]])
            feature_importance['importance'].append(importances[indices[f]])
        return pd.DataFrame(feature_importance)
