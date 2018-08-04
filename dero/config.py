import os
from functools import partial
from typing import List, Union

from .dropbox import filepath as dropbox_filepath

ListOfStrs = List[str]
StrOrListOfStrs = Union[ListOfStrs, str]

data_filepath = r'E:\Data'

def data_path(subpath: StrOrListOfStrs):
    return _os_join_list_or_str(data_filepath, subpath)

def data_path_func(subpath: StrOrListOfStrs):
    return path_func(subpath, data_path)

def dropbox_path(subpath: StrOrListOfStrs):
    return _os_join_list_or_str(dropbox_filepath, subpath)

def dropbox_path_func(subpath: StrOrListOfStrs):
    return path_func(subpath, dropbox_path)

def path_func(subpath: StrOrListOfStrs, path_func):
    new_path = path_func(subpath)
    new_path_func = partial(_os_join_list_or_str, new_path)
    return new_path_func

def _os_join_list_or_str(basepath: str, paths: StrOrListOfStrs) -> str:

    # If a list is passed, combine using operating system-specific path separator
    if isinstance(paths, list):
        paths = os.path.sep.join(paths)

    return os.path.join(basepath, paths)

#### Project paths

etf_project_path = dropbox_path_func(['UF', 'Andy', 'ETF Project'])
etf_path_func = lambda subpath: path_func(subpath, etf_project_path)