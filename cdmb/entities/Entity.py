import re
import uuid

import pandas as pd
from pandas.errors import ParserError

from cdmb.entities.Rule import Rule, BetweenComparison, NullCheckingRule, ComparisonRule, InValuesRule
from cdmb.entities.RuleSet import RuleSet
from cdmb.entities.Variable import Variable


class Entity:
    def __init__(
            self,
            name: str,
            time_varying: bool = False,
            variables: list[Variable] = None,
            rules: RuleSet = None
    ):
        """
A class to represent an entity in a data model.

Parameters
----------
    name : str
        The name of the entity, without spaces.
    time_varying : bool, optional
        A flag indicating whether the entity is time-varying or not. (default is False)
    variables : list[Variable], optional
        A list of Variable objects that belong to the entity. (default is None)
    rules : RuleSet, optional
        A RuleSet object containing the rules that apply to the entity. (default is None)

Raises
------
ValueError
    If any of the arguments are invalid or out of range.
TypeError
    If any of the arguments are not of the expected type.

Examples
--------
>>> # Constructing Entity
>>> entity_ = Entity(
>>>       name="Patient",
>>>       time_varying=True,
>>>       variables=[
>>>           Variable('age', "patient's age"),
>>>           Variable('admission_dt', 'hospital admission'),
>>>          Variable('discharge_dt', 'hospital discharge')
>>>       ]
>>>       rules=RuleSet([
>>>         ComparisonRule(
>>>                Variable('admission_dt', 'hospital admission'),
>>>                '<=',
>>>                Variable('discharge_dt', 'hospital discharge')
>>>         )
>>>       ])
>>>     )


See Also
--------
    Variable : A class to represent a variable in a data model.
    RuleSet : A class to represent a set of rules for an entity or a variable.

"""

        if variables is not None:
            errmsg = '"variables" argument must be a list of Variable.'
            if not isinstance(variables, list) or not all([isinstance(val, Variable) for val in variables]):
                raise TypeError(errmsg)

            labels = [var.label for var in variables]
            if len(labels) != len(set(labels)):
                raise ValueError('There cannot be two or more variables with the same label.')

        errmsg = '"time_varying" argument must be boolean'
        if not isinstance(time_varying, bool):
            raise TypeError(errmsg)

        if rules is not None:
            errmsg = '"rules" argument must be RuleSet'
            if not isinstance(rules, RuleSet):
                raise TypeError(errmsg)

        if ' ' in name:
            raise ValueError('"name" argument cannot contain spaces. Replace it with "_".')

        if name.strip() == "":
            raise ValueError('"name" argument cannot be an empty string.')
        if len(name) > 50:
            raise ValueError('The argument "name" must be less than 50 characters.')

        self._uuid = str(uuid.uuid4())
        self._name: str = name
        self._time_varying: bool = time_varying
        self._variables: list[Variable] = variables if variables is not None else []
        self._rules: RuleSet = rules if rules is not None else RuleSet()

    @property
    def uuid(self):
        return self._uuid

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def time_varying(self):
        return self._time_varying

    @time_varying.setter
    def time_varying(self, time_varying: bool):
        errmsg = '"time_varying" argument must be boolean.'
        if not isinstance(time_varying, bool):
            raise TypeError(errmsg)
        self._time_varying = time_varying

    @property
    def variables(self):
        return self._variables

    @variables.setter
    def variables(self, variables: list[Variable]):
        errmsg = '"variables" argument must be a list of Variable.'
        if not isinstance(variables, list) or not all([isinstance(val, Variable) for val in variables]):
            raise TypeError(errmsg)

        labels = [var.label for var in variables]
        if len(labels) != len(set(labels)):
            raise ValueError('There cannot be two or more variables with the same label.')

        self._variables = variables

    def add_variable(self, variable: Variable):
        labels = [var.label for var in self._variables]
        if variable.label in labels:
            raise ValueError('There cannot be two or more variables with the same label.')
        current_list = self._variables
        current_list.append(variable)
        self._variables = current_list

    def pop_variable(self):
        current_list = self._variables
        element = current_list.pop()
        self._variables = current_list
        return element

    def get_variable_by_label(self, label: str) -> Variable:
        response = None
        for variable in self.variables:
            if variable.label == label:
                response = variable
                break
        return response

    @property
    def rules(self):
        return self._rules

    @rules.setter
    def rules(self, rules: RuleSet):
        errmsg = '"rules" argument must be RuleSet.'
        if not isinstance(rules, RuleSet):
            raise TypeError(errmsg)
        self._rules = rules

    def get_catalogs(self) -> tuple[dict[str, str], dict[str, any]]:
        distinct_catalogs = set(
            [variable.catalog.filename for variable in self.variables if variable.catalog_bl and variable.catalog])
        variables_with_catalog = [variable for variable in self.variables if variable.catalog_bl and variable.catalog]
        catalog_by_filename = {}
        catalog_by_label = {}
        for filename in distinct_catalogs:
            catalog_by_filename[filename] = {"data": pd.DataFrame(), "variable_list": []}

        for variable in variables_with_catalog:
            label_ = variable.label
            catalog_column_name = variable.catalog.column_name
            filename_ = variable.catalog.filename
            data_ = variable.catalog.data
            data_ = data_[catalog_column_name]
            data_.rename(label_, inplace=True)
            catalog_by_filename[filename_]["data"] = pd.concat([catalog_by_filename[filename_]["data"], data_], axis=1)
            catalog_by_filename[filename_]["variable_list"].append(label_)
            catalog_by_label[label_] = filename_
        return catalog_by_label, catalog_by_filename

    def get_rules_synthetic(self):
        return self._rules.rules_for_synthetic_data(self._variables)

    def dict_to_variables(self, variables_dict: [dict]):
        for element in variables_dict:
            del element['catalog']
            element['catalog_bl'] = False
            var = Variable(**element)
            self.add_variable(var)
        return self._variables

    def get_rules_structure(self):
        response = self.rules.get_rules_dict()
        response['entity'] = self._name
        return response

    def get_structure(self):
        return {
            "uuid": self._uuid,
            "name": self._name,
            "time_varying": self._time_varying,
            "variables": [v.get_structure() for v in self._variables],
            "rules": self._rules.get_structure()
        }

    class Tree:
        def __init__(self, variable):
            self.children: list[Variable] = []
            self.variable: Variable = variable
            self.parent: Variable = None

    def get_variables_in_order(self, first_variable: Variable):
        response = [first_variable]
        for variable in self._variables:
            if variable.label != first_variable.label:
                response.append(variable)
        return response

    def get_tree_structure_rules(self, variable_order_) -> Tree:
        variable_order = {}
        for var in variable_order_:
            variable_order[var.label] = self.Tree(var)

        dependencies = self._rules.get_rules_comparison_between_variables(variable_order_)
        for label, dependency in dependencies.items():
            if len(dependency) > 0:
                for d in dependency:
                    variable_order[label].children.append(variable_order[d])
        tree_response = self.Tree(None)
        for tree_order in variable_order.values():
            tree_response.children.append(tree_order)
        return tree_response

    def create_rule_from_expression(self, exp: str, name: str = None, description: str = None) -> Rule:
        entity = self
        rule: Rule = None
        ### regular expresion
        exp1 = re.search(
            "(\w+)\s*(=|>=|<=|<>|<|>|!=)\s*(\'\d+[\-\/]+\d+[\-\/]+\d+\s*(?:\d{2}:\d{2}:\d{2})*\'|\'[a-zA-Z_]+\'|[a-zA-Z_]+|\d*\.?\d+)",
            exp)
        if exp1 is not None:
            left_statement = exp1.groups()[0]
            comparison_operator = exp1.groups()[1]
            right_statement = exp1.groups()[2]

            left_statement = entity.get_variable_by_label(left_statement)
            if left_statement is None:
                raise ValueError('The variable "' + left_statement + '" does not belong to the entity.')

            if '\'' in right_statement:
                try:
                    right_statement = pd.to_datetime(right_statement)
                    right_statement = right_statement.to_pydatetime()
                except ParserError:
                    pass
            else:
                # variable, int or float
                var = entity.get_variable_by_label(right_statement)
                if var is None:
                    # int or float
                    if '.' in right_statement:
                        # float
                        right_statement = float(right_statement)
                    else:
                        right_statement = int(right_statement)
                else:
                    right_statement = var

            rule = ComparisonRule(left_statement, comparison_operator, right_statement)

        # Between rule
        exp2 = re.search(
            "(\w+)\s*(BETWEEN|NOT BETWEEN|between|not between)\s*(\'\d*[\-\/]\d*[\-\/]\d*\s*(?:\d{2}:\d{2}:\d{2})*\'|\d*\.?\d*)\s*(?:AND|and)\s*(\'\d*[\-\/]\d*[\-\/]\d*\s*(?:\d{2}:\d{2}:\d{2})*\'|\d*\.?\d+)",
            exp)

        if exp2 is not None:
            left_statement = exp2.groups()[0]
            beetween_operator = exp2.groups()[1]
            x_value = exp2.groups()[2]
            y_value = exp2.groups()[3]

            left_statement = entity.get_variable_by_label(left_statement)
            if left_statement is None:
                raise ValueError('The variable "' + left_statement + '" does not belong to the entity.')
            negative = False
            if 'NOT' in beetween_operator:
                negative = True
            if '\'' in x_value:
                # x_value is DATE
                try:
                    x_value = pd.to_datetime(x_value)
                    x_value = x_value.to_pydatetime()
                except ParserError:
                    raise ValueError('The variable "' + left_statement + '" does not belong to the entity.')

            else:
                # x_value is int or float
                if '.' in x_value:
                    x_value = float(x_value)
                else:
                    x_value = int(x_value)

            if '\'' in y_value:
                # y_value is DATE
                try:
                    y_value = pd.to_datetime(y_value)
                    y_value = y_value.to_pydatetime()
                except ParserError:
                    raise ValueError('The variable "' + left_statement + '" does not belong to the entity.')

            else:
                # y_value is int or float
                if '.' in y_value:
                    y_value = float(y_value)
                else:
                    y_value = int(y_value)

            rule = BetweenComparison(left_statement, x_value, y_value, negative)

        # Reglas is NULL
        exp3 = re.search("(\w+)\s*(IS NULL| IS NOT NULL)", exp)
        if exp3 is not None:
            left_statement = exp3.groups()[0]
            null_operator = exp3.groups()[1]
            left_statement = entity.get_variable_by_label(left_statement)
            if left_statement is None:
                raise ValueError('The variable "' + left_statement + '" does not belong to the entity.')
            negative = False
            if 'NOT' in null_operator:
                negative = True
            NullCheckingRule(left_statement, negative)

        # In values rule int and float
        exp4 = re.search("(\w+)\s*(IN|NOT IN|in|not in)\s\(((?:\d*\.?\d+)(?:\s*,\s*\d*\.?\d+)*)\)", exp)
        # palabra IN (1.1,2,3,4)
        if exp4 is not None:
            left_statement = exp4.groups()[0]
            in_operator = exp4.groups()[1]
            list_values = exp4.groups()[2]

            left_statement = entity.get_variable_by_label(left_statement)
            if left_statement is None:
                raise ValueError('The variable "' + left_statement + '" does not belong to the entity.')
            negative = False
            if 'NOT' in in_operator:
                negative = True

            list_values = list_values.split(',')

            if '.' in list_values[0]:
                list_values = [float(v) for v in list_values]
            else:
                list_values = [int(float(v)) for v in list_values]

            rule = InValuesRule(left_statement, list_values, negative)

        # In values rule str
        exp5 = re.search("(\w*)\s*(IN|NOT IN|in|not in)\s\(((?:\'\w+\')(?:\s*,\s*\'\w+\')*)\)", exp)
        if exp5 is not None:
            left_statement = exp5.groups()[0]
            in_operator = exp5.groups()[1]
            list_values = exp5.groups()[2]

            left_statement = entity.get_variable_by_label(left_statement)
            if left_statement is None:
                raise ValueError('The variable "' + left_statement + '" does not belong to the entity.')
            negative = False
            if 'NOT' in in_operator:
                negative = True
            list_values = list_values.split(',')
            list_values_ = [value.strip().replace('\'', '') for value in list_values]
            rule = InValuesRule(left_statement, list_values_, negative)

        # Reglas TRUE FALSE
        exp6 = re.search("(\w*)\s*(=|!=|<>)\s*(TRUE|FALSE)", exp)
        if exp6 is not None:
            left_statement = exp6.groups()[0]
            comparison_operator = exp6.groups()[1]
            right_statement = exp6.groups()[2]

            left_statement = entity.get_variable_by_label(left_statement)
            if left_statement is None:
                raise ValueError('The variable "' + left_statement + '" does not belong to the entity.')

            if right_statement == 'TRUE':
                right_statement = True
            else:
                right_statement = False

            rule = ComparisonRule(left_statement, comparison_operator, right_statement)
        return rule
