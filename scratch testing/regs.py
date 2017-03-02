
import itertools
import statsmodels.api as sm
from statsmodels.iolib.summary2 import summary_col

import timeit, sys
import dero
from functools import partial

estimate_time = dero.time.estimate_time
parallel_loop_with_timeout = dero.multiprocessing.parallel_loop_with_timeout

def reg(df, xvars, yvar, robust=True, cluster=False):
    """
    Returns a fitted regression. Takes df, produces a regression df with no missing among needed
    variables, and fits a regression model. If robust is specified, uses heteroskedasticity-
    robust standard errors. If cluster is specified, calculated clustered standard errors
    by the given variable. 
    
    Note: only specify at most one of robust and cluster.
    
    Required inputs:
    df: pandas dataframe containing regression data
    xvars: list of strs, column names of x variables for regression
    yvar: str, column name of outcome y variable
    
    Optional inputs:
    robust: bool, set to True to use heterskedasticity-robust standard errors
    cluster: False or str, set to a column name to calculate standard errors within clusters
             given by unique values of given column name
    """
    regdf = df.dropna(subset=[yvar] + xvars)
    y = regdf[yvar]
    X = regdf.loc[:, xvars]
    X = sm.add_constant(X)

    mod = sm.OLS(y, X)
    
    assert not (robust and cluster) #need to pick one of robust or cluster
    
    if robust:
        return mod.fit(cov_type='HC1')
    
    if cluster:
        groups = regdf[cluster].unique().tolist()
        group_ints = regdf[cluster].apply(lambda x: groups.index(x))
        return mod.fit(cov_type='cluster', cov_kwds={'groups': group_ints})
    
    return mod.fit()


def reg_for_each_combo(df, xvars, yvar, **reg_kwargs):
    """
    Takes each possible combination of xvars (starting from each var individually, then each pair
    of vars, etc. all the way up to all xvars), and regresses yvar on each set of xvars. Returns
    a list of fitted regressions.
    """   
    #Get the entire list of combinations of xvars to run regressions with
    combo_list = []
    for i in range(1, len(xvars) + 1):
        for combo in itertools.combinations(xvars, i):
            combo_list.append(list(combo))
            
    df_reg = partial(reg, df, yvar=yvar, **reg_kwargs)
    
    results = parallel_loop_with_timeout(df_reg, combo_list, timeout=2)
    return [res[1] for res in results if res[1] != 'timeout'] #strip results from result tuples
            
#     reg_list = []
#     num_regs = len(combo_list)
#     start_time = timeit.default_timer()
#     for i, x in enumerate(combo_list):
#         reg_list.append(reg(df, x, yvar=yvar, **reg_kwargs))
#         estimate_time(num_regs, i, start_time)
        
#         ####TEMPPPPPP
#         print(i)
#         ######################
        
        
#         sys.stdout.flush()

    
#     reg_list = []
#     for i in range(1, len(xvars) + 1):
#         for combo in itertools.combinations(xvars, i):
#             x = list(combo)
#             reg_list.append(reg(df, x, yvar=yvar, **reg_kwargs))
            
#     return reg_list

def select_models(reg_list, keepnum, xvars):
    """
    Takes a list of fitted regression models and selects among them based on adjusted R-Squared. For each
    number of variables involved in the regressions, keepnum with the highest R-squareds will be kept.
    
    For example, if reg_list contains 3 regressions with two variables and 6 regressions with three variables,
    and keepnum is 2, will return a list of four regressions, 2 with two variables and 2 with three variables.
    """
    outlist = []
    for i in range(1, len(xvars) + 1):
        reg_list_match = [reg for reg in reg_list if reg.df_model == i] #select models with this many variables
        try:
            r2_min = sorted([reg.rsquared_adj for reg in reg_list_match])[-keepnum] #gets keepnumth highest r2
        except IndexError: #should happen once there are less models run than keepnum (i.e. with all xvars)
            r2_min = sorted([reg.rsquared_adj for reg in reg_list_match])[0] #gets lowest r2 (keep all)
        outlist += [reg for reg in reg_list_match if reg.rsquared_adj >= r2_min]
    return outlist

def produce_summary(reg_list, stderr=False):

    summ =  summary_col(reg_list, stars=True, float_format='%0.1f',
            info_dict={'N':lambda x: "{0:d}".format(int(x.nobs)),
                      'R2':lambda x: "{:.2f}".format(x.rsquared),
                      'Adj-R2':lambda x: "{:.2f}".format(x.rsquared_adj)})
    
    if not stderr:
        summ.tables[0].drop('', axis=0, inplace=True) #drops the rows containing standard errors
        
    return summ

def reg_for_each_combo_select_and_produce_summary(df, xvars, yvar, robust=True, cluster=False,
                                                  keepnum=5, stderr=False):
    """
    Convenience function to run regressions for every combination of xvars, select the best models,
    and present them in a summary format. Returns a tuple of (reg_list, summary) where reg_list
    is a list of fitted regression models, and summary is a single dataframe of results
    
    Required inputs:
    df: pandas dataframe containing regression data
    xvars: list of strs, column names of all possible x variables
    yvar: str, column name of y variable
    
    Optional inputs:
    robust: bool, set to True to use heterskedasticity-robust standard errors
    cluster: False or str, set to a column name to calculate standard errors within clusters
             given by unique values of given column name
    keepnum: int, number to keep for each amount of x variables. The total number of outputted
             regressions will be roughly keepnum * len(xvars)
    stderr: bool, set to True to keep rows for standard errors below coefficient estimates
    
    Note: only specify at most one of robust and cluster.
    
    """
    reg_list = reg_for_each_combo(df, xvars, yvar, robust=robust, cluster=cluster)
    outlist = select_models(reg_list, keepnum, xvars)
    summ = produce_summary(outlist, stderr=stderr) 
    return outlist, summ


