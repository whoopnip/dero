from typing import Dict, List, Union, Any
from sympy import Eq
from dero.ext_sympy.indexed import IndexedEquation

Equation = Union[Eq, IndexedEquation]
EqList = List[Equation]
