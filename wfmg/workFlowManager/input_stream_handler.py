import pandas as pd
from pandas import datetime
import numpy as np
from abc import ABC, abstractmethod
import os
import pickle


class InputStreamHandler():
    def __init__(self, source, type='disk'):
        """ Initialize the type of the source and the path or name of the source
            Keyword Arguments: 
            type: 
                type of the source, it can be 'disk' or 'memory'
            source:
                if type is 'disk' source should be the path to that file. The file must be a csv file or a pickle file. 
                if the type is set to 'memory' then a copy of that variable will be stored in the object.
        """
        self.type = type
        self.source = source
        self.dataFrame = None
        self.pickle = None

        if self.type == 'memory':
            if isinstance(self.source, pd.DataFrame):
                self.dataFrame = self.source

            elif isinstance(self.source, dict):
                self.dataFrame = pd.DataFrame.from_dict(self.source)

            else:
                raise ValueError("Source must be a DataFrame or a dictionary")

    def load(self, index_name=None):
        """Returns the data from the source as a dataFrame or as a pickle object"""
        # In the outline we discussed that the fuction should return a list of dataframes 
        # but I believe that returning a list is unnecessary and that a single inputStream should contain a single dataframe
        # Since most models use the column for Date as the index, we should also be able to set the index of the data
        #
        if self.type == 'disk':
            (path, ext) = os.path.splitext(self.source)
            # Check if the file is a csv file
            if ext == '.csv':
                if os.path.isfile(self.source):
                    self.dataFrame = pd.read_csv(self.source)
                else:
                    raise FileNotFoundError(f"The file at {self.source} could not be found")
            elif ext == '.pkl':
                if os.path.isfile(self.source):
                    f = open(self.source, 'rb')
                    self.pickle = pickle.load(f)
                else:
                    raise FileNotFoundError(f"The file at {self.source} could not be found")
            else:
                raise ValueError("The source must be a csv file with the extension .csv")

        if self.pickle is None:
            if index_name is not None and index_name in self.dataFrame.columns.values:
                self.dataFrame.index = self.dataFrame[index_name]
                self.dataFrame.index = pd.to_datetime(self.dataFrame.index)
                self.dataFrame = self.dataFrame.drop(index_name, axis=1)
                self.dataFrame.index = pd.DatetimeIndex(self.dataFrame.index.values,
                                                        freq=self.dataFrame.index.inferred_freq)

        return_value = self.pickle or self.dataFrame
        return return_value
