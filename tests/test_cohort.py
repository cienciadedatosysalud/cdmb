import datetime

# Generated by CodiumAI

import pytest

from cdmb.cohort.Cohort import Cohort
from cdmb.cohort.Crosswalks import Crosswalks
import pandas as pd
"""
Code Analysis

Main functionalities:
The Cohort class represents a cohort study and its main functionalities are to store information about the cohort, such as its name, description, inclusion and exclusion criteria, study period, and crosswalks for inclusion and exclusion definitions. It also provides methods to get and set these fields and to get the structure of the cohort.

Methods:
- __init__: initializes the cohort object with its fields and validates their types and lengths.
- getters and setters: provide access to the fields of the cohort object and validate their types and lengths.
- get_structure: returns a dictionary with the structure of the cohort object, including its fields and the structure of its crosswalks.

Fields:
- name: the name of the cohort.
- description: the description of the cohort.
- inclusion_criteria: the inclusion criteria of the cohort.
- exclusion_criteria: the exclusion criteria of the cohort.
- beggining_study_period: the beginning of the study period.
- end_study_period: the end of the study period.
- cohort_definition_inclusion: the crosswalks for the inclusion definition.
- cohort_definition_exclusion: the crosswalks for the exclusion definition.
"""
class TestCohort:
    #  Tests that a Cohort object can be created with all required arguments
    def test_create_cohort_object_with_all_required_arguments(self):
        cohort = Cohort(
            name='Test Cohort',
            description='Test Description',
            inclusion_criteria='Test Inclusion Criteria',
            beggining_study_period=datetime.date(2021, 1, 1),
            end_study_period=datetime.date(2021, 12, 31)
        )
        assert cohort.name == 'Test Cohort'
        assert cohort.description == 'Test Description'
        assert cohort.inclusion_criteria == 'Test Inclusion Criteria'
        assert cohort.beggining_study_period == datetime.datetime(2021, 1, 1, 0, 0)
        assert cohort.end_study_period == datetime.datetime(2021, 12, 31, 0, 0)
        assert cohort.cohort_definition_inclusion is None
        assert cohort.cohort_definition_exclusion is None

    #  Tests that the name property can be set and retrieved
    def test_set_and_get_name_property(self):
        cohort = Cohort(
            name='Test Cohort',
            description='Test Description',
            inclusion_criteria='Test Inclusion Criteria',
            beggining_study_period=datetime.date(2021, 1, 1),
            end_study_period=datetime.date(2021, 12, 31)
        )
        cohort.name = 'New Test Cohort'
        assert cohort.name == 'New Test Cohort'

    #  Tests that the description property can be set and retrieved
    def test_set_and_get_description_property(self):
        cohort = Cohort(
            name='Test Cohort',
            description='Test Description',
            inclusion_criteria='Test Inclusion Criteria',
            beggining_study_period=datetime.date(2021, 1, 1),
            end_study_period=datetime.date(2021, 12, 31)
        )
        cohort.description = 'New Test Description'
        assert cohort.description == 'New Test Description'

    #  Tests that the inclusion_criteria property can be set and retrieved
    def test_set_and_get_inclusion_criteria_property(self):
        cohort = Cohort(
            name='Test Cohort',
            description='Test Description',
            inclusion_criteria='Test Inclusion Criteria',
            beggining_study_period=datetime.date(2021, 1, 1),
            end_study_period=datetime.date(2021, 12, 31)
        )
        cohort.inclusion_criteria = 'New Test Inclusion Criteria'
        assert cohort.inclusion_criteria == 'New Test Inclusion Criteria'

    #  Tests that the exclusion_criteria property can be set and retrieved
    def test_set_and_get_exclusion_criteria_property(self):
        cohort = Cohort(
            name='Test Cohort',
            description='Test Description',
            inclusion_criteria='Test Inclusion Criteria',
            beggining_study_period=datetime.date(2021, 1, 1),
            end_study_period=datetime.date(2021, 12, 31)
        )
        cohort.exclusion_criteria = 'New Test Exclusion Criteria'
        assert cohort.exclusion_criteria == 'New Test Exclusion Criteria'

    #  Tests that the beggining_study_period property can be set and retrieved
    def test_set_and_get_beggining_study_period_property(self):
        cohort = Cohort(
            name='Test Cohort',
            description='Test Description',
            inclusion_criteria='Test Inclusion Criteria',
            beggining_study_period=datetime.date(2021, 1, 1),
            end_study_period=datetime.date(2021, 12, 31)
        )
        cohort.beggining_study_period = datetime.date(2022, 1, 1)
        assert cohort.beggining_study_period == datetime.datetime(2022, 1, 1, 0, 0)

    #  Tests that the end_study_period property can be set and retrieved
    def test_set_and_get_end_study_period_property(self):
        cohort = Cohort(
            name='Test Cohort',
            description='Test Description',
            inclusion_criteria='Test Inclusion Criteria',
            beggining_study_period=datetime.date(2021, 1, 1),
            end_study_period=datetime.date(2021, 12, 31)
        )
        cohort.end_study_period = datetime.date(2022, 12, 31)
        assert cohort.end_study_period == datetime.datetime(2022, 12, 31, 0, 0)

    #  Tests that the cohort_definition_inclusion property can be set and retrieved
    def test_set_and_get_cohort_definition_inclusion_property(self):
        crosswalks_df = pd.DataFrame({'code': [1, 2, 3], 'name': ['a', 'b', 'c']})
        crosswalks = Crosswalks(
            data=crosswalks_df,
            nature='Condition',
            column_name='code'
        )
        cohort = Cohort(
            name='Test Cohort',
            description='Test Description',
            inclusion_criteria='Test Inclusion Criteria',
            beggining_study_period=datetime.date(2021, 1, 1),
            end_study_period=datetime.date(2021, 12, 31),
            cohort_definition_inclusion=crosswalks
        )
        assert cohort.cohort_definition_inclusion == crosswalks
