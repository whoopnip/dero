import numpy as np
import pandas as pd
from linearmodels.panel.model import (
    PooledOLS,
    lstsq,
    PanelResults,
    FamaMacBethCovariance,
    FamaMacBethKernelCovariance,
    PanelFormulaParser,
    matrix_rank
)

class FamaMacBeth(PooledOLS):
    r"""
    Pooled coefficient estimator for panel data

    Parameters
    ----------
    dependent : array-like
        Dependent (left-hand-side) variable (time by entity)
    exog : array-like
        Exogenous or right-hand-side variables (variable by time by entity).
    weights : array-like, optional
        Weights to use in estimation.  Assumes residual variance is
        proportional to inverse of weight to that the residual time
        the weight should be homoskedastic.

    Notes
    -----
    The model is given by

    .. math::

        y_{it}=\beta^{\prime}x_{it}+\epsilon_{it}

    The Fama-MacBeth estimator is computed by performing T regressions, one
    for each time period using all available entity observations.  Denote the
    estimate of the model parameters as :math:`\hat{\beta}_t`.  The reported
    estimator is then

    .. math::

        \hat{\beta} = T^{-1}\sum_{t=1}^T \hat{\beta}_t

    While the model does not explicitly include time-effects, the
    implementation based on regressing all observation in a single
    time period is "as-if" time effects are included.

    Parameter inference is made using the set T parameter estimates using
    either the standard covariance estimator or a kernel-based covariance,
    depending on ``cov_type``.
    """

    def __init__(self, dependent, exog, *, weights=None):
        super(FamaMacBeth, self).__init__(dependent, exog, weights=weights)

    def fit(self, cov_type='unadjusted', debiased=True, **cov_config):
        """
        Estimate model parameters

        Parameters
        ----------
        cov_type : str, optional
            Name of covariance estimator. See Notes.
        debiased : bool, optional
            Flag indicating whether to debiased the covariance estimator using
            a degree of freedom adjustment.
        **cov_config
            Additional covariance-specific options.  See Notes.

        Returns
        -------
        results :  PanelResults
            Estimation results

        Examples
        --------
        >>> from linearmodels import FamaMacBeth
        >>> mod = FamaMacBeth(y, x)
        >>> res = mod.fit(cov_type='kernel', kernel='Parzen')

        Notes
        -----
        Four covariance estimators are supported:

        * 'unadjusted', 'homoskedastic', 'robust', 'heteroskedastic' - Use the
          standard covariance estimator of the T parameter estimates.
        * 'kernel' - HAC estimator. Configurations options are:

          * ``kernel`` - One of the supported kernels (bartlett, parzen, qs).
            Default is Bartlett's kernel, which is implements the the
            Newey-West covariance estimator.
          * ``bandwidth`` - Bandwidth to use when computing the kernel.  If
            not provided, a naive default is used.
        """
        y = self._y
        x = self._x
        root_w = np.sqrt(self._w)
        wy = root_w * y
        wx = root_w * x

        dep = self.dependent.dataframe
        exog = self.exog.dataframe
        index = self.dependent.index
        wy = pd.DataFrame(wy[self._not_null], index=index, columns=dep.columns)
        wx = pd.DataFrame(wx[self._not_null], index=exog.notnull().index, columns=exog.columns)

        yx = pd.DataFrame(np.c_[wy.values, wx.values], columns=list(wy.columns) + list(wx.columns),
                          index=wy.index)

        def single(z: pd.DataFrame):
            exog = z.iloc[:, 1:].values
            if exog.shape[0] < exog.shape[1]:
                return pd.Series([np.nan] * len(z.columns), index=z.columns)
            dep = z.iloc[:, :1].values
            params = lstsq(exog, dep)[0]
            return pd.Series(np.r_[np.nan, params.ravel()], index=z.columns)

        all_params = yx.groupby(level=1).apply(single)
        all_params = all_params.iloc[:, 1:]
        params = all_params.mean(0).values[:, None]
        all_params = all_params.values

        wy = wy.values
        wx = wx.values
        index = self.dependent.index
        fitted = pd.DataFrame(self.exog.values2d @ params, index, ['fitted_values'])
        effects = pd.DataFrame(np.full_like(fitted.values, np.nan), index, ['estimated_effects'])
        idiosyncratic = pd.DataFrame(self.dependent.values2d - fitted.values, index,
                                     ['idiosyncratic'])

        eps = self.dependent.values2d - fitted.values
        weps = wy - wx @ params
        w = self.weights.values2d
        root_w = np.sqrt(w)
        #
        residual_ss = float(weps.T @ weps)
        y = e = self.dependent.values2d
        if self.has_constant:
            e = y - (w * y).sum() / w.sum()
        total_ss = float(w.T @ (e ** 2))
        r2 = 1 - residual_ss / total_ss

        if cov_type in ('robust', 'unadjusted', 'homoskedastic', 'heteroskedastic'):
            cov_est = FamaMacBethCovariance
        elif cov_type == 'kernel':
            cov_est = FamaMacBethKernelCovariance
        else:
            raise ValueError('Unknown cov_type')

        cov = cov_est(wy, wx, params, all_params, debiased=debiased, **cov_config)
        df_resid = wy.shape[0] - params.shape[0]
        res = self._postestimation(params, cov, debiased, df_resid, weps, wy, wx, root_w)
        index = self.dependent.index
        res.update(dict(df_resid=df_resid, df_model=x.shape[1], nobs=y.shape[0],
                        residual_ss=residual_ss, total_ss=total_ss,
                        r2=r2, resids=eps, wresids=weps, index=index, fitted=fitted,
                        effects=effects, idiosyncratic=idiosyncratic))
        return PanelResults(res)

    @classmethod
    def from_formula(cls, formula, data, *, weights=None):
        """
        Create a model from a formula

        Parameters
        ----------
        formula : str
            Formula to transform into model. Conforms to patsy formula rules.
        data : array-like
            Data structure that can be coerced into a PanelData.  In most
            cases, this should be a multi-index DataFrame where the level 0
            index contains the entities and the level 1 contains the time.
        weights: array-like, optional
            Weights to use in estimation.  Assumes residual variance is
            proportional to inverse of weight to that the residual times
            the weight should be homoskedastic.

        Returns
        -------
        model : FamaMacBeth
            Model specified using the formula

        Notes
        -----
        Unlike standard patsy, it is necessary to explicitly include a
        constant using the constant indicator (1)

        Examples
        --------
        >>> from linearmodels import BetweenOLS
        >>> mod = FamaMacBeth.from_formula('y ~ 1 + x1', panel_data)
        >>> res = mod.fit()
        """
        parser = PanelFormulaParser(formula, data)
        dependent, exog = parser.data
        mod = cls(dependent, exog, weights=weights)
        mod.formula = formula
        return mod