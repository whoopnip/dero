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

    yvar = 'y'
    xvars = ['x1', 'x2']
    all_xvars = ['const', 'x1', 'x2']
    groupvar = 'group'
    fe_xvars = all_xvars + ['a', 'b']

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
            -0.23049716725241853,
            0.60590360637890839,
            0.022986080158407668,
            0.74459056311787641,
            -0.97508773037029473,
            ], index=self.fe_xvars)

        expect_cov = pd.DataFrame(data = [
            (0.51833530035154651, -0.13516173067093232, 0.0077398741774187142, 0.095219780867766016, 0.42311551948378062),
            (-0.13516173067093232, 0.043999645145278161, -0.0029669956299292191, -0.019057301893355846, -0.11610442877757651),
            (0.0077398741774187142, -0.0029669956299292191, 0.00024317047738642891, 0.0010647919388587532, 0.0066750822385599623),
            (0.095219780867766016, -0.019057301893355846, 0.0010647919388587532, 0.15764681227101526, -0.06242703140324924),
            (0.42311551948378062, -0.11610442877757651, 0.0066750822385599623, -0.06242703140324924, 0.48554255088702991),
            ], columns=self.fe_xvars, index=self.fe_xvars)

        self._reg_test(self.df_groups_no_nan, expect_params, expect_cov, robust=False, fe=self.groupvar)


