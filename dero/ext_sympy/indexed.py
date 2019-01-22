import itertools
from typing import List, Tuple, Set, Dict, Any, Union
from sympy import Idx, Eq, Expr, Symbol
from sympy.tensor.index_methods import get_indices, IndexConformanceException
from dero.mixins.propertycache import SimplePropertyCacheMixin

IntTuple = Tuple[int]
IntOrIntTuple = Union[IntTuple, int]


class IndexedEquation(Eq, SimplePropertyCacheMixin):
    is_IndexedEquation = True

    def __getitem__(self, item: IntOrIntTuple):
        raise NotImplementedError('have partial implementation, but need to handle order of indices to get working.')
        if isinstance(item, int):
            # cast to tuple
            item = (item,)
        lhs_indices = get_all_indices(self.lhs)
        if len(item) != len(lhs_indices):
            raise ValueError(f'could not align desired indices {item} with lhs indices {lhs_indices}')
        sub_dict = {}
        # TODO: this is becoming out of order because indices are not ordered
        for i, idx in enumerate(lhs_indices):
            sub_dict[idx] = item[i]
        if not _sub_dict_is_valid_for_expr(sub_dict, self.lhs):
            raise ValueError(f'invalid sub dict {sub_dict} for expr {self.lhs}')

        evaled_lhs = self.lhs.subs(sub_dict)
        for eq in self.evaluated_index_eqs:
            if evaled_lhs in eq.lhs.free_symbols:
                return eq

        raise ValueError(f'could not find any evaluated index equations with lhs matching {evaled_lhs}')

    @property
    def evaluated_index_eqs(self):
        return self._try_getattr_else_call_func('_evaluated_index_eqs', self._generate_evaluated_index_eqs)

    @property
    def indices(self):
        return self._try_getattr_else_call_func('_indices', self._extract_indices)

    @property
    def index_symbols(self):
        return self._try_getattr_else_call_func('_index_symbols', self._extract_symbols_from_indices)

    def _extract_symbols_from_indices(self):
        self._index_symbols = _get_symbols_from_indices(self.indices)

    def _generate_evaluated_index_eqs(self):
        self._evaluated_index_eqs = equations_from_indexed_equation(self, self.index_symbols)

    def _extract_indices(self):
        self._indices = get_all_indices_for_eq(self)



def equations_from_indexed_equation(equation: Eq, indices: Tuple[Idx]) -> List[Eq]:
    """
    Generates a set of equations with evaluated indices from a single indexed equation

    Args:
        equation: must contain indices
        indices: indices which should be evaluated

    Returns:
        evaluated equations

    Examples:
        >>> from sympy import symbols, Idx, IndexedBase, Eq
        >>> N = 2
        >>> T = 2
        >>> i = Idx('i', range=(1, N))
        >>> t = Idx('t', range=(0, T))

        >>> price = IndexedBase('P', shape=(N, T + 1))
        >>> ret = IndexedBase('r', shape=(N, T))

        >>> p_eq = Eq(price[i, t], price[i, t - 1] * ret[i, t])

        >>> equations_from_indexed_equation(p_eq, (i, t))

        P_{1,1} = P_{1,0} r_{1,1}
        P_{1,2} = P_{1,1} r_{1,2}
        P_{2,1} = P_{2,0} r_{2,1}
        P_{2,2} = P_{2,1} r_{2,2}

    """
    if not _all_bounds_are_numeric(indices):
        # Not possible to create equations when bounds are symbolic
        return equation

    index_element_tuples = map(_elements_from_index, indices)
    substitution_tuples = itertools.product(*index_element_tuples)

    output_eqs = []
    for sub_tup in substitution_tuples:
        sub_dict = {index: sub_tup[i] for i, index in enumerate(indices)}
        if _sub_dict_is_valid_for_equation(sub_dict, equation):
            evaled_eq = equation.subs(sub_dict)
            output_eqs.append(evaled_eq)

    return output_eqs


def _all_bounds_are_numeric(indexes: Tuple[Idx]) -> bool:
    return all(map(_bounds_are_numeric, indexes))


def _bounds_are_numeric(index: Idx) -> bool:
    if (not index.lower.is_symbol) and (not index.upper.is_symbol):
        return True

    return False


def _elements_from_index(index: Idx) -> Tuple:
    return tuple([i for i in range(index.lower, index.upper + 1)])


def get_all_indices(expr: Expr) -> Set[Idx]:
    all_indices = set()
    # First try to get indices for entire expr
    try:
        indices = _get_all_indices(expr)
        all_indices.update(indices)
    except IndexConformanceException:
        pass

    # Now get indices for each term of expr
    for term in expr.args:
        # Recursively call get indices on each sub term
        indices = get_all_indices(term)
        all_indices.update(indices)
    return all_indices


def get_all_indices_for_eq(equation: Eq) -> Set[Idx]:
    indices = get_all_indices(equation.lhs)
    indices.update(get_all_indices(equation.rhs))
    return indices


def _get_all_indices(expr: Expr) -> Set[Idx]:
    indices, empty_dict = get_indices(expr)
    return indices


def _get_symbols_from_indices(idx_set: Set[Idx]) -> Set[Symbol]:
    all_symbols = set()
    for idx in idx_set:
        all_symbols.update(idx.free_symbols)
    return all_symbols


def _is_in_indices(sym: Symbol, idx_set: Set[Idx]) -> bool:
    symbols = _get_symbols_from_indices(idx_set)
    return sym in symbols


def _sub_dict_is_valid_for_indices(sub_dict: Dict[Idx, Any], indices: Set[Idx]) -> bool:
    for idx in indices:
        for sub_idx, sub_val in sub_dict.items():
            if _is_in_indices(sub_idx, {idx}):
                symbols = idx.free_symbols
                result = idx.subs(sub_dict)
                for symbol in symbols:
                    if hasattr(symbol, 'lower') and result < symbol.lower:
                        return False
                    if hasattr(symbol, 'upper') and result > symbol.upper:
                        return False
    return True


def _sub_dict_is_valid_for_equation(sub_dict: Dict[Idx, Any], equation: Eq) -> bool:
    indices = get_all_indices_for_eq(equation)

    return _sub_dict_is_valid_for_indices(sub_dict, indices)

def _sub_dict_is_valid_for_expr(sub_dict: Dict[Idx, Any], expr: Expr) -> bool:
    indices = get_all_indices(expr)

    return _sub_dict_is_valid_for_indices(sub_dict, indices)
