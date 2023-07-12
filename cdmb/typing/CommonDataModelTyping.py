from typing import Literal

NatureOptions = Literal["Condition", "Intervention", "Drugs", "Any"]
FormatOptions = Literal["String", "Boolean", "Date", "Datetime", "Integer", "Double"]
TypeOptions = Literal["Categorical", "Date", "Numerical"]
RequirementOptions = Literal["Required", "Recommended", "Optional"]
JoinOptions = Literal["LEFT JOIN", "INNER JOIN", "RIGHT JOIN", "FULL JOIN"]
CharacteristicOptions = Literal["Observed", "Calculated"]
ComparisonOperators = Literal['<', '<=', '>', '>=', '=', '<>', '!=']
BooleanOperators = Literal['and', 'or']


