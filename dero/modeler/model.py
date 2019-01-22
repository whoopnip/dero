from sympy import Eq, solve
from dero.modeler.typing import EqList, Any, List, Equation
from dero.ext_sympy.subs import substitute_equations, substitute_equations_ordered


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


