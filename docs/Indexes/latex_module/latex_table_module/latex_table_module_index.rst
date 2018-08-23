latex.table module
==================
Used for creating latex tables from pandas DataFrames. Has support for multiple panels in a table, and multiple DataFrames in a panel. Intelligently consolidates column and row headers across and within panels, and provides flexibility for controlling that behavior. Supports arbitrary underlines and automatic underlining of headers. Easiest usage is Table.from_list_of_lists_of_dfs, To apply different options to each panel, construct them individually using Panel.from_df_list or sub panels individually with DataTable.from_df then make modifications. Output to pdf using Table.to_pdf_and_move. 

.. toctree::
   :maxdepth: 3
   :caption: Contents:
   
   Panel
   DataTable
   LabelCollection
   LabelTable
   Label
   Table
   show_contents