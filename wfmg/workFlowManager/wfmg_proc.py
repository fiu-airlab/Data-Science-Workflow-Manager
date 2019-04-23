from .wfmg_module_base import WFMG_ModuleBase
from abc import ABC, abstractmethod

class WFMG_Proc(WFMG_ModuleBase):
    def __init__(self, name, input_stream, output_stream, **kwargs):
        # call __init__ of WFMG_ModuleBase first and then
        super().__init__(name, input_stream, output_stream, **kwargs)

    # abstract function of generating result of x
    @abstractmethod
    def proc(self):
        pass






