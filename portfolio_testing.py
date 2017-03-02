
import numpy as np
import pandas as pd
from functools import partial
from multiprocessing import Pool
import timeit
import time, datetime
import logging
import dero

estimate_time = dero.time.estimate_time





def portfolio(df, groupvar, ngroups=10, byvars=None, cutdf=None, portvar='portfolio',
              multiprocess=True):
    '''
    Constructs portfolios based on percentile values of groupvar. If ngroups=10, then will form 10 portfolios,
    with portfolio 1 having the bottom 10 percentile of groupvar, and portfolio 10 having the top 10 percentile
    of groupvar.
    
    df: pandas dataframe, input data
    groupvar: string, name of variable in df to form portfolios on
    ngroups: integer, number of portfolios to form
    byvars: string, list, or None, name of variable(s) in df, finds portfolios within byvars. For example if byvars='Month',
            would take each month and form portfolios based on the percentiles of the groupvar during only that month
    cutdf: pandas dataframe or None, optionally determine percentiles using another dataset. See second note.
    portvar: string, name of portfolio variable in the output dataset
    multiprocess: bool or int, set to True to use all available processors, 
                  set to False to use only one, pass an int less or equal to than number of 
                  processors to use that amount of processors 
    
    NOTE: Resets index and drops in output data, so don't use if index is important (input data not affected)
    NOTE: If using a cutdf, MUST have the same bygroups as df. The number of observations within each bygroup
          can be different, but there MUST be a one-to-one match of bygroups, or this will NOT work correctly.
          This may require some cleaning of the cutdf first.
    '''
    #Check types
    _check_portfolio_inputs(df, groupvar, ngroups=ngroups, byvars=byvars, cutdf=cutdf, portvar=portvar)
    byvars = _assert_byvars_list(byvars)
    if cutdf != None:
        assert isinstance(cutdf, pd.DataFrame)
    else: #this is where cutdf == None, the default case
        cutdf = df
        tempcutdf = cutdf.copy()
        
    pct_per_group = int(100/ngroups)
    percentiles = [i for i in range(0, 100 + pct_per_group, pct_per_group)] #percentile values, e.g. 0, 10, 20, 30... 100
    
    #Create new functions with common arguments added
    create_cutoffs_and_sort_into_ports = partial(_create_cutoffs_and_sort_into_ports, 
                                       groupvar=groupvar, portvar=portvar, percentiles=percentiles)
    split = partial(_split, keepvars=[groupvar], force_numeric=True)
    sort_arr_list_into_ports_and_return_series = partial(_sort_arr_list_into_ports_and_return_series,
                                                         percentiles=percentiles,
                                                         multiprocess=multiprocess)
    
    outdf = df.copy()
    
    #If there are no byvars, just complete portfolio sort
    if byvars == None: return create_cutoffs_and_sort_into_ports(outdf, cutdf)
    
    
    #else, deal with byvars
    #First create a key variable based on all the byvars
    tempdf = df.copy().reset_index(drop=True)
    for this_df in [tempdf, tempcutdf]:
        this_df['__key_var__'] = 'key' #container for key
        for col in [this_df[c].astype(str) for c in byvars]:
            this_df['__key_var__'] += col
    
    #Now split into list of arrays and process
    array_list = split(tempdf)
    cut_array_list = split(tempcutdf)
    
    ###########TEMP
    import pdb
    pdb.set_trace()
    
    
    outdf[portvar] = sort_arr_list_into_ports_and_return_series(array_list, cut_array_list)
    return outdf