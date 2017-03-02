
from context import dero

import pandas as pd
from pandas.util.testing import assert_frame_equal
from pandas import Timestamp
from numpy import nan

class DataFrameTest:
    
    df = pd.DataFrame([
                                (10516, 'a', '1/1/2000', 1.01),
                                (10516, 'a', '1/2/2000', 1.02),
                                (10516, 'a', '1/3/2000', 1.03),
                                (10516, 'a', '1/4/2000', 1.04),
                                (10516, 'b', '1/1/2000', 1.05),
                                (10516, 'b', '1/2/2000', 1.06),
                                (10516, 'b', '1/3/2000', 1.07),
                                (10516, 'b', '1/4/2000', 1.08),
                                (10517, 'a', '1/1/2000', 1.09),
                                (10517, 'a', '1/2/2000', 1.10),
                                (10517, 'a', '1/3/2000', 1.11),
                                (10517, 'a', '1/4/2000', 1.12),
                               ], columns = ['PERMNO','byvar','Date', 'RET'])   
    
    df_duplicate_row = pd.DataFrame([
                                (10516, 'a', '1/1/2000', 1.01),
                                (10516, 'a', '1/2/2000', 1.02),
                                (10516, 'a', '1/3/2000', 1.03),
                                (10516, 'a', '1/3/2000', 1.03), #this is a duplicated row
                                (10516, 'a', '1/4/2000', 1.04),
                                (10516, 'b', '1/1/2000', 1.05),
                                (10516, 'b', '1/2/2000', 1.06),
                                (10516, 'b', '1/3/2000', 1.07),
                                (10516, 'b', '1/4/2000', 1.08),
                                (10517, 'a', '1/1/2000', 1.09),
                                (10517, 'a', '1/2/2000', 1.10),
                                (10517, 'a', '1/3/2000', 1.11),
                                (10517, 'a', '1/4/2000', 1.12),
                               ], columns = ['PERMNO','byvar','Date', 'RET'])  
    
    df_weight = pd.DataFrame(data = [
                                (10516, 'a', '1/1/2000', 1.01, 0),
                                (10516, 'a', '1/2/2000', 1.02, 1),
                                (10516, 'a', '1/3/2000', 1.03, 1),
                                (10516, 'a', '1/4/2000', 1.04, 0),
                                (10516, 'b', '1/1/2000', 1.05, 1),
                                (10516, 'b', '1/2/2000', 1.06, 1),
                                (10516, 'b', '1/3/2000', 1.07, 1),
                                (10516, 'b', '1/4/2000', 1.08, 1),
                                (10517, 'a', '1/1/2000', 1.09, 0),
                                (10517, 'a', '1/2/2000', 1.1, 0),
                                (10517, 'a', '1/3/2000', 1.11, 0),
                                (10517, 'a', '1/4/2000', 1.12, 1),
                                ], columns = ['PERMNO', 'byvar', 'Date', 'RET', 'weight'])
    
    df_nan_byvar = pd.DataFrame(data = [
                                ('a', 1),
                                (nan, 2),
                                ('b', 3),
                                ('b', 4),
                                ], columns = ['byvar', 'val'])
    
    df_nan_byvar_and_val = pd.DataFrame(data = [
                                ('a', 1),
                                (nan, 2),
                                ('b', nan),
                                ('b', 4),
                                ], columns = ['byvar', 'val'])

    
    df_datetime = df.copy()
    df_datetime['Date'] = pd.to_datetime(df_datetime['Date'])
    
    df_datetime_no_ret = df_datetime.copy()
    df_datetime_no_ret.drop('RET', axis=1, inplace=True)

class TestCumulate(DataFrameTest):
    
    
    expect_between_1_3 = pd.DataFrame([
                                (10516, 'a', '1/1/2000', 1.01, 1.01),
                                (10516, 'a', '1/2/2000', 1.02, 1.02),
                                (10516, 'a', '1/3/2000', 1.03, 1.03),
                                (10516, 'a', '1/4/2000', 1.04, 1.0712),
                                (10516, 'b', '1/1/2000', 1.05, 1.05),
                                (10516, 'b', '1/2/2000', 1.06, 1.06),
                                (10516, 'b', '1/3/2000', 1.07, 1.07),
                                (10516, 'b', '1/4/2000', 1.08, 1.1556),
                                (10517, 'a', '1/1/2000', 1.09, 1.09),
                                (10517, 'a', '1/2/2000', 1.10, 1.10),
                                (10517, 'a', '1/3/2000', 1.11, 1.11),
                                (10517, 'a', '1/4/2000', 1.12, 1.2432),
                                ], columns = ['PERMNO','byvar','Date', 'RET', 'cum_RET'])
    
    expect_first = pd.DataFrame([
                                (10516, 'a', '1/1/2000', 1.01, 1.01),
                                (10516, 'a', '1/2/2000', 1.02, 1.02),
                                (10516, 'a', '1/3/2000', 1.03, 1.0506),
                                (10516, 'a', '1/4/2000', 1.04, 1.092624),
                                (10516, 'b', '1/1/2000', 1.05, 1.05),
                                (10516, 'b', '1/2/2000', 1.06, 1.06),
                                (10516, 'b', '1/3/2000', 1.07, 1.1342),
                                (10516, 'b', '1/4/2000', 1.08, 1.224936),
                                (10517, 'a', '1/1/2000', 1.09, 1.09),
                                (10517, 'a', '1/2/2000', 1.10, 1.10),
                                (10517, 'a', '1/3/2000', 1.11, 1.221),
                                (10517, 'a', '1/4/2000', 1.12, 1.36752),
                                ], columns = ['PERMNO','byvar','Date', 'RET', 'cum_RET'])
        
    def test_method_between(self):
        cum_df = dero.pandas.cumulate(self.df, 'RET', 'between', periodvar='Date', 
                                      byvars=['PERMNO','byvar'], time=[1,3])
        
        assert_frame_equal(self.expect_between_1_3, cum_df, check_dtype=False)
        
    def test_method_first(self):
        cum_df = dero.pandas.cumulate(self.df, 'RET', 'first', periodvar='Date', 
                                      byvars=['PERMNO','byvar'])
        
        assert_frame_equal(self.expect_first, cum_df, check_dtype=False)
        
    def test_grossify(self):
        df = self.df.copy() #don't overwrite original
        df['RET'] -= 1 #ungrossify
        expect_first_grossify = self.expect_first.copy()
        expect_first_grossify['cum_RET'] -= 1
        expect_first_grossify['RET'] -= 1
        cum_df = dero.pandas.cumulate(df, 'RET', 'first', periodvar='Date', 
                                      byvars=['PERMNO','byvar'], grossify=True)
    
        assert_frame_equal(expect_first_grossify, cum_df, check_dtype=False)

class TestGroupbyMerge(DataFrameTest):

    
    def test_subset(self):
        byvars = ['PERMNO','byvar']
        out = dero.pandas.groupby_merge(self.df, byvars, 'max', subset='RET')
        expect_df = pd.DataFrame(
                                [(10516, 'a', '1/1/2000', 1.01, 1.04),
                                 (10516, 'a', '1/2/2000', 1.02, 1.04),
                                 (10516, 'a', '1/3/2000', 1.03, 1.04),
                                 (10516, 'a', '1/4/2000', 1.04, 1.04),
                                 (10516, 'b', '1/1/2000', 1.05, 1.08),
                                 (10516, 'b', '1/2/2000', 1.06, 1.08),
                                 (10516, 'b', '1/3/2000', 1.07, 1.08),
                                 (10516, 'b', '1/4/2000', 1.08, 1.08),
                                 (10517, 'a', '1/1/2000', 1.09, 1.12),
                                 (10517, 'a', '1/2/2000', 1.10, 1.12),
                                 (10517, 'a', '1/3/2000', 1.11, 1.12),
                                 (10517, 'a', '1/4/2000', 1.12, 1.12)],
         columns = ['PERMNO','byvar','Date', 'RET', 'RET_max'])
        
        assert_frame_equal(expect_df, out)
        
    def test_nan_byvar_transform(self):
        expect_df = self.df_nan_byvar.copy()
        expect_df['val_transform'] = expect_df['val']
        
        out = dero.pandas.groupby_merge(self.df_nan_byvar, 'byvar', 'transform', (lambda x: x))
        
        assert_frame_equal(expect_df, out)
        
    def test_nan_byvar_and_nan_val_transform_numeric(self):
        non_standard_index = self.df_nan_byvar_and_val.copy()
        non_standard_index.index = [5,6,7,8]
        
        expect_df = self.df_nan_byvar_and_val.copy()
        expect_df['val_transform'] = expect_df['val'] + 1
        expect_df.index = [5,6,7,8]
        
        out = dero.pandas.groupby_merge(non_standard_index, 'byvar', 'transform', (lambda x: x + 1))
        
        assert_frame_equal(expect_df, out)
        
    def test_nan_byvar_and_nan_val_and_nonstandard_index_transform_numeric(self):
        expect_df = self.df_nan_byvar_and_val.copy()
        expect_df['val_transform'] = expect_df['val'] + 1
        
    def test_nan_byvar_sum(self):
        expect_df = pd.DataFrame(data = [
                        ('a', 1, 1.0),
                        (nan, 2, nan),
                        ('b', 3, 7.0),
                        ('b', 4, 7.0),
                        ], columns = ['byvar', 'val', 'val_sum'])
        
        out = dero.pandas.groupby_merge(self.df_nan_byvar, 'byvar', 'sum')
        
        assert_frame_equal(expect_df, out)
        
        
class TestLongToWide:
    
    expect_df_with_colindex = pd.DataFrame(data = [
                                (10516, 'a', 1.01, 1.02, 1.03, 1.04),
                                (10516, 'b', 1.05, 1.06, 1.07, 1.08),
                                (10517, 'a', 1.09, 1.1, 1.11, 1.12),
                                ], columns = ['PERMNO', 'byvar', 
                                              'RET1/1/2000', 'RET1/2/2000', 
                                              'RET1/3/2000', 'RET1/4/2000'])
    
    expect_df_no_colindex = pd.DataFrame(data = [
                            (10516, 'a', '1/1/2000', 1.01, 1.02, 1.03, 1.04),
                            (10516, 'a', '1/2/2000', 1.01, 1.02, 1.03, 1.04),
                            (10516, 'a', '1/3/2000', 1.01, 1.02, 1.03, 1.04),
                            (10516, 'a', '1/4/2000', 1.01, 1.02, 1.03, 1.04),
                            (10516, 'b', '1/1/2000', 1.05, 1.06, 1.07, 1.08),
                            (10516, 'b', '1/2/2000', 1.05, 1.06, 1.07, 1.08),
                            (10516, 'b', '1/3/2000', 1.05, 1.06, 1.07, 1.08),
                            (10516, 'b', '1/4/2000', 1.05, 1.06, 1.07, 1.08),
                            (10517, 'a', '1/1/2000', 1.09, 1.1, 1.11, 1.12),
                            (10517, 'a', '1/2/2000', 1.09, 1.1, 1.11, 1.12),
                            (10517, 'a', '1/3/2000', 1.09, 1.1, 1.11, 1.12),
                            (10517, 'a', '1/4/2000', 1.09, 1.1, 1.11, 1.12),
                            ], columns = ['PERMNO', 'byvar', 'Date', 'RET0', 
                                          'RET1', 'RET2', 'RET3'])
    input_data = DataFrameTest()

    ltw_no_dup_colindex    = dero.pandas.long_to_wide(input_data.df,
                                                     ['PERMNO', 'byvar'], 'RET', colindex='Date')
    ltw_dup_colindex       = dero.pandas.long_to_wide(input_data.df_duplicate_row,
                                                     ['PERMNO', 'byvar'], 'RET', colindex='Date')
    ltw_no_dup_no_colindex = dero.pandas.long_to_wide(input_data.df,
                                                     ['PERMNO', 'byvar'], 'RET')
    ltw_dup_no_colindex    = dero.pandas.long_to_wide(input_data.df_duplicate_row,
                                                     ['PERMNO', 'byvar'], 'RET')
    df_list = [ltw_no_dup_colindex, ltw_dup_colindex, 
               ltw_no_dup_no_colindex, ltw_dup_no_colindex]

    def test_no_duplicates_with_colindex(self):
        assert_frame_equal(self.expect_df_with_colindex, self.ltw_no_dup_colindex)
        
    def test_duplicates_with_colindex(self):
        assert_frame_equal(self.expect_df_with_colindex, self.ltw_dup_colindex)
        
    def test_no_duplicates_no_colindex(self):        
        assert_frame_equal(self.expect_df_no_colindex, self.ltw_no_dup_no_colindex)
        
    def test_duplicates_no_colindex(self):        
        assert_frame_equal(self.expect_df_no_colindex, self.ltw_dup_no_colindex)
        
    def test_no_extra_vars(self):
        for df in self.df_list:
            assert ('__idx__','__key__') not in df.columns
            

class TestPortfolioAverages:
    
    input_data = DataFrameTest()
    
    expect_avgs_no_wt = pd.DataFrame(data = [
                    (1, 'a', 1.0250000000000001),
                    (1, 'b', 1.0550000000000002),
                    (2, 'a', 1.1050000000000002),
                    (2, 'b', 1.0750000000000002),
                    ], columns = ['portfolio', 'byvar', 'RET'])
    
    expect_avgs_wt = pd.DataFrame(data = [
                    (1, 'a', 1.0250000000000001, 1.025),
                    (1, 'b', 1.0550000000000002, 1.0550000000000002),
                    (2, 'a', 1.1050000000000002, 1.12),
                    (2, 'b', 1.0750000000000002, 1.0750000000000002),
                    ], columns = ['portfolio', 'byvar', 'RET', 'RET_wavg'])
    
    expect_ports = pd.DataFrame(data = [
                    (10516, 'a', '1/1/2000', 1.01, 0, 1),
                    (10516, 'a', '1/2/2000', 1.02, 1, 1),
                    (10516, 'a', '1/3/2000', 1.03, 1, 1),
                    (10516, 'a', '1/4/2000', 1.04, 0, 1),
                    (10516, 'b', '1/1/2000', 1.05, 1, 1),
                    (10516, 'b', '1/2/2000', 1.06, 1, 1),
                    (10516, 'b', '1/3/2000', 1.07, 1, 2),
                    (10516, 'b', '1/4/2000', 1.08, 1, 2),
                    (10517, 'a', '1/1/2000', 1.09, 0, 2),
                    (10517, 'a', '1/2/2000', 1.1, 0, 2),
                    (10517, 'a', '1/3/2000', 1.11, 0, 2),
                    (10517, 'a', '1/4/2000', 1.12, 1, 2),
                    ], columns = ['PERMNO', 'byvar', 'Date', 'RET', 'weight', 'portfolio'])
    
    avgs, ports = dero.pandas.portfolio_averages(input_data.df_weight, 'RET', 'RET', ngroups=2,
                                                  byvars='byvar')
    
    w_avgs, w_ports = dero.pandas.portfolio_averages(input_data.df_weight, 'RET', 'RET', ngroups=2,
                                                  byvars='byvar', wtvar='weight')
    
    def test_simple_averages(self):
        assert_frame_equal(self.expect_avgs_no_wt, self.avgs)
    
    def test_weighted_averages(self):
        assert_frame_equal(self.expect_avgs_wt, self.w_avgs)
        
    def test_portfolio_construction(self):
        assert_frame_equal(self.expect_ports, self.ports)
        assert_frame_equal(self.expect_ports, self.w_ports)

class TestWinsorize(DataFrameTest):
    
    def test_winsor_40_subset_byvars(self):
        
        expect_df = pd.DataFrame(data = [
            (10516, 'a', '1/1/2000', 1.0216),
            (10516, 'a', '1/2/2000', 1.0216),
            (10516, 'a', '1/3/2000', 1.028),
            (10516, 'a', '1/4/2000', 1.028),
            (10516, 'b', '1/1/2000', 1.0616),
            (10516, 'b', '1/2/2000', 1.0616),
            (10516, 'b', '1/3/2000', 1.068),
            (10516, 'b', '1/4/2000', 1.068),
            (10517, 'a', '1/1/2000', 1.1016000000000001),
            (10517, 'a', '1/2/2000', 1.1016000000000001),
            (10517, 'a', '1/3/2000', 1.108),
            (10517, 'a', '1/4/2000', 1.108),
            ], columns = ['PERMNO', 'byvar', 'Date', 'RET'])
        
        wins = dero.pandas.winsorize(self.df, .4, subset='RET', byvars=['PERMNO','byvar'])
        
        assert_frame_equal(expect_df, wins)
    
class TestRegBy(DataFrameTest):
    
    indf = self.df_weight.copy()
    indf['key'] = indf['PERMNO'].astype(str) + '_' + indf['byvar']
    
    def test_regby_nocons(self):
        
        expect_df = pd.DataFrame(data = [
            (0.48774684748988806, '10516_a'),
            (0.9388636664168903, '10516_b'),
            (0.22929206076239614, '10517_a'),
            ], columns = ['coef_RET', 'key'])
        
        rb = dero.pandas.reg_by(self.indf, 'weight', 'RET', 'key', cons=False)
        
        print('Reg by: ', rb)
        
        assert_frame_equal(expect_df, rb)