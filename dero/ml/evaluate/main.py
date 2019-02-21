from typing import Optional, Tuple, List
import pandas as pd
from dero.ml.typing import DfDict
from dero.ml.evaluate.train_score import train_and_score_models
from dero.ml.dataprep.split import train_validation_test_split
from dero.ml.results.reformat import all_model_results_dict_to_df, all_model_results_dict_to_model_df_dict


def split_data_train_and_score_models(df: pd.DataFrame, y_col: str, models,
                                      select_x_cols: Optional[List[str]] = None,
                                      test_size: float = 0.2, validation_size: float = 0.2,
                                      random_seed: Optional[int] = None) -> Tuple[pd.DataFrame, DfDict]:
    x_train, y_train, x_val, y_val, x_test, y_test = train_validation_test_split(
        df,
        y_col,
        select_x_cols=select_x_cols,
        test_size=test_size,
        validation_size=validation_size,
        random_seed=random_seed
    )

    results = train_and_score_models(
        models,
        x_train,
        y_train,
        x_val,
        y_val,
    )

    results_df_dict = all_model_results_dict_to_model_df_dict(results)
    all_model_results_df = all_model_results_dict_to_df(results)

    return all_model_results_df, results_df_dict