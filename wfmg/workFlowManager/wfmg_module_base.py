from abc import ABC, abstractmethod

class WFMG_ModuleBase(ABC):
    def __init__(self, name, input_stream, output_stream, **kwargs):
        ''' Initialize the name, input, output, and hyperparameters
        name:
            the name of the real model/class
        We can also accept any number of keyword arguments for the hyper-parameters'''
        self.name = name
        self.input_stream = input_stream
        self.output_stream = output_stream
        self.hyperparameters = kwargs

    def set_hyper_para(self, key, value):
        '''This function checks whether the key exists in the dictionary, if not it throws a ValueError exception.
        Otherwise, it sets the value corresponding to the provided key in the dictionary as the provided value'''
        if key in self.hyperparameters.keys():
            # We need to set the value
            self.hyperparameters[key] = value
        else:
            raise ValueError("The key was not found")

    def get_hyper_para(self, key):
        ''' This functions finds the value for the hyper-parameter with name key'''
        if key in self.hyperparameters.keys():
            # We need to return the value
            return self.hyperparameters[key]
        else:
            raise ValueError("The key was not found in the dictionary self.hyper_paras")

