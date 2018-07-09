
from dero.latex.models.package import Package
from dero.latex.table.models.texgen.newcolumntype import NewColumnTypes

class ColumnTypesPackage(Package):
    """
    New column types are created by importing the dcolumn package then adding the column type definition lines
    """

    def __init__(self):
        super().__init__('dcolumn')

    def __str__(self):
        from dero.latex.logic.builder import _build
        package_import = super().__str__()
        return _build([
            package_import,
            NewColumnTypes
        ])
