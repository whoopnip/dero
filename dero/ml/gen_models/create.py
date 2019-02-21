from dero.ml.typing import AllModelKwargsDict


def create_model_instances_from_model_class_list_and_kwargs_dict(model_classes,
                                                                 model_all_kwargs_dict: AllModelKwargsDict) -> list:

    models = []
    for model_class in model_classes:
        model_kwargs_list = model_all_kwargs_dict.get(model_class.__name__, [{}])
        for model_kwargs in model_kwargs_list:
            models.append(
                model_class(**model_kwargs)
            )
    return models
