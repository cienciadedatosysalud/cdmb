from typing import Literal

NatureOptions = Literal["Condition", "Intervention", "Drugs", "Any"]
FormatOptions = Literal["String", "Boolean", "Date", "Datetime", "Integer", "Double"]
TypeOptions = Literal["Categorical", "Date", "Numerical"]
RequirementOptions = Literal["Required", "Recommended", "Optional"]
JoinOptions = Literal["LEFT JOIN", "INNER JOIN", "RIGHT JOIN", "FULL JOIN"]
CharacteristicOptions = Literal["Observed", "Calculated"]
ComparisonOperators = Literal['<', '<=', '>', '>=', '=', '<>', '!=']
BooleanOperators = Literal['and', 'or']
DuckDBReservedWords = Literal[
"ALL", "ALTER", "AND", "ANY", "AS", "ASC", "BETWEEN", "BIGINT", "BINARY", "BLOB", "BOOLEAN", "BY", "CASE", "CAST",
"CHAR", "CHARACTER", "CHECK", "COLUMN", "CONSTRAINT", "CREATE", "CROSS", "CURRENT_DATE", "CURRENT_TIME",
"CURRENT_TIMESTAMP", "DATABASE", "DATE", "DECIMAL", "DEFAULT", "DELETE", "DESC", "DISTINCT", "DOUBLE", "DROP",
"ELSE", "END", "ESCAPE", "EXISTS", "EXTRACT", "FALSE", "FLOAT", "FOR", "FOREIGN", "FROM", "FULL", "GROUP", "HAVING",
"IF", "ILIKE", "IN", "INNER", "INSERT", "INTEGER", "INTERSECT", "INTERVAL", "INTO", "IS", "JOIN", "LEFT", "LIKE",
"LIMIT", "NATURAL", "NOT", "NULL", "NUMERIC", "ON", "OR", "ORDER", "OUTER", "PRIMARY", "REFERENCES", "RIGHT",
"SELECT", "SET", "SMALLINT", "TABLE", "THEN", "TIME", "TIMESTAMP", "TRUE", "UNION", "UNIQUE", "UPDATE", "USING",
"VALUES", "VARCHAR", "WHEN", "WHERE"
]

