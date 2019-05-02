import pickle
import pandas as pd 

class OutputStreamHandler():
    def __init__(self, destination, type='disk'):
        """initialize the handler and be able to access the disk/memory as specified and make sure they are available.
        type is a string, either “disk” or “memory”
        destination is either a path to the disk, or a memory holding by this handler"""
        self.type = type
        if type == 'disk':
            self.destination = destination
        elif type == 'memory':
            raise NotImplementedError('The output can\'t be a variable in memory yet')
        else:
            raise ValueError("The type should be disk or memory")

    def save(self, data):
        '''This function saves the data to a file. or to a variable'''
        try:
            file = open(self.destination, 'wb')
            file.write(data)
            file.close() 
        except:
            data.save(self.destination)
        else:
            raise ValueError('the data must be of type str or an object that implements the function save')