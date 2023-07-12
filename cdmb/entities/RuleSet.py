import datetime
import random

from faker import Faker

from cdmb.typing.CommonDataModelTyping import ComparisonOperators
from cdmb.entities.Rule import Rule, ComparisonRule, BetweenComparison, InValuesRule
from cdmb.entities.Variable import Variable


class RuleSet:
    def __init__(
            self,
            rules: list[Rule] = None
    ):
        """
A class to represent a set of rules for a data model.

Parameters
----------
    rules : list[Rule], optional
        A list of rules to be applied to the data model. (default is None)

Examples
--------
>>> # Constructing RuleSet
>>> age_var = Variable('age', "patient's age")
>>> rule_1 = ComparisonRule(
>>>     left_statement=age_var,
>>>     comparison_operator=">",
>>>     right_statement=18
>>>     )
>>> rule_2 = ComparisonRule(
>>>     left_statement=age_var,
>>>     comparison_operator="<",
>>>     right_statement=65
>>>     )
>>> rule_set = RuleSet(
>>>     rules=[rule_1, rule_2]
>>>     )


See Also
--------
Rule : A class to represent a rule for a variable or an entity.

"""

        self._description = '''The expressions of the different rules follow the syntax of the SQL OLAP database 
        management system called DuckDB. For more information, visit https://duckdb.org/docs/sql/introduction. 
        Keep in mind that you only have to declare as a rule the statement that would follow a WHERE clause. 
        e.g.,  Select * from people WHERE {expression}
        expression = age >= 18
        '''
        if rules is not None:
            errmsg = '"rules" argument must be a list of Rule objects.'
            if not isinstance(rules, list) or not all([isinstance(rul, Rule) for rul in rules]):
                raise TypeError(errmsg)
        self._rules: list[Rule] = [] if rules is None else rules

    @property
    def rules(self):
        return self._rules

    @rules.setter
    def rules(self, rules: list[Rule]):
        errmsg = '"rules" argument must be a list of Rule objects.'
        if not isinstance(rules, list) or not all([isinstance(rul, Rule) for rul in rules]):
            raise TypeError(errmsg)
        self._rules = rules

    def append_rule(self, rule: Rule):
        current_list = self._rules
        current_list.append(rule)
        self._rules = current_list

    def pop_rule(self):
        current_list = self._rules
        element = current_list.pop()
        self._rules = current_list
        return element

    def rules_for_synthetic_data(self, variable_list: [Variable]):
        rules_set = {}
        for variable in variable_list:
            rules_set['' + variable.label + ''] = []
        for rule in self._rules:
            if rule.subtype_comparison != "variable":
                if isinstance(rule, ComparisonRule):
                    if rule.subtype_comparison == 'date':
                        rules_set['' + rule.name + ''].append(
                            {
                                "category": "date_comparison",
                                "min_value": rule.min_value,
                                "max_value": rule.max_value
                            }
                        )
                    elif rule.subtype_comparison == 'datetime':
                        rules_set['' + rule.name + ''].append(
                            {
                                "category": "datetime_comparison",
                                "min_value": rule.min_value,
                                "max_value": rule.max_value
                            }
                        )
                    else:
                        # numeric
                        rules_set['' + rule.name + ''].append(
                            {
                                "category": "number_comparison",
                                "min_value": rule.min_value,
                                "max_value": rule.max_value
                            }
                        )

                elif isinstance(rule, BetweenComparison):
                    if rule.subtype_comparison == 'date':
                        rules_set['' + rule.name + ''].append(
                            {
                                "category": "date_interval_comparison",
                                "min_value": rule.min_value,
                                "max_value": rule.max_value,
                                "negative": rule.negative
                            }
                        )
                    elif rule.subtype_comparison == 'datetime':
                        rules_set['' + rule.name + ''].append(
                            {
                                "category": "datetime_interval_comparison",
                                "min_value": rule.min_value,
                                "max_value": rule.max_value,
                                "negative": rule.negative
                            }
                        )
                    else:
                        # numeric
                        rules_set['' + rule.name + ''].append(
                            {
                                "category": "number_interval_comparison",
                                "min_value": rule.min_value,
                                "max_value": rule.max_value,
                                "negative": rule.negative
                            }
                        )
                elif isinstance(rule, InValuesRule):
                    rules_set['' + rule.name + ''].append(
                        {
                            "category": "restricted",
                            "values": rule.list_values
                        }
                    )
        for variable in variable_list:
            if len(rules_set['' + variable.label + '']) == 0:
                del rules_set['' + variable.label + '']
        return rules_set

    def get_rules_comparison_between_variables(self, variable_list: list[Variable]):
        rules_set = {}
        for variable in variable_list:
            rules_set['' + variable.label + ''] = []

        for rule in self._rules:
            if rule.subtype_comparison == "variable":
                if isinstance(rule, ComparisonRule):
                    if rule.min_value is None and rule.max_value is not None:
                        # var 1 <= var2 (max value)
                        rules_set['' + rule.variable_affected.label + ''].append(rule.max_value)
                    elif rule.min_value is not None and rule.max_value is None:
                        # var 1 >= var2 (max value)
                        rules_set['' + rule.min_value + ''].append(rule.variable_affected.label)
        return rules_set

    def get_rules_dict(self):
        response = {'description': self._description, 'rules': []}
        for rule in self._rules:
            response['rules'].append(
                {
                    'expression': rule.expression,
                    'name': rule.name,
                    'description': rule.description
                }
            )
        return response

    def get_structure(self):
        return [r.get_structure() for r in self._rules]

    @staticmethod
    def get_rules_structure_example(variables: list[Variable]):
        fake = Faker()
        response = {'description': '''The expressions of the different rules follow the syntax of the SQL OLAP database 
        management system called DuckDB. For more information, visit https://duckdb.org/docs/sql/introduction. 
        Keep in mind that you only have to declare as a rule the statement that would follow a WHERE clause. 
        e.g.,  Select * from people WHERE {expression}
        expression = age >= 18
        ''', 'rules': []}
        for variable in variables:
            if variable.format == 'Integer':
                response['rules'].append(
                    {
                        'expression': variable.label + ' ' + random.choice(ComparisonOperators.__args__) + ' ' + str(
                            fake.pyint(max_value=80)),
                        'name': variable.label,
                        'description': "Rule for column '" + variable.label + "'"
                    }
                )
            elif variable.format == "Double":
                response['rules'].append(
                    {
                        'expression': variable.label + ' ' + random.choice(ComparisonOperators.__args__) + ' ' + str(
                            fake.pyfloat(right_digits=2, min_value=0,
                                         max_value=1000)),
                        'name': variable.label,
                        'description': "Rule for column '" + variable.label + "'"
                    }
                )
            elif variable.format == "String":
                response['rules'].append(
                    {
                        'expression': variable.label + ' = \'' + str(
                            fake.pystr()) + '\'',
                        'name': variable.label,
                        'description': "Rule for column '" + variable.label + "'"
                    }
                )

            elif variable.format == "Date":
                response['rules'].append(
                    {
                        'expression': variable.label + ' ' + random.choice(
                            ComparisonOperators.__args__) + ' \'' + datetime.date.today().strftime(
                            "%Y-%m-%d") + '\'',
                        'name': variable.label,
                        'description': "Rule for column '" + variable.label + "'"
                    }
                )
            elif variable.format == "Datetime":
                response['rules'].append(
                    {
                        'expression': variable.label + ' ' + random.choice(
                            ComparisonOperators.__args__) + ' \'' + datetime.datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S") + '\'',
                        'name': variable.label,
                        'description': "Rule for column '" + variable.label + "'"
                    }
                )
        return response
