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

    yvar = 'y'
    xvars = ['x1', 'x2']
    all_xvars = ['const', 'x1', 'x2']
    groupvar = 'group'

class RegTest(DataFrameTest):

    def _reg_test(self, df, expect_params, expect_cov, **reg_kwargs):
        reg_result = dero.reg.reg(df, self.yvar, self.xvars, **reg_kwargs)

        assert_series_equal(expect_params, reg_result.params)
        assert_frame_equal(expect_cov, reg_result.cov_params())


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


