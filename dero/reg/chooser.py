from .reg import reg
from .differenced import diff_reg


def any_reg(reg_type, *reg_args, **reg_kwargs):

    reg_type = reg_type.lower()

    if reg_type in ('diff', 'difference', 'diff_reg', 'diff reg', 'difference reg', 'difference regression'):
        temp_kwargs = reg_kwargs.copy()
        if 'diff_cols' in temp_kwargs:
            diff_cols = temp_kwargs.pop('diff_cols')
        else:
            diff_cols = None
        id_col = temp_kwargs.pop('id_col')
        date_col = temp_kwargs.pop('date_col')
        return diff_reg(*reg_args, id_col, date_col, diff_cols=diff_cols, **temp_kwargs)

    if reg_type in ('reg', 'normal', 'ols') or reg_type == None:
        return reg(*reg_args, **reg_kwargs)

    raise ValueError(f'Must pass valid reg type. Got {reg_type}')
