from dero.ml.typing import (
    AllModelOptionPossibilitiesDict,
    ModelOptionPossibilitiesDict
)
from dero.ml.gen_models.create import create_model_instances_from_model_class_list_and_kwargs_dict
from dero.ml.gen_models.kwargs import get_kwarg_list_model_dict


def get_model_instances_from_classes_and_options(model_classes,
                                                 models_option_possibilities: AllModelOptionPossibilitiesDict,
                                                 all_models_possibilities: ModelOptionPossibilitiesDict):
    """
    Creates model instances from every combination of options

    Args:
        model_classes: list of classes
        models_option_possibilities: e.g. {
                'SVC': {
                    'kernel': ['rbf', 'linear'],
                },
                'RandomForestClassifier': {
                    'n_estimators': [10, 20]
                }
            }
        all_models_possibilities: e.g. dict(
            class_weight=[None, 'balanced'],
            random_state=[1564564]
        )

    Returns: list of class instances

    """
    model_all_kwargs_dict = get_kwarg_list_model_dict(
        models_option_possibilities,
        all_models_possibilities,
    )

    instances = create_model_instances_from_model_class_list_and_kwargs_dict(
        model_classes,
        model_all_kwargs_dict
    )

    return instances

