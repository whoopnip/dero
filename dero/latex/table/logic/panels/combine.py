import copy

from dero.latex.table.models.panels.grid import PanelGrid
from dero.latex.table.models.labels.table import LabelTable
from dero.latex.table.models.labels.collection import LabelCollection
from dero.latex.table.models.table.section import TableSection

def common_column_labels(grid: PanelGrid, use_object_equality=True):
    axis = 1 # columns
    all_column_ints = list(range(grid.shape[1]))

    return _selected_common_labels_for_axis(
        grid,
        selections=all_column_ints,
        axis=axis,
        use_object_equality=use_object_equality
    )

def common_row_labels(grid: PanelGrid, use_object_equality=True):
    axis = 0  # rows
    all_row_ints = list(range(grid.shape[0]))

    return _selected_common_labels_for_axis(
        grid,
        selections=all_row_ints,
        axis=axis,
        use_object_equality=use_object_equality
    )


def _selected_common_labels_for_axis(grid: PanelGrid, selections: [int]=[0], axis: int=0, use_object_equality=True):
    common_label_tables: [LabelTable] = []
    for i in selections:
        common_label_tables.append(
            _common_labels(
                grid,
                i,
                axis=axis,
                use_object_equality=use_object_equality
            )
        )

    return common_label_tables


def _common_labels(grid: PanelGrid, num: int, axis: int=0, use_object_equality=True):
    subgrid = _get_subgrid(
        grid=grid,
        num=num,
        axis=axis
    )

    label_attr = _get_label_attr(axis=axis)

    label_tables: [LabelTable] = [getattr(section, label_attr, None) for section in subgrid]

    common_label_collections = []
    for i, label_collection in enumerate(label_tables[0]):
        for label_table in label_tables[1:]:
            match = _compare_label_collections(
                label_collection,
                label_table[i],
                use_object_equality=use_object_equality
            )
            if match:
                common_label_collections.append(label_collection)
            else:
                break # as soon as one label collection doesn't match, stop consolidating

    return LabelTable(common_label_collections)

def _remove_label_collections(section: TableSection, label_table: LabelTable, axis: int=0,
                              use_object_equality=True):

    # Handle section not having labels for this axis
    label_attr = _get_label_attr(axis=axis)
    if not hasattr(section, label_attr):
        return section

    # Now has labels for this axis. Create a copy to avoid modifying original
    out_section = copy.deepcopy(section)

    for label_collection in label_table:
        for section_label_collection in getattr(section, label_attr, []):
            match = _compare_label_collections(
                label_collection,
                section_label_collection,
                use_object_equality=use_object_equality
            )
            if match:
                getattr(out_section, label_attr).remove(section_label_collection)

    return out_section


def _get_label_attr(axis: int=0):
    # select rows
    if axis == 0:
        return 'row_labels'
    # select columns
    elif axis == 1:
        return 'column_labels'
    else:
        raise ValueError(f'axis must be 0 or 1, got {axis}')

def _get_subgrid(grid: PanelGrid, num: int, axis: int=0):
    # select rows
    if axis == 0:
        return _grid_if_not(grid[num])
    # select columns
    elif axis == 1:
        return _grid_if_not(grid[:, num])
    else:
        raise ValueError(f'axis must be 0 or 1, got {axis}')

def _grid_if_not(ambiguous_grid):
    if isinstance(ambiguous_grid, PanelGrid):
        return ambiguous_grid
    else:
        return PanelGrid([ambiguous_grid])

def _compare_label_collections(collection1: LabelCollection, collection2: LabelCollection, use_object_equality=True):
    if use_object_equality:
        return collection1 == collection2
    else:
        return collection1.matches(collection2)