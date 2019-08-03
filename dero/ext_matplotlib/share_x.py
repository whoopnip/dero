from typing import List, Optional, Dict, Any, Tuple
import matplotlib.pyplot as plt
import pandas as pd


def share_x_graph(df: pd.DataFrame, cols: List[str],
                  plot_col_kwarg_dict: Optional[Dict[str, Dict[str, Any]]] = None,
                  gridspec_kw: Optional[Dict[str, Any]] = None,
                  **plot_kwargs) -> Tuple[plt.Figure, List[plt.Axes]]:

    if plot_col_kwarg_dict is None:
        plot_col_kwarg_dict = {col: {} for col in cols}
    if gridspec_kw is None:
        gridspec_kw = {}

    fig, axes = plt.subplots(nrows=len(cols), ncols=1, sharex=True, gridspec_kw=gridspec_kw)

    for i, col in enumerate(cols):
        print(f'plotting {col} {plot_col_kwarg_dict[col]} {plot_kwargs}')
        df[col].plot(ax=axes[i], **plot_col_kwarg_dict[col], **plot_kwargs)
    return fig, list(axes)

