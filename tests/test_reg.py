from context import dero


import pandas as pd
from pandas import Timestamp
from pandas.testing import assert_frame_equal, assert_series_equal
from numpy import nan, inf



class DataFrameTest:

    df = pd.DataFrame(
        data=[
            (1, 2, 3),
            (4, 5, nan),
            (10, 11, 100)
        ],
        columns=['y', 'x1', 'x2']
    )

    df_groups = pd.DataFrame(
        data=[
            (1, 2, 3, 'a'),
            (4, 5, nan, 'a'),
            (10, 11, 100, 'a'),
            (2, 4, 6, 'b'),
            (5, 10, nan, 'b'),
            (11, 15, 150, 'b'),
        ],
        columns=['y', 'x1', 'x2', 'group']
    )

    df_groups_no_nan = pd.DataFrame(
        data=[
            (1, 2, 3, 'a'),
            (4, 5, 8, 'a'),
            (10, 11, 100, 'a'),
            (2, 4, 6, 'b'),
            (5, 10, 20, 'b'),
            (11, 15, 150, 'b'),
        ],
        columns=['y', 'x1', 'x2', 'group']
    )

    df_groups_lag_reg = pd.DataFrame(
        data=[
            ('1/1/2000', 1, 2, 3, nan, nan, 'a'),
            ('1/2/2000', 4, 5, 8, 2, 3, 'a'),
            ('1/3/2000', 10, 11, 100, 5, 8, 'a'),
            ('1/4/2000', 15, 12, 40, 11, 100, 'a'),
            ('1/6/2000', 22, 18, 82, 12, 40, 'a'),
            ('1/7/2000', 46, 10, 61, 18, 82, 'a'),
            ('1/1/2000', 2, 4, 6, nan, nan, 'b'),
            ('1/2/2000', 5, 10, 20, 4, 6, 'b'),
            ('1/3/2000', 11, 15, 150, 10, 20, 'b'),
            ('1/4/2000', 13, 12, 156, 15, 150, 'b'),
            ('1/7/2000', 13, 12, 156, nan, nan, 'b'),

        ],
        columns=['Date', 'y', 'x1', 'x2', 'x1_lag_pregen', 'x2_lag_pregen', 'group']
    )
    df_groups_lag_reg['Date'] = pd.to_datetime(df_groups_lag_reg['Date'])

    yvar = 'y'
    xvars = ['x1', 'x2']
    all_xvars = ['const', 'x1', 'x2']
    groupvar = 'group'
    fe_xvars = all_xvars + ['b']

class RegTest(DataFrameTest):

    def _reg_test(self, df, expect_params, expect_cov, **reg_kwargs):
        reg_result = dero.reg.reg(df, self.yvar, self.xvars, **reg_kwargs)

        # Single result
        if (not 'fe' in reg_kwargs) or (not reg_kwargs['fe']):
            result = reg_result
        # Tuple of result, dummy_col_dict
        else:
            result = reg_result[0]


        assert_series_equal(expect_params, result.params)
        assert_frame_equal(expect_cov, result.cov_params())


#### Actual test cases below ####

class TestReg(RegTest):

    def test_reg_simple(self):

        expect_params = pd.Series(data = [
            0.17948580753899121,
            0.31490944113004432,
            0.063565103400305134,
            ], index=self.all_xvars)

        expect_cov = pd.DataFrame(data = [
                (inf, inf, -inf),
                (inf, inf, -inf),
                (-inf, -inf, inf),
                ], columns=self.all_xvars, index=self.all_xvars)

        self._reg_test(self.df, expect_params, expect_cov, robust=False, cluster=False)

    def test_reg_nocons(self):
        expect_params = pd.Series(data = [
            0.41916167664670689,
            0.053892215568862201,
            ], index=self.xvars)

        expect_cov = pd.DataFrame(data = [
            (inf, -inf),
            (-inf, inf),
            ], columns =self.xvars, index=self.xvars)

        self._reg_test(self.df, expect_params, expect_cov, robust=False, cluster=False, cons=False)

    def test_reg_cluster(self):
        expect_params = pd.Series(data=[
            -0.057782704189492023,
            0.56915450458771888,
            0.023236241968922107,
        ], index=self.all_xvars)

        expect_cov = pd.DataFrame(data=[
            (1.3825827000648401, -0.64860156573107908, 0.037973583240341238),
            (-0.64860156573067984, 0.30427401633831397, -0.017814287380373151),
            (0.03797358324036447, -0.017814287380394575, 0.0010429705391543902),
        ], columns=self.all_xvars, index=self.all_xvars)

        self._reg_test(self.df_groups, expect_params, expect_cov, robust=False, cluster=self.groupvar)

    def test_reg_fe(self):
        expect_params = pd.Series(data = [
            0.5140934,
            0.60590361,
            0.02298608,
            -1.71967829,
            ], index=self.fe_xvars)

        expect_cov = pd.DataFrame(data = [
            (0.86642167435809347, -0.15421903256428801, 0.0088046661162774695, 0.10782189494174726),
            (-0.15421903256428801, 0.043999645145278127, -0.0029669956299292195, -0.097047126884220028),
            (0.0088046661162774695, -0.0029669956299292195, 0.00024317047738642904, 0.0056102902997011801),
            (0.10782189494174726, -0.097047126884220028, 0.0056102902997011801, 0.76804342596454134),
        ], columns=self.fe_xvars, index=self.fe_xvars)

        self._reg_test(self.df_groups_no_nan, expect_params, expect_cov, robust=False, fe=self.groupvar)


class TestLagReg(DataFrameTest):

    def test_lag_reg(self):
        expected_result = dero.reg.reg(
            self.df_groups_lag_reg,
            'y',
            ['x1_lag_pregen', 'x2_lag_pregen']
        )

        lag_result = dero.reg.reg(
            self.df_groups_lag_reg,
            'y',
            ['x1', 'x2'],
            lag_variables=['x1', 'x2'],
            num_lags=1,
            lag_period_var='Date',
            lag_id_var='group'
        )

        assert (lag_result.params.values == expected_result.params.values).all()
        assert (lag_result.pvalues.values == expected_result.pvalues.values).all()