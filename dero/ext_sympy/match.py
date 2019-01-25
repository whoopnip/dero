from typing import List, Optional
from sympy import Expr, Eq


def get_equation_where_lhs_matches(match_expr: Expr, equations: List[Eq]) -> Optional[Eq]:
    for equation in equations:
        if equation.lhs == match_expr:
            return equation

    return None
