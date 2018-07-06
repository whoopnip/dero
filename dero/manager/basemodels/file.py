import os
from typing import TYPE_CHECKING, List, Tuple
if TYPE_CHECKING:
    from dero.manager.basemodels.config import ConfigBase

from dero.manager.sectionpath.sectionpath import _strip_py

from dero.manager.config.logic.load import (
    _split_assignment_line_into_variable_name_and_assignment
)
from dero.manager.config.logic.write import (
    import_lines_as_str,
    assignment_lines_as_str
)
from dero.manager.imports.models.statements.obj import ObjectImportStatement
from dero.manager.imports.models.statements.container import ImportStatementContainer


class ConfigFileBase:

    ##### Scaffolding functions or attributes. Need to override when subclassing  ####

    def load(self) -> 'ConfigBase':
        """

        Override this function when subclassing ConfigFileBase. Need to use self._load_into_config_dict,
        to get a dictionary of configuration, then create a Config instance from it. For example, see below:

        from dero.manager.config.models.config import FunctionConfig

        config_dict = self._load_into_config_dict()

        return FunctionConfig(config_dict, _loaded_modules=self._loaded_modules, _file=self, name=self.name)

        """
        raise NotImplementedError('must use FunctionConfigFile.load or DataConfigFile.load, not ConfigFileBase.load')

    def _load_into_config_dict(self) -> dict:
        """

        Assigns to self._loaded_modules, self._lines, self.imports, self.assigns
        Returns: config_dict

        """
        raise NotImplementedError('must use FunctionConfigFile._load_into_config_dict or '
                                  'DataConfigFile._load_into_config_dict, not ConfigFileBase._load_into_config_dict')

    def _config_to_file_lines(self, config: 'ConfigBase') -> Tuple[List[str], List[str]]:
        """

        Args:
            config:

        Returns:

        """
        raise NotImplementedError('must use FunctionConfigFile._config_to_file_lines or'
                                  ' DataConfigFile._config_to_file_lines, not ConfigFileBase._config_to_file_lines')

    ##### Base class functions and attributes below. Shouldn't usually need to override in subclassing #####

    def __init__(self, filepath: str, name: str=None, loaded_modules=None):
        self.filepath = filepath

        if name is None:
            name = _strip_py(os.path.basename(filepath))

        self.name = name
        self.imports = ImportStatementContainer([])
        self._assigns = []
        self._loaded_modules = loaded_modules

    @property
    def content(self):
        return '\n'.join(self._lines)

    def save(self, config: 'ConfigBase') -> None:
        import_lines, assignment_lines = self._config_to_file_lines(config)
        self._add_new_lines(import_lines, assignment_lines)
        file_str = self.file_str # access here, so that if error in assembling, will not overwrite file

        with open(self.filepath, 'w') as f:
            f.write(file_str)

    @property
    def file_str(self) -> str:
        return self._import_section + self._assignment_section

    @property
    def _import_section(self) -> str:
        return import_lines_as_str(self.imports)

    @property
    def _assignment_section(self) -> str:
        return assignment_lines_as_str(self._assigns)

    @property
    def assigned_variables(self) -> List[str]:

        if hasattr(self, '_assigned_variables'):
            return self._assigned_variables

        self._set_assigned_variables()
        return self._assigned_variables

    def _set_assigned_variables(self):
        assigned_variables = []
        for line in self._assigns:
            variable_name, value_repr = _split_assignment_line_into_variable_name_and_assignment(line)
            assigned_variables.append(variable_name)
        self._assigned_variables = assigned_variables

    @property
    def assigns(self):
        return self._assigns

    @assigns.setter
    def assigns(self, assigns: List[str]):
        self._assigns = assigns
        self._set_assigned_variables()

    def _add_new_lines(self, new_imports_lines: List[str], new_variable_assignment_lines: List[str]) -> None:
        always_imports = [
            ObjectImportStatement.from_str('from dero.manager import Selector')
        ]

        always_assign_strs = [
            's = Selector()'
        ]

        # For import statements, just check if they already exist exactly as generated
        [_append_if_not_in_list(self.imports, line) for line in new_imports_lines]

        # Add always imports
        always_imports.reverse() # are getting added to beginning, so reverse order first to maintain order
        for import_obj in always_imports:
            if import_obj not in self.imports:
                self.imports.insert(0, import_obj)

        # Add always assigns
        always_assign_strs.reverse() # are getting added to beginning, so reverse order first to maintain order
        for line in always_assign_strs:
            variable_name, value_repr = _split_assignment_line_into_variable_name_and_assignment(line)
            if variable_name is None:
                continue  # whitespace line
            if variable_name not in self.assigned_variables:
                self.assigns.insert(0, line)
                self._set_assigned_variables()

        # For assignment statements, check if the variable name is already defined. Then don't add
        # the new line. Different handling as value may not be set correctly by code.
        for line in new_variable_assignment_lines:
            variable_name, value_repr = _split_assignment_line_into_variable_name_and_assignment(line)
            if variable_name is None:
                continue  # whitespace line
            if variable_name not in self.assigned_variables:
                self.assigns.append(line)
                # need to trigger set so that assigned variables will update from self.assigns
                self._set_assigned_variables()

    def _get_loaded_modules(self, config: 'ConfigBase') -> List[str]:
        if config._loaded_modules is not None:
            return config._loaded_modules
        elif self._loaded_modules is not None:
            return self._loaded_modules
        else:
            return None

def _append_if_not_in_list(list_: List, item) -> None:
    if item not in list_:
        list_.append(item)