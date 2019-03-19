import pandas as pd
from dero.ml.typing import AllModelResultsDict


def train_and_score_model(model, x_train: pd.DataFrame, y_train: pd.Series, x_val: pd.DataFrame,
                          y_val: pd.Series) -> float:
    model.fit(x_train.values, y_train.values)
    return model.score(x_val.values, y_val.values)


def train_and_score_models(models, x_train: pd.DataFrame, y_train: pd.Series, x_val: pd.DataFrame,
                           y_val: pd.Series) -> AllModelResultsDict:
    out_dict = {}
    for model in models:
        score = train_and_score_model(
            model,
            x_train,
            y_train,
            x_val,
            y_val
        )
        model_dict = {
            'params': model.get_params(),
            'score': score
        }
        model_base_name = model.__class__.__name__
        if model_base_name in out_dict:
            out_dict[model_base_name].append(model_dict)
        else:
            out_dict[model_base_name] = [model_dict]
    return out_dict
