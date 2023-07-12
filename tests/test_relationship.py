
# Generated by CodiumAI

import pytest

from cdmb.entities.Entity import Entity
from cdmb.entities.Variable import Variable
from cdmb.relationships.Relationship import Relationship

"""
Code Analysis

Main functionalities:
The Relationship class represents the relationship between two entities (Entity) and provides functionalities to establish and update the relationship. It allows the user to specify the left and right entities, the left and right columns, and the type of join. It also provides methods to get the structure of the relationship and to update the left and right entities, columns, and join type.

Methods:
- __init__: Initializes the Relationship object with the left and right entities, left and right columns, and join type.
- get_structure: Returns a dictionary with the structure of the relationship.
- left_entity, right_entity, join_type, left_column, right_column: Getter and setter methods for the corresponding fields.

Fields:
- _left_entity: The left entity of the relationship.
- _right_entity: The right entity of the relationship.
- _join_type: The type of join between the two entities.
- _left_column: The left column of the relationship.
- _right_column: The right column of the relationship.
"""
class TestRelationship:
    #  Tests that a Relationship object can be created with valid arguments
    def test_create_relationship_valid_args(self):
        left_entity_ = Entity("entity1")
        left_column_ = Variable("person_id","person pseudonymized identificator")
        left_entity_.add_variable(left_column_)
        right_entity_ = Entity("entity2")
        right_column_ = Variable("patient_id","patient pseudonymized identificator")
        right_entity_.add_variable(right_column_)
        first_relationship = Relationship(left_entity_,right_entity_,left_column_,right_column_,"INNER JOIN")
        assert first_relationship.left_entity == left_entity_
        assert first_relationship.right_entity == right_entity_
        assert first_relationship.left_column == left_column_
        assert first_relationship.right_column == right_column_
        assert first_relationship.join_type == "INNER JOIN"

    #  Tests that the left_entity property can be accessed
    def test_get_left_entity(self):
        left_entity_ = Entity("entity1")
        left_column_ = Variable("person_id","person pseudonymized identificator")
        left_entity_.add_variable(left_column_)
        right_entity_ = Entity("entity2")
        right_column_ = Variable("patient_id","patient pseudonymized identificator")
        right_entity_.add_variable(right_column_)
        first_relationship = Relationship(left_entity_,right_entity_,left_column_,right_column_,"INNER JOIN")
        assert first_relationship.left_entity == left_entity_

    #  Tests that the right_entity property can be accessed
    def test_get_right_entity(self):
        left_entity_ = Entity("entity1")
        left_column_ = Variable("person_id","person pseudonymized identificator")
        left_entity_.add_variable(left_column_)
        right_entity_ = Entity("entity2")
        right_column_ = Variable("patient_id","patient pseudonymized identificator")
        right_entity_.add_variable(right_column_)
        first_relationship = Relationship(left_entity_,right_entity_,left_column_,right_column_,"INNER JOIN")
        assert first_relationship.right_entity == right_entity_

    #  Tests that the join_type property can be accessed
    def test_get_join_type(self):
        left_entity_ = Entity("entity1")
        left_column_ = Variable("person_id","person pseudonymized identificator")
        left_entity_.add_variable(left_column_)
        right_entity_ = Entity("entity2")
        right_column_ = Variable("patient_id","patient pseudonymized identificator")
        right_entity_.add_variable(right_column_)
        first_relationship = Relationship(left_entity_,right_entity_,left_column_,right_column_,"INNER JOIN")
        assert first_relationship.join_type == "INNER JOIN"

    #  Tests that the left_column property can be accessed
    def test_get_left_column(self):
        left_entity_ = Entity("entity1")
        left_column_ = Variable("person_id","person pseudonymized identificator")
        left_entity_.add_variable(left_column_)
        right_entity_ = Entity("entity2")
        right_column_ = Variable("patient_id","patient pseudonymized identificator")
        right_entity_.add_variable(right_column_)
        first_relationship = Relationship(left_entity_,right_entity_,left_column_,right_column_,"INNER JOIN")
        assert first_relationship.left_column == left_column_

    #  Tests that the right_column property can be accessed
    def test_get_right_column(self):
        left_entity_ = Entity("entity1")
        left_column_ = Variable("person_id","person pseudonymized identificator")
        left_entity_.add_variable(left_column_)
        right_entity_ = Entity("entity2")
        right_column_ = Variable("patient_id","patient pseudonymized identificator")
        right_entity_.add_variable(right_column_)
        first_relationship = Relationship(left_entity_,right_entity_,left_column_,right_column_,"INNER JOIN")
        assert first_relationship.right_column == right_column_

    #  Tests that a Relationship object cannot be created with an invalid left_entity argument
    def test_create_relationship_invalid_left_entity(self):
        with pytest.raises(TypeError):
            Relationship("entity1",Entity("entity2"),Variable("person_id","person pseudonymized identificator"),Variable("patient_id","patient pseudonymized identificator"),"INNER JOIN")

    #  Tests that a Relationship object cannot be created with an invalid right_entity argument
    def test_create_relationship_invalid_right_entity(self):
        with pytest.raises(TypeError):
            Relationship(Entity("entity1"),"entity2",Variable("person_id","person pseudonymized identificator"),Variable("patient_id","patient pseudonymized identificator"),"INNER JOIN")

    #  Tests that a Relationship object cannot be created with an invalid left_column argument
    def test_create_relationship_invalid_left_column(self):
        left_entity_ = Entity("entity1")
        right_entity_ = Entity("entity2")
        with pytest.raises(TypeError):
            Relationship(left_entity_,right_entity_,"person_id",Variable("patient_id","patient pseudonymized identificator"),"INNER JOIN")
