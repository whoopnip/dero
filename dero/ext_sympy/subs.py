from typing import List
from sympy import Eq, Expr


def substitute_equations(orig_eq: Eq, sub_eqs: List[Eq]) -> Eq:
    for_sub = [eq for eq in sub_eqs if eq is not orig_eq]
    eq = orig_eq
    # TODO: more efficient algorithm
    for i in range(len(sub_eqs)):
        eq = substitute_equations_ordered(eq, for_sub)
    return eq


def substitute_equations_ordered(orig_eq: Eq, sub_eqs: List[Eq]) -> Eq:
    all_subs = [(eq.lhs, eq.rhs) for eq in sub_eqs]
    return orig_eq.subs(all_subs)
