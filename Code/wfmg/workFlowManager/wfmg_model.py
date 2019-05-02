import pandas as pd
from .wfmg_module_base import WFMG_ModuleBase
from .input_stream_handler import InputStreamHandler
from abc import ABC, abstractmethod
import pickle

class WFMG_Model(WFMG_ModuleBase):
    def __init__(self, name, input_stream, output_stream, ml_model=None, **kwargs):
        """ Superclass for machine learning models
            Keyword arguments:
            name (string): the name of the model. 

            input_stream (InputStreamHandler): an object of type InputStreamHandler with the source of the raw data.

            ouput_stream (OuputStreamHandler): an object of type OutputStreamHandler with the path to the destination file.
        """
        super().__init__(name, input_stream, output_stream, **kwargs)
        self.ml_model = ml_model
        self.dataFrame = None

    def get_para(self):
        """Returns an array of parameters"""
        return self.hyperparameters

    @abstractmethod
    def predict(self, start_date, end_date):
        """Returns the prediciton data in the range from start_date to end_data""" 
        pass

    @abstractmethod
    def fit(self):
        """Fits the model using the data from the input stream"""
        pass

    def save(self, path=None):
        '''This function saves the model to a pickle file'''
        # We want to dump the contents of self.model into a file specified in the output stream
        # pickled_model = pickle.dumps(self.model)
        # self.output_stream.save(pickled_model)
        if path is None and self.ml_model is not None:
            pickled_model = pickle.dumps(self.ml_model) 
            # Use the outputstream 
            self.output_stream.save(pickled_model)
        if self.ml_model is not None:
            self.ml_model.save(path)
        else:
            raise ValueError("You need to fit the model before saving")

    def load(self, path):
        """Load model from pickle object sotred in a file at path"""
        input_stream = InputStreamHandler(path)
        self.ml_model = input_stream.load()
        return self.ml_model
    
    def get_dataFrame(self):
        return self.dataFrame

