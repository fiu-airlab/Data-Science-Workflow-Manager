from .wfmg_proc import WFMG_Proc
import pandas as pd

class FrequencyDistribution(WFMG_Proc):
    def __init__(self, name, input_stream, output_stream, **kwargs):
        # call __init__ of WFMG_Proc first and then add needed
        # hyper-parameters
        # example of hyper-parameters: number of bins
        super().__init__(name, input_stream, output_stream, **kwargs)

    def proc(self):
        #   return  the frequency   distribution    of  x
        arg = super().get_hyper_para('distrib')
        df = self.input_stream[arg].value_counts()
        df_proc = pd.DataFrame({arg: df.index, 'Count': df.values})
        return df_proc