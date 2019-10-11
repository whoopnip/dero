from copy import deepcopy
from typing import Union

from sympy import Eq, solve, Expr

from dero.ext_sympy.indexed import IndexedEquation
from dero.ext_sympy.solver import solved_equation
from dero.modeler.typing import EqList, Any, List, Equation, EquationOrNone
from dero.ext_sympy.subs import substitute_equations, substitute_equations_ordered
from dero.ext_sympy.match import get_equation_where_lhs_matches


class Model:

    def __init__(self, equations: EqList):
        self.equations = []
        self.evaluated_equations = []
        self._definitions = []
        self._evaluated_definitions = []
        self.set_equations(equations)

    def set_equations(self, equations: EqList):
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
        new_model._separate_definitions()  # without this some may become True on the first substitution
        new_model.equations = [eq.subs(*args, **kwargs) for eq in self.equations]
        new_model.evaluated_equations = [eq.subs(*args, **kwargs) for eq in self.evaluated_equations]

        # prior_eqs = new_model.equations.copy()
        prior_eval_eqs = new_model.evaluated_equations.copy()
        finished = False
        while not finished:
            ###
            # TEMP
            breakpoint()
            print('solving equations')
            ###
            new_model._separate_definitions()
            new_model._reevaluate_eqs()
            new_model._eliminate_useless_eqs()
            finished = (
                # prior_eqs == new_model.equations and
                prior_eval_eqs == new_model.evaluated_equations
            )
            # prior_eqs = new_model.equations.copy()
            prior_eval_eqs = new_model.evaluated_equations.copy()

        new_model._add_definitions_into_equations()

        return new_model

    def _separate_definitions(self):
        """
        Separate equations once they have only a single symbol, and store as a definition.
        This is necessary as continued substitutions will make the equation evaluate as True
        So a fully evaluated model without this would just be a list of True
        """

        self._definitions.extend(_pop_solved_equations_from_list(self.equations))
        self._evaluated_definitions.extend(_pop_solved_equations_from_list(self.evaluated_equations))

    def _add_definitions_into_equations(self):
        self.equations.extend(self._definitions)
        self.evaluated_equations.extend(self._evaluated_definitions)

    def _reevaluate_eqs(self):
        # self.equations = [
        #     substitute_equations_ordered(eq, self.equations) for eq in self.equations
        # ]
        self.evaluated_equations = [
            substitute_equations_ordered(eq, self.evaluated_equations) for eq in self.evaluated_equations
        ]

    def _eliminate_useless_eqs(self):
        self.equations = [eq for eq in self.equations if not eq == True]
        self.evaluated_equations = [eq for eq in self.evaluated_equations if not eq == True]


def _pop_solved_equations_from_list(equations: EqList):
    extracted_equations = []
    solved_indices = []
    for i, eq in enumerate(equations):
        solution = solved_equation(eq)
        if solution is not None:
            extracted_equations.append(solution)
            solved_indices.append(i)

    # Now actually remove the solved equations, starting from the latest in the list to avoid changing the indices
    for ele in sorted(solved_indices, reverse=True):
        del equations[ele]

    return extracted_equations


