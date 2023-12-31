
# Generated by CodiumAI

import pytest

from cdmb.entities.Rule import ComparisonRule, Rule
from cdmb.entities.Variable import Variable

"""
Code Analysis

Main functionalities:
The ComparisonRule class is a subclass of the abstract class Rule and represents a rule that compares a left statement with a right statement using a comparison operator. The main functionalities of this class are:
- To create a comparison rule with a left statement, a comparison operator, and a right statement.
- To validate the types of the left statement, the comparison operator, and the right statement.
- To treat the right statement according to its type and the comparison operator.
- To generate an expression that represents the comparison rule.
- To provide information about the comparison rule, such as its name, description, subtype comparison, max value, min value, and variable affected.

Methods:
- __init__: initializes the ComparisonRule object with a left statement, a comparison operator, and a right statement. It validates the types of the left statement, the comparison operator, and the right statement, and treats the right statement according to its type and the comparison operator. It generates an expression that represents the comparison rule, and provides information about the comparison rule, such as its name, description, subtype comparison, max value, min value, and variable affected.
- expression: returns the expression that represents the comparison rule.
- name: returns the name of the comparison rule.
- name.setter: sets the name of the comparison rule.
- description: returns the description of the comparison rule.
- description.setter: sets the description of the comparison rule.
- subtype_comparison: returns the subtype comparison of the comparison rule.
- max_value: returns the max value of the comparison rule.
- min_value: returns the min value of the comparison rule.
- variable_affected: returns the variable affected by the comparison rule.
- get_structure: returns a dictionary with the expression, name, and description of the comparison rule.

Fields:
- _expression: a string that represents the expression of the comparison rule.
- _name: a string that represents the name of the comparison rule.
- _description: a string that represents the description of the comparison rule.
- _subtype_comparison: a string that represents the subtype comparison of the comparison rule.
- __max_value: a variable that represents the max value of the comparison rule.
- __min_value: a variable that represents the min value of the comparison rule.
- __variable_affected: a variable that represents the variable affected by the comparison rule.
"""
class TestComparisonRule:
    #  Tests that a ComparisonRule object can be successfully instantiated with valid input parameters
    def test_instantiation(self):
        left_statement = Variable('test_var', 'int')
        comparison_operator = '<='
        right_statement = 10
        rule = ComparisonRule(left_statement, comparison_operator, right_statement)
        assert isinstance(rule, Rule)
        assert isinstance(rule, ComparisonRule)
        assert rule.variable_affected == left_statement
        assert rule.subtype_comparison == 'number'
        assert rule.max_value == 10
        assert rule.min_value is None

    #  Tests that the expression property returns the expected string
    def test_expression_property(self):
        left_statement = Variable('test_var', 'int')
        comparison_operator = '<='
        right_statement = 10
        rule = ComparisonRule(left_statement, comparison_operator, right_statement)
        expected_expression = 'test_var <= 10'
        assert rule.expression == expected_expression

    #  Tests that the name property returns the expected string
    def test_name_property(self):
        left_statement = Variable('test_var', 'int')
        comparison_operator = '<='
        right_statement = 10
        rule = ComparisonRule(left_statement, comparison_operator, right_statement)
        expected_name = 'test_var'
        assert rule.name == expected_name

        rule.name = 'new_name'
        assert rule.name == 'new_name'

    #  Tests that the description property returns the expected string
    def test_description_property(self):
        left_statement = Variable('test_var', 'int')
        comparison_operator = '<='
        right_statement = 10
        rule = ComparisonRule(left_statement, comparison_operator, right_statement)
        expected_description = 'Rule for column test_var'
        assert rule.description == expected_description

        rule.description = 'new_description'
        assert rule.description == 'new_description'

    #  Tests that a ValueError is raised when comparison_operator argument is not a valid ComparisonOperator
    def test_comparison_operator_edge_case(self):
        left_statement = Variable('test_var', 'int')
        comparison_operator = 'invalid_operator'
        right_statement = 10
        with pytest.raises(ValueError):
            ComparisonRule(left_statement, comparison_operator, right_statement)

    #  Tests that a TypeError is raised when right_statement argument is boolean and comparison_operator is not '=', '<>', or '!='
    def test_right_statement_boolean_edge_case(self):
        left_statement = Variable('test_var', 'int')
        comparison_operator = '<='
        right_statement = True
        with pytest.raises(TypeError):
            ComparisonRule(left_statement, comparison_operator, right_statement)

        comparison_operator = '>'
        with pytest.raises(TypeError):
            ComparisonRule(left_statement, comparison_operator, right_statement)

        comparison_operator = '!='
        ComparisonRule(left_statement, comparison_operator, right_statement)

    #  Tests that the expression property returns the expected string when right_statement argument is a boolean
    def test_expression_property_boolean_right_statement(self):
        left_statement = Variable('var1','description')
        comparison_operator = '='
        right_statement = True
        rule = ComparisonRule(left_statement, comparison_operator, right_statement)
        assert rule.expression == 'var1 = TRUE'

    #  Tests that the expression property returns the expected string when right_statement argument is a Variable object
    def test_expression_property_variable_right_statement(self):
        left_statement = Variable('var1','description')
        comparison_operator = '='
        right_statement = Variable('var2','description')
        rule = ComparisonRule(left_statement, comparison_operator, right_statement)
        assert rule.expression == 'var1 = var2'
