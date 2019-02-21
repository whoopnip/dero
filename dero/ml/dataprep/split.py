from typing import Optional, List, Tuple
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


def train_validation_test_split(df: pd.DataFrame, y_col: str, select_x_cols: Optional[List[str]] = None,
                                test_size: float = 0.2, validation_size: float = 0.2,
                                random_seed: Optional[int] = None
                                ) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    if select_x_cols is not None:
        df = df[select_x_cols + [y_col]]

    if random_seed is not None:
        kwargs = {'random_state': random_seed}
    else:
        kwargs = {}

    x_train, x_remain, y_train, y_remain = train_test_split(
        df.drop(y_col, axis=1),
        df[y_col],
        test_size=(validation_size + test_size),
        **kwargs
    )
    new_test_size = np.around(test_size / (validation_size + test_size), 2)
    # To preserve (new_test_size + new_val_size) = 1.0
    new_val_size = 1.0 - new_test_size

    x_val, x_test, y_val, y_test = train_test_split(x_remain, y_remain, test_size=new_test_size, **kwargs)

    return x_train, y_train, x_val, y_val, x_test, y_test
