import itertools
from dero.ml.typing import (
    AllModelOptionPossibilitiesDict,
    ModelOptionPossibilitiesDict,
    AllModelKwargsDict,
    AllModelKwargs
)


def get_kwarg_list_model_dict(models_option_possibilities: AllModelOptionPossibilitiesDict,
                              all_models_possibilities: ModelOptionPossibilitiesDict) -> AllModelKwargsDict:
    out_dict = {}
    for model_name, model_option_possibilities in models_option_possibilities.items():
        all_possibilities_for_model = model_option_possibilities.copy()
        all_possibilities_for_model.update(all_models_possibilities)
        kwarg_list = get_kwarg_list_for_model(all_possibilities_for_model)
        out_dict[model_name] = kwarg_list
    return out_dict


def get_kwarg_list_for_model(model_option_possibilities: ModelOptionPossibilitiesDict) -> AllModelKwargs:
    iter_list = []
    name_list = []
    for param_name, possible_values in model_option_possibilities.items():
        iter_list.append(possible_values)
        name_list.append(param_name)

    kwargs_list = []
    for option_set in itertools.product(*iter_list):
        kwargs = dict(list(zip(name_list, option_set)))
        kwargs_list.append(kwargs)

    return kwargs_list
