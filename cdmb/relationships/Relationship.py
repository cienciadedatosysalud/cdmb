from cdmb.typing.CommonDataModelTyping import JoinOptions
from cdmb.entities.Entity import Entity
from cdmb.entities.Variable import Variable


class Relationship:
    def __init__(self,
                 left_entity: Entity,
                 right_entity: Entity,
                 left_column: Variable,
                 right_column: Variable,
                 join_type: JoinOptions = "LEFT JOIN"):
        """Initializes a Relationship object with the given parameters.

        Parameters
        ----------
        left_entity : Entity
            The entity representing the left-hand side of the relationship.
        right_entity : Entity
            The entity representing the right-hand side of the relationship.
        left_column : Variable
            The variable on the left entity by which the join is made.
        right_column : Variable
            The variable on the right entity by which the join is made.
        join_type : JoinOptions
            The type of join between the two entities, such as "LEFT JOIN" or "INNER JOIN". Defaults to "LEFT JOIN".

        Raises
        ------
        TypeError
            If any of the arguments are not of the expected type.
        ValueError
            If any of the arguments are not valid, such as a join type that is not supported, or a column that is not part of its entity.

        Examples
        --------
        >>> # Constructing Catalog
        >>> main_entity = Entity(
        >>> name='Admission',
        >>> time_varying=False,
        >>> variables=[
        >>>     Variable('patient_id', "Patient's pseudonymized id"),
        >>>     Variable('service_cd', "Service's code")
        >>> ])
        >>> services_entity = Entity(
        >>>         name='Service',
        >>>         time_varying=False,
        >>>         variables=[
        >>>             Variable('code', "Service's code"),
        >>>             Variable('description', "Service's description")
        >>>         ])

        >>> relationship = Relationship(
        >>>     left_entity = main_entity,
        >>>     right_entity = services_entity,
        >>>     left_column =  Variable('service_cd', "Service's code"),
        >>>     right_column = Variable('code', "Service's code"),
        >>>     join_type= "LEFT JOIN" # Join Options -> ["LEFT JOIN", "INNER JOIN", "RIGHT JOIN", "FULL JOIN"]
        >>> )
        """

        join_type = str(join_type).upper()
        if type(left_entity) is not Entity:
            raise TypeError('"left_entity" argument must be Entity')

        if type(right_entity) is not Entity:
            raise TypeError('"right_entity" argument must be Entity')

        if type(left_column) is not Variable:
            raise TypeError('"left_column" argument must be Variable')

        if type(right_column) is not Variable:
            raise TypeError('"right_column" argument must be Variable')

        if join_type not in JoinOptions.__args__:
            raise ValueError('join_type must be in {literal_values}'.format(literal_values=JoinOptions.__args__))

        column_ = left_entity.get_variable_by_label(left_column.label)
        if column_ is None:
            raise ValueError('"left_column" variable has to be part of its entity ("left_entity")')

        column_ = right_entity.get_variable_by_label(right_column.label)
        if column_ is None:
            raise ValueError('"right_column" variable has to be part of its entity ("right_entity")')

        self._left_entity = left_entity
        self._right_entity = right_entity
        self._join_type = join_type
        self._left_column = left_column
        self._right_column = right_column

    @property
    def left_entity(self) -> Entity:
        return self._left_entity

    @left_entity.setter
    def left_entity(self, left_entity: Entity):
        if type(left_entity) is not Entity:
            raise TypeError('"left_entity" argument must be Entity')
        self._left_entity = left_entity

    @property
    def right_entity(self) -> Entity:
        return self._right_entity

    @right_entity.setter
    def right_entity(self, right_entity: Entity):
        if type(right_entity) is not Entity:
            raise TypeError('"right_entity" argument must be Entity')
        self._right_entity = right_entity

    @property
    def join_type(self) -> str:
        return self._join_type

    @join_type.setter
    def join_type(self, join_type: str):
        if join_type not in JoinOptions.__args__:
            raise ValueError('join_type must be in {literal_values}'.format(literal_values=JoinOptions.__args__))
        self._join_type = join_type

    @property
    def left_column(self) -> Variable:
        return self._left_column

    @left_column.setter
    def left_column(self, left_column: Variable):
        if type(left_column) is not Variable:
            raise TypeError('"left_column" argument must be Variable')
        column_ = self._left_entity.get_variable_by_label(left_column.label)
        if column_ is None:
            raise ValueError('"left_column" variable has to be part of its entity ("left_entity")')
        self._left_column = left_column

    @property
    def right_column(self) -> Variable:
        return self._right_column

    @right_column.setter
    def right_column(self, right_column: Variable):
        if type(right_column) is not Variable:
            raise TypeError('"right_column" argument must be Variable')
        column_ = self._right_entity.get_variable_by_label(right_column.label)
        if column_ is None:
            raise ValueError('"right_column" variable has to be part of its entity ("right_entity")')
        self._right_column = right_column

    def get_structure(self) -> dict:
        return {
            "left_entity": self._left_entity.name,
            "right_entity": self._right_entity.name,
            "join_type": self._join_type,
            "left_column": self._left_column.label,
            "right_column": self._right_column.label
        }
