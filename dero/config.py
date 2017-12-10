import os

from .dropbox import filepath as dropbox_filepath

data_filepath = r'E:\Data'

def data_path(subpath):
    return os.path.join(data_filepath, subpath)

def dropbox_path(subpath):
    return os.path.join(dropbox_filepath, subpath)


#### Project paths

etf_project_path = dropbox_path('UF\Andy\ETF Project')
