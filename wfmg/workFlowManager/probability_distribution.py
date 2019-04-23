from .wfmg_proc import WFMG_Proc
import pandas as pd

class ProbabilityDistribution(WFMG_Proc):
    def __init__(self, name, input_stream, output_stream, **kwargs):
                # call __init__ of  WFMG_Proc first and then add needed
                # hyper-parameters example of hyper-parameters: # of bins
                super().__init__(name, input_stream, output_stream,
                                 **kwargs)

    def proc(self):
        #   return  the probability distribution    of  x
        df_proc = self.input_stream
        df_proc = df_proc.sort_values(by='Count', ascending=False)
        df_proc['Percent'] = (df_proc.Count / df_proc.Count.sum() * 100)
        return df_proc