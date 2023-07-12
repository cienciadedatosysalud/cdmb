
# Generated by CodiumAI

import pytest

from cdmb.entities.Rule import InValuesRule
from cdmb.entities.Variable import Variable

"""
Code Analysis

Main functionalities:
The InValuesRule class is a subclass of the abstract Rule class and represents a rule that checks if a variable's value is in a list of specified values. It can also check if the value is not in the list if the negative parameter is set to True. The class generates an SQL expression based on the input parameters and provides methods to access the expression, name, description, subtype_comparison, list of values, and the affected variable.

Methods:
- __init__(self, variable: Variable, list_values: list, negative: bool = False): Initializes the InValuesRule object with a Variable object, a list of values, and a boolean flag to indicate if the rule should check for values not in the list.
- expression(self): Returns the SQL expression generated by the class.
- name(self): Returns the name of the rule.
- description(self): Returns the description of the rule.
- subtype_comparison(self): Returns the subtype comparison of the rule.
- list_values(self): Returns the list of values used in the rule.
- variable_affected(self): Returns the Variable object affected by the rule.
- get_structure(self): Returns a dictionary with the expression, name, and description of the rule.

Fields:
- _expression: A string representing the SQL expression generated by the class.
- _name: A string representing the name of the rule.
- _description: A string representing the description of the rule.
- _subtype_comparison: None, as this rule does not have a subtype comparison.
- _list_values: A list of values used in the rule.
- __variable_affected: The Variable object affected by the rule.
"""
class TestInValuesRule:
    #  Tests that the rule is created with a variable and a list of values
    def test_positive_rule_creation(self):
        variable = Variable('test_var', 'Test Variable')
        rule = InValuesRule(variable, [1, 2, 3])
        assert rule.variable_affected == variable
        assert rule.list_values == ['1', '2', '3']
        assert rule.subtype_comparison is None

    #  Tests that the rule expression is generated correctly for a positive rule
    def test_positive_rule_expression(self):
        variable = Variable('test_var', 'Test Variable')
        rule = InValuesRule(variable, [1, 2, 3])
        assert rule.expression == 'test_var IN (\'1\', \'2\', \'3\')'

    #  Tests that the rule expression is generated correctly for a negative rule
    def test_negative_rule_expression(self):
        variable = Variable('test_var', 'Test Variable')
        rule = InValuesRule(variable, [1, 2, 3], negative=True)
        assert rule.expression == 'test_var NOT IN (\'1\', \'2\', \'3\') '

    #  Tests that the rule name is set correctly
    def test_rule_name(self):
        variable = Variable('test_var', 'Test Variable')
        rule = InValuesRule(variable, [1, 2, 3])
        assert rule.name == 'test_var'
        rule.name = 'new_name'
        assert rule.name == 'new_name'

    #  Tests that the rule description is set correctly
    def test_rule_description(self):
        variable = Variable('test_var', 'Test Variable')
        rule = InValuesRule(variable, [1, 2, 3])
        assert rule.description == 'Rule for column test_var'
        rule.description = 'New description'
        assert rule.description == 'New description'

    #  Tests that an empty list of values raises a ValueError
    def test_empty_list_values(self):
        variable = Variable('test_var', 'Test Variable')
        with pytest.raises(ValueError):
            InValuesRule(variable, [])