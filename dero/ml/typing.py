from typing import List, Dict, Optional, Union
import pandas as pd

ModelParam = Optional[Union[str, int, float]]
ParamDict = Dict[str, ModelParam]
ModelDict = Dict[str, Union[ParamDict, float]]
AllModelResultsDict = Dict[str, List[ModelDict]]
DfDict = Dict[str, pd.DataFrame]