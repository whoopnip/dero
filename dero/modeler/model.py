from copy import deepcopy
from sympy import Eq, solve, Expr
from dero.modeler.typing import EqList, Any, List, Equation, EquationOrNone
from dero.ext_sympy.subs import substitute_equations, substitute_equations_ordered
from dero.ext_sympy.match import get_equation_where_lhs_matches


class Model:

    def __init__(self, equations: EqList):
        self.set_equations(equations)

    def set_equations(self, equations: EqList):
        self.equations = []
        self.evaluated_equations = []
        for equation in equations:
            self.equations.append(equation)
            if hasattr(equation, 'is_IndexedEquation') and equation.is_IndexedEquation:
                self.evaluated_equations.extend(equation.evaluated_index_eqs)
            else:
                self.evaluated_equations.append(equation)

    def sub_eq(self, eq: Equation, deep_substitute: bool = True) -> Eq:
        if deep_substitute:
            return substitute_equations(eq, self.evaluated_equations)
        else:
            return substitute_equations_ordered(eq, self.evaluated_equations)

    def solve(self, *symbols, **flags):
        return solve(self.evaluated_equations, *symbols, **flags)

    def get_eq_for(self, lhs_expr: Expr) -> EquationOrNone:
        return get_equation_where_lhs_matches(lhs_expr, self.evaluated_equations)

    def subs(self, *args, **kwargs):
        new_model = deepcopy(self)
        new_model.equations = [eq.subs(*args, **kwargs) for eq in self.equations]
        new_model.evaluated_equations = [eq.subs(*args, **kwargs) for eq in self.evaluated_equations]

        # TODO: deep sub, run on loop, extract definitions so they don't evaluate as true. stop when equations stop changing.
        new_model._eliminate_useless_eqs()  # need to do before reevaluating as expecting eq but have True
        new_model._reevaluate_eqs()
        new_model._eliminate_useless_eqs()  # need to do again after reevaluating as some are newly True

        return new_model

    def _eliminate_useless_eqs(self):
        self.equations = [eq for eq in self.equations if not eq == True]
        self.evaluated_equations = [eq for eq in self.evaluated_equations if not eq == True]

    def _reevaluate_eqs(self):
        self.equations = [
            substitute_equations_ordered(eq, self.equations) for eq in self.equations
        ]
        self.evaluated_equations = [
            substitute_equations_ordered(eq, self.evaluated_equations) for eq in self.evaluated_equations
        ]





