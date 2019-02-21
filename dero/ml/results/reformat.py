from typing import Optional
import pandas as pd
from dero.ml.typing import ModelDict, AllModelResultsDict, DfDict


def model_dict_to_df(model_results: ModelDict, model_name: Optional[str] = None) -> pd.DataFrame:
    df = pd.DataFrame(model_results).T
    df.drop('score', inplace=True)
    df['score'] = model_results['score']
    if model_name is not None:
        df['model'] = model_name
        first_cols = ['model', 'score']
    else:
        first_cols = ['score']

    other_cols = [col for col in df.columns if col not in first_cols]

    return df[first_cols + other_cols]


def all_model_results_dict_to_df(results: AllModelResultsDict) -> pd.DataFrame:
    df = pd.DataFrame()
    for model_type, instance_list in results.items():
        for instance in instance_list:
            model_df = model_dict_to_df(instance, model_name=model_type)
            df = df.append(model_df)
    first_cols = ['model', 'score']
    other_cols = [col for col in df.columns if col not in first_cols]
    return df[first_cols + other_cols].sort_values('score', ascending=False)


def all_model_results_dict_to_model_df_dict(results: AllModelResultsDict) -> DfDict:
    out_dict = {}
    for model_type, instance_list in results.items():
        model_df = pd.DataFrame()
        for instance in instance_list:
            model_instance_df = model_dict_to_df(instance, model_name=model_type)
            model_df = model_df.append(model_instance_df)
        out_dict[model_type] = model_df.sort_values('score', ascending=False)
    return out_dict
