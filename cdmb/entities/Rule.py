import datetime
from abc import ABC, abstractmethod
from numbers import Number
from typing import Union

from cdmb.typing.CommonDataModelTyping import BooleanOperators
from cdmb.typing.CommonDataModelTyping import ComparisonOperators
from cdmb.entities.Variable import Variable


class Rule(ABC):

    @property
    @abstractmethod
    def expression(self) -> str:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def subtype_comparison(self):
        pass

    @abstractmethod
    def get_structure(self):
        pass


class ComparisonRule(Rule):
    def __init__(self,
                 left_statement: Variable,
                 comparison_operator: ComparisonOperators,
                 right_statement: Union[Variable, int, float, datetime.date, datetime.datetime, str,bool]):
        """
A class to represent a comparison rule for a variable.

Parameters
----------
    left_statement : Variable
        The variable to be compared.
    comparison_operator : ComparisonOperators
        An enumeration value indicating the comparison operator, such as =, <, >, etc.
    right_statement : Union[Variable, int, float, datetime.date, datetime.datetime, str,bool]
        The value or variable to be compared with the left statement.

Raises
------
TypeError
    If any of the arguments are not of the expected type.
ValueError
    If any of the arguments are invalid or out of range.

Examples
--------
>>> # ComparisonOperators ['<', '<=', '>', '>=', '=', '<>', '!=']

>>> left_statement = Variable('age', "patient's age")
>>> comparison_operator = '>='
>>> right_statement = 18
>>> rule = ComparisonRule(left_statement, comparison_operator, right_statement)

>>> # Compare variables
>>> left_statement = Variable('admission_dt', 'hospital admission')
>>> right_statement = Variable('discharge_dt', 'hospital discharge')
>>> rule2 = ComparisonRule(left_statement, '<=', right_statement)

>>> # Compare with dates
>>> rule3 = ComparisonRule(left_statement, '>=', datetime.date(2022,1,1))


See Also
--------
Variable : A class to represent a variable in a data model.
ComparisonOperators : An enumeration class for the possible comparison operators.

"""
        if not isinstance(left_statement, Variable):
            raise TypeError('"left_statement" argument must be Variable')

        if comparison_operator not in ComparisonOperators.__args__:
            raise ValueError('"comparison_operator" argument must be in {literal_values}'.format(
                literal_values=ComparisonOperators.__args__)
            )

        if type(right_statement) not in Union[Variable, int, float, datetime.date, datetime.datetime, str,bool].__args__:
            raise TypeError('"right_statement" argument must be in {literal_values}'.format(
                literal_values=Union[Variable, int, float, datetime.date, datetime.datetime, str,bool].__args__)
            )

        if type(right_statement) == bool and comparison_operator not in ['=', '<>', '!=']:
            raise TypeError('If "right_statement" argument is boolean only "=", "<>" and "!=" are allowed.')

        subtype_comparison = "number"
        # treat right_statement
        right_statement_ = right_statement
        if isinstance(right_statement, Variable):
            subtype_comparison = "variable"
            right_statement_ = right_statement.label
        elif isinstance(right_statement, str):
            subtype_comparison = "str"
            right_statement_ = "\'"+right_statement_+"\'"

        elif isinstance(right_statement, bool):
            subtype_comparison = "bool"
            right_statement_ = str(right_statement).upper()
        elif isinstance(right_statement, datetime.date):
            subtype_comparison = "date"
            right_statement_ = right_statement.strftime("%Y-%m-%d")
            right_statement_ = "\'"+right_statement_+"\'"


        elif isinstance(right_statement, datetime.date):
            subtype_comparison = "datetime"
            right_statement_ = right_statement.strftime("%Y-%m-%d %H:%M:%S")
            right_statement_ = "\'"+right_statement_+"\'"


        if comparison_operator in ['<=', '<']:
            self.__max_value = right_statement if subtype_comparison in ['number', 'date',
                                                                         'datetime'] else right_statement_
            self.__min_value = None
        elif comparison_operator in ['>=', '>']:
            self.__max_value = None
            self.__min_value = right_statement if subtype_comparison in ['number', 'date',
                                                                         'datetime'] else right_statement_
        else:
            self.__max_value = None
            self.__min_value = None

        expression = "{left_statement_} {comparison_operator_} {right_statement_}".format(
            left_statement_=left_statement.label,
            comparison_operator_=comparison_operator,
            right_statement_=right_statement_)

        self._expression = expression
        self._name = left_statement.label
        self._description = 'Rule for column ' + left_statement.label
        self._subtype_comparison = subtype_comparison
        self.__variable_affected = left_statement

    @property
    def expression(self):
        return self._expression

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description: str):
        self._description = description

    @property
    def subtype_comparison(self):
        return self._subtype_comparison

    @property
    def max_value(self):
        return self.__max_value

    @property
    def min_value(self):
        return self.__min_value

    @property
    def variable_affected(self):
        return self.__variable_affected

    def get_structure(self):
        return {
            "expression": self._expression,
            "name": self._name,
            "description": self._description
        }


class BetweenComparison(Rule):
    def __init__(self,
                 variable: Variable,
                 x_value: Union[Number, datetime.date, datetime.datetime],
                 y_value: Union[Number, datetime.date, datetime.datetime],
                 negative: bool = False
                 ):
        """
A class to represent a between comparison rule for a variable.

Parameters
----------
    variable : Variable
        The variable to be compared.
    x_value : Union[Number, datetime.date, datetime.datetime]
        The lower bound value for the comparison.
    y_value : Union[Number, datetime.date, datetime.datetime]
        The upper bound value for the comparison.
    negative : bool, optional
        A flag indicating whether the comparison is negated or not. (default is False)

Raises
------
    TypeError
        If any of the arguments are not of the expected type.
    ValueError
        If any of the arguments are invalid or out of range.

Examples
--------
>>> variable = Variable('age', "patient's age")
>>> x_value = 18
>>> y_value = 115
>>> r1 = BetweenComparison(variable, x_value, y_value)
>>> # r1 -> age BETWEEN 18 AND 115

>>> variable2 = Variable('admission_dt', 'hospital admission')
>>> r2 = BetweenComparison(variable2, datetime.date(2020,1,1), datetime.date(2021,1,1),negative=True)
>>> # r2 -> admission_dt NOT BETWEEN '2020-01-01' AND '2021-01-01'

See Also
--------
Variable : A class to represent a variable in a data model.

"""

        if not isinstance(variable, Variable):
            raise TypeError('"variable" argument must be Variable')

        if type(x_value) not in Union[int, float, datetime.date, datetime.datetime].__args__:
            raise TypeError('"x_value" argument must be int, float, datetime.date or  datetime.datetime')

        if type(y_value) not in Union[int, float, datetime.date, datetime.datetime].__args__:
            raise ValueError('"y_value" argument must be int, float, datetime.date or  datetime.datetime')

        if type(x_value) != type(y_value):
            raise ValueError('"x_type" argument and "y_type" argument must be the same type')

        if x_value > y_value:
            raise ValueError('"y_value" argument must be greater than "x_type" argument')

        subtype_comparison = "number"
        x_value_ = x_value
        if isinstance(x_value, datetime.date):
            subtype_comparison = "date"
            x_value_ = x_value.strftime("%Y-%m-%d")
            x_value_ = "'" + x_value_ + "'"

        elif isinstance(x_value, datetime.date):
            subtype_comparison = "datetime"
            x_value_ = x_value.strftime("%Y-%m-%d %H:%M:%S")
            x_value_ = "'" + x_value_ + "'"

        y_value_ = y_value
        if isinstance(y_value, datetime.date):
            y_value_ = y_value.strftime("%Y-%m-%d")
            y_value_ = "'"+y_value_+"'"

        elif isinstance(y_value, datetime.date):
            y_value_ = y_value.strftime("%Y-%m-%d %H:%M:%S")
            y_value_ = "'" + y_value_ + "'"

        if negative is False:
            expression = "{variable_} BETWEEN {x_value_} AND {y_value_}".format(
                variable_=variable.label,
                x_value_=x_value_,
                y_value_=y_value_)
        else:
            expression = "{variable_} NOT BETWEEN {x_value_} AND {y_value_}".format(
                variable_=variable.label,
                x_value_=x_value_,
                y_value_=y_value_)

        if subtype_comparison in ["date", "datetime"]:
            expression = expression.replace(x_value_, '\'' + x_value_ + '\'')
            expression = expression.replace(y_value_, '\'' + y_value_ + '\'')

        if negative is False and subtype_comparison in ['number', 'date', 'datetime']:
            self.__min_value = x_value
            self.__max_value = y_value

        elif negative is True and subtype_comparison in ['number', 'date', 'datetime']:
            self.__min_value = y_value
            self.__max_value = x_value

        else:
            self.__max_value = None
            self.__min_value = None

        self._expression = expression
        self._name = variable.label
        self._description = 'Rule for column ' + variable.label
        self._subtype_comparison = subtype_comparison
        self._negative = negative
        self.__variable_affected = variable

    @property
    def expression(self):
        return self._expression

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        if not isinstance(name, Variable):
            raise TypeError('"name" argument must be str')
        self._name = name

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description: str):
        if not isinstance(description, Variable):
            raise TypeError('"description" argument must be str')
        self._description = description

    @property
    def subtype_comparison(self):
        return self._subtype_comparison

    @property
    def negative(self):
        return self._negative

    @property
    def min_value(self):
        return self.__min_value

    @property
    def max_value(self):
        return self.__max_value

    @property
    def variable_affected(self):
        return self.__variable_affected

    def get_structure(self):
        return {
            "expression": self._expression,
            "name": self._name,
            "description": self._description
        }


class NullCheckingRule(Rule):
    def __init__(self,
                 variable: Variable,
                 negative: bool = True):
        """
A class to represent a null checking rule for a variable.

Parameters
----------
    variable : Variable
        The variable to be checked for null values.
    negative : bool, optional
        A flag indicating whether the rule is negated or not. (default is True)

Raises
------
    TypeError
        If the variable argument is not a Variable object.

Examples
--------
>>> variable_1 = Variable('admission_dt', 'hospital admission')
>>> rule = NullCheckingRule(variable_1, negative=True)
>>> # rule -> admission_dt IS NOT NULL

>>> variable_2 = Variable('discharge_dt', 'hospital discharge')
>>> rule2 = NullCheckingRule(variable_2, negative=False)
>>> # rule2 -> discharge_dt IS NULL


See Also
--------
Variable : A class to represent a variable in a data model.

"""
        if not isinstance(variable, Variable):
            raise TypeError('"variable" argument must be Variable')

        if negative is False:
            expression = "{variable_} IS NULL".format(variable_=variable.label)
        else:
            expression = "{variable_} IS NOT NULL".format(variable_=variable.label)

        self._expression = expression
        self._name = variable.label
        self._description = 'Rule for column ' + variable.label
        self._subtype_comparison = None
        self.__variable_affected = variable

    @property
    def expression(self):
        return self._expression

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description: str):
        self._description = description

    @property
    def subtype_comparison(self):
        return self._subtype_comparison

    @property
    def variable_affected(self):
        return self.__variable_affected

    def get_structure(self):
        return {
            "expression": self._expression,
            "name": self._name,
            "description": self._description
        }


class InValuesRule(Rule):
    def __init__(self,
                 variable: Variable,
                 list_values: list,
                 negative: bool = False):
        """
A class to represent an in values rule for a variable.

Parameters
----------
variable : Variable
    The variable to be checked for being in a list of values.
list_values : list
        A list of values to be compared with the variable.
negative : bool, optional
        A flag indicating whether the rule is negated or not. (default is False)

Raises
------
    ValueError
        If any of the arguments are invalid or out of range.
    TypeError
        If any of the arguments are not of the expected type.

Examples
--------
>>> # Constructing InValuesRule
>>> variable_1 = Variable('sex_cd', "patient's sex")
>>> rule = InValuesRule(variable_1,['1','2','3','9'])
>>> # rule -> sex_cd IN ('1','2','3','9')

>>> rule2 = InValuesRule(variable_1,['1','2','3','9'], negative=True)
>>> # rule2 ->  sex_cd NOT IN ('1','2','3','9')


See Also
--------
Variable : A class to represent a variable in a data model.

"""
        if len(list_values) == 0:
            raise ValueError('list_value must have at least one element.')

        list_values = list(map(str, list_values))
        if not isinstance(variable, Variable):
            raise ValueError('variable must be a Variable.')
        if not isinstance(list_values, list):
            raise ValueError('list_values must be a list of strings or numbers.')

        values_ = ', '.join(f"'{v}'" for v in list_values)
        if negative is False:
            expression = "{variable_} IN ({values_})".format(variable_=variable.label, values_=values_)
        else:
            expression = "{variable_} NOT IN ({values_}) ".format(variable_=variable.label, values_=values_)

        self._expression = expression
        self._name = variable.label
        self._description = 'Rule for column ' + variable.label
        self._subtype_comparison = None
        self._list_values = list_values
        self.__variable_affected = variable

    @property
    def expression(self):
        return self._expression

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description: str):
        self._description = description

    @property
    def subtype_comparison(self):
        return self._subtype_comparison

    @property
    def list_values(self):
        return self._list_values

    @property
    def variable_affected(self):
        return self.__variable_affected

    def get_structure(self):
        return {
            "expression": self._expression,
            "name": self._name,
            "description": self._description
        }


class ComposedRule(Rule):
    def __init__(self,
                 left_statement: Rule,
                 logical_operator: BooleanOperators,
                 right_statement: Rule):
        """
A class to represent a composed rule that combines two rules with a logical operator.

Parameters
----------
    left_statement : Rule
        The left rule to be combined.
    logical_operator : BooleanOperators
        An enumeration value indicating the logical operator, such as and, or, etc.
    right_statement : Rule
        The right rule to be combined.

Raises
------
    ValueError
        If any of the arguments are invalid or out of range.
    TypeError
        If any of the arguments are not of the expected type.

Examples
--------
>>> # Constructing ComposedRule
>>> variable_1 = Variable('sex_cd', "patient's sex")
>>> variable_2 = Variable('pregnancy_bl', "pregnancy status")

>>> composed_rule = ComposedRule(
>>>     left_statement=ComparisonRule(variable_1,'=','1'),
>>>     logical_operator='and',
>>>     right_statement=ComparisonRule(variable_2, '!=', False))

>>> # composed_rule -> (sex_cd = 1) and (pregnancy_bl != FALSE)


See Also
--------
Rule : A class to represent a rule for a variable or an entity.
BooleanOperators : An enumeration class for the possible logical operators.

"""
        if not isinstance(left_statement, Rule):
            raise ValueError('left_statement must be a Variable')

        if not isinstance(right_statement, Rule):
            raise ValueError('right_statement must be a Variable')

        if logical_operator not in BooleanOperators.__args__:
            raise ValueError('logical_operator not [\'and\', \'or\']')

        expression = "({left_statement_}) {boolean_operator_} ({right_statement_})".format(
            left_statement_=left_statement.expression,
            boolean_operator_=logical_operator,
            right_statement_=right_statement.expression)

        self._expression = expression
        self._name = 'Composed rule'
        self._description = 'Complex rule'
        self._subtype_comparison = None

    @property
    def expression(self):
        return self._expression

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description: str):
        self._description = description

    @property
    def subtype_comparison(self):
        return self._subtype_comparison

    def get_structure(self):
        return {
            "expression": self._expression,
            "name": self._name,
            "description": self._description
        }

def _check_type(value, expected_type):
    errmsg = f'"{value}" argument must be {expected_type}'
    if not isinstance(value, expected_type):
        raise TypeError(errmsg)

def validate_string_length(string: str, arg_name: str, could_be_null:bool):
    if could_be_null is False and (string is None or string == ""):
        raise ValueError(f'The argument "{arg_name}" cannot be null or an empty string.')

class DummyRule(Rule):

    def __init__(self,
                 expression: str,
                 name: str,
                 description: str):
        """
            A class to represent a dummy rule with a custom expression, name, and description. This class can be used to create a rule that does not fit into any of the other rule subclasses.
            Exploit the full potential of DuckDB by following its documentation (https://duckdb.org/docs/sql/introduction).

            Parameters
            ----------
                expression : str
                    The expression of the rule, without validation or logic.
                name : str
                    The name of the rule.
                description : str
                    The description of the rule.

            Raises
            ------
                TypeError
                    If any of the arguments are not strings.
                ValueError
                    If any of the arguments are empty strings.

            Examples
            --------
            >>> # Constructing DummyRule
            >>> r1 = DummyRule(
            >>>     expression="diagnose LIKE 'I20%' and age_cd < 40",
            >>>     name='heart attacks rule',
            >>>     description=' heart attacks in people under 40 years of age')

            >>> # r1 -> diagnose LIKE 'I20%' and age_cd < 40


            See Also
            --------
            Rule : A class to represent a rule for a variable or an entity.

            """

        _check_type(expression,str)
        _check_type(name, str)
        _check_type(description, str)

        validate_string_length(expression,'expression',False)
        validate_string_length(name, 'name', False)
        validate_string_length(description, 'description', False)

        self._expression = expression
        self._name = name
        self._description = description
        self._subtype_comparison = None



    @property
    def expression(self):
        return self._expression

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        _check_type(name, str)
        validate_string_length(name, 'name', False)
        self._name = name

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description: str):
        _check_type(description, str)
        validate_string_length(description, 'description', False)
        self._description = description

    @property
    def subtype_comparison(self):
        return  self._subtype_comparison

    def get_structure(self):
        return {
            "expression": self._expression,
            "name": self._name,
            "description": self._description
        }
