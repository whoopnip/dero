from typing import List, Dict, Optional, Union, Any
import pandas as pd

ModelParam = Optional[Union[str, int, float]]
ParamDict = Dict[str, ModelParam]
ModelDict = Dict[str, Union[ParamDict, float]]
AllModelResultsDict = Dict[str, List[ModelDict]]
DfDict = Dict[str, pd.DataFrame]

ModelOptionPossibilitiesDict = Dict[str, List[Any]]
AllModelOptionPossibilitiesDict = Dict[str, ModelOptionPossibilitiesDict]
AllModelKwargs = List[Dict[str, Any]]
AllModelKwargsDict = Dict[str, AllModelKwargs]