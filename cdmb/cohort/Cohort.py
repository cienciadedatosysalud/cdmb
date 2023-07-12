import datetime
from datetime import date, datetime
from typing import Optional

from cdmb.cohort.Crosswalks import Crosswalks


def validate_string_length(string: str, max_length: int, arg_name: str, could_be_null:bool):
    if could_be_null is False and (string is None or string == ""):
        raise ValueError(f'The argument "{arg_name}" cannot be null or an empty string.')
    if string is not None and len(string) > max_length:
        raise ValueError(f'The argument "{arg_name}" must be less than {max_length} characters.')


def _check_type(value, expected_type):
    errmsg = f'"{value}" argument must be {expected_type}'
    if not isinstance(value, expected_type):
        raise TypeError(errmsg)


class Cohort:
    def __init__(
            self,
            name: str,
            description: str,
            inclusion_criteria: str,
            exclusion_criteria: Optional[str] = None,
            beggining_study_period: date = date.today(),
            end_study_period: date = date.today(),
            cohort_definition_inclusion: Crosswalks = None,
            cohort_definition_exclusion: Crosswalks = None
    ):
        """A class to represent a cohort in a data model.

    Parameters
    ----------
        name : str
            The name of the cohort, without spaces.
        description : str
            A brief description of the cohort's meaning and purpose. PICO(T) format preferred.
        inclusion_criteria : str
            The inclusion criteria definition of the cohort.
        exclusion_criteria : str, optional
            The exclusion criteria definition of the cohort. (default is None)
        beggining_study_period : date, optional
            The start date of the study period. (default is today)
        end_study_period : date, optional
            The end date of the study period. (default is today)
        cohort_definition_inclusion : Crosswalks, optional
            A Crosswalks object containing the crosswalks defining the cohort inclusions. (default is None)
        cohort_definition_exclusion : Crosswalks, optional
            A Crosswalks object containing the crosswalks defining the cohort exclusions. (default is None)

    Raises
    ------
        ValueError
            If any of the arguments are invalid or out of range.
        TypeError
            If any of the arguments are not of the expected type.
        Exception
            If cohort_definition_X is not None but cohort_definition_X is a Crosswalks.

    Examples
    --------
    >>> # Constructing Cohort
    >>> import pandas as pd
    >>> cohort_ = Cohort(
    >>>     name="Cohort name",
    >>>     description="Patients with comorbidity X",
    >>>     inclusion_criteria="patients that, at 01/01/2000 or during the follow-up from 01/01/2000 had active health card",
    >>>     exclusion_criteria="patients with no contact with the health system from 01/01/2015 to 31/12/2022",
    >>>     beggining_study_period=date(2000, 1, 1),
    >>>     end_study_period=date(2022, 12, 31),
    >>>     )

    See Also
    --------
        Crosswalks : A class to represent a crosswalks of possible values and descriptions for a variable.
"""

        if not isinstance(beggining_study_period, date):
            raise TypeError('"beggining_study_period" argument must be date')

        if not isinstance(end_study_period, date):
            raise TypeError('"end_study_period" argument must be date')

        if cohort_definition_inclusion is not None and type(cohort_definition_inclusion) is not Crosswalks:
            raise TypeError('"cohort_definition_inclusion" argument must be Crosswalks')

        if cohort_definition_exclusion is not None and type(cohort_definition_exclusion) is not Crosswalks:
            raise TypeError('"cohort_definition_exclusion" argument must be Crosswalks')

        # check len
        validate_string_length(name, 250, 'name', False)
        validate_string_length(description, 1000, 'description',False)
        validate_string_length(inclusion_criteria, 500, 'inclusion_criteria',False)
        validate_string_length(exclusion_criteria, 500, 'exclusion_criteria',True)

        self._name = name
        self._description = description
        self._inclusion_criteria = inclusion_criteria
        self._exclusion_criteria = exclusion_criteria
        self._beggining_study_period = beggining_study_period.strftime("%Y-%m-%d")
        self._end_study_period = end_study_period.strftime("%Y-%m-%d")
        self._cohort_definition_inclusion: Crosswalks = cohort_definition_inclusion
        self._cohort_definition_exclusion: Crosswalks = cohort_definition_exclusion

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        _check_type(name, str)
        validate_string_length(name, 250, 'name', False)
        self._name = name

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description: str):
        _check_type(description, str)
        validate_string_length(description, 1000, 'description',False)
        self._description = description

    @property
    def inclusion_criteria(self) -> str:
        return self._inclusion_criteria

    @inclusion_criteria.setter
    def inclusion_criteria(self, inclusion_criteria: str):
        _check_type(inclusion_criteria, str)
        validate_string_length(inclusion_criteria, 500, 'inclusion_criteria',False)
        self._inclusion_criteria = inclusion_criteria

    @property
    def exclusion_criteria(self) -> str:
        return self._exclusion_criteria

    @exclusion_criteria.setter
    def exclusion_criteria(self, exclusion_criteria: str):
        _check_type(exclusion_criteria, str)
        validate_string_length(exclusion_criteria, 500, 'exclusion_criteria',True)
        self._exclusion_criteria = exclusion_criteria

    @property
    def beggining_study_period(self) -> datetime:
        return datetime.strptime(self._beggining_study_period, "%Y-%m-%d")

    @beggining_study_period.setter
    def beggining_study_period(self, beggining_study_period: date):
        errmsg = '"beggining_study_period" argument must be date'
        if not isinstance(beggining_study_period, date):
            raise TypeError(errmsg)

        self._beggining_study_period = beggining_study_period.strftime("%Y-%m-%d")

    @property
    def end_study_period(self) -> datetime:
        return datetime.strptime(self._end_study_period, "%Y-%m-%d")

    @end_study_period.setter
    def end_study_period(self, end_study_period: date):
        errmsg = '"end_study_period" argument must be date type'
        if not isinstance(end_study_period, date):
            raise TypeError(errmsg)
        self._end_study_period = end_study_period.strftime("%Y-%m-%d")

    @property
    def cohort_definition_inclusion(self) -> Crosswalks:
        return self._cohort_definition_inclusion

    @cohort_definition_inclusion.setter
    def cohort_definition_inclusion(self, cohort_definition_inclusion: Crosswalks):
        errmsg = '"cohort_definition_inclusion" argument must be Crosswalks type'
        if not isinstance(cohort_definition_inclusion, Crosswalks):
            raise TypeError(errmsg)
        self._cohort_definition_inclusion = cohort_definition_inclusion

    @property
    def cohort_definition_exclusion(self) -> Crosswalks:
        return self._cohort_definition_exclusion

    @cohort_definition_exclusion.setter
    def cohort_definition_exclusion(self, cohort_definition_exclusion: Crosswalks):
        errmsg = '"cohort_definition_exclusion" argument must be Crosswalks'
        if not isinstance(cohort_definition_exclusion, Crosswalks):
            raise TypeError(errmsg)
        self._cohort_definition_exclusion = cohort_definition_exclusion

    def get_structure(self) -> dict:
        return {
            "name": self._name,
            "description": self._description,
            "inclusion_criteria": self._inclusion_criteria,
            "exclusion_criteria": self._exclusion_criteria,
            "beggining_study_period": self._beggining_study_period,
            "end_study_period": self._end_study_period,
            "cohort_definition_inclusion": None if self._cohort_definition_inclusion is None else self._cohort_definition_inclusion.get_structure(),
            "cohort_definition_exclusion": None if self._cohort_definition_exclusion is None else self._cohort_definition_exclusion.get_structure()
        }
