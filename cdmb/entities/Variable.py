from cdmb.typing.CommonDataModelTyping import CharacteristicOptions
from cdmb.typing.CommonDataModelTyping import FormatOptions
from cdmb.typing.CommonDataModelTyping import RequirementOptions
from cdmb.typing.CommonDataModelTyping import TypeOptions
from cdmb.entities.Catalog import Catalog


def validate_string_length(string: str, max_length: int, arg_name: str, could_be_null: bool):
    if could_be_null is False and (string is None or string == ""):
        raise ValueError(f'The argument "{arg_name}" cannot be null or an empty string.')
    if string is not None and len(string) > max_length:
        raise ValueError(f'The argument "{arg_name}" must be less than {max_length} characters.')


def _check_type(value, expected_type):
    errmsg = f'"{value}" argument must be {expected_type}'
    if not isinstance(value, expected_type):
        raise TypeError(errmsg)


def validate_string_values(string, values, arg_name):
    if string not in values.__args__:
        raise ValueError('"{arg_name}" argument must must be in {literal_values}.'.format(arg_name=arg_name,
                                                                                          literal_values=values.__args__))


class Variable:
    def __init__(
            self,
            label: str,
            description: str,
            standard_classification: str = "",
            format: FormatOptions = "String",
            type: TypeOptions = "Categorical",
            units: str = "",
            requirement_level: RequirementOptions = "Required",
            characteristic: CharacteristicOptions = "Observed",
            catalog_bl: bool = False,
            transformations_from_origin: str = "",
            possible_data_source: str = "",
            observations_comments: str = "",
            examples: str = "",
            catalog: Catalog = None,

    ):
        """
A class to represent a variable in a data model.

Parameters
----------
    label : str
        The name of the variable, without spaces.
    description : str
        A brief description of the variable's meaning and purpose.
    standard_classification : str, optional
        A reference to a standard classification system for the variable, if any. (default is "")
    format : FormatOptions, optional
        An enumeration value indicating the format of the variable's values, such as String, Integer, Decimal, etc. (default is "String")
    type : TypeOptions, optional
        An enumeration value indicating the type of the variable's values, such as Categorical, Continuous, Ordinal, etc. (default is "Categorical")
    units : str, optional
        The units of measurement for the variable's values, if applicable. (default is "")
    requirement_level : RequirementOptions, optional
        An enumeration value indicating the requirement level of the variable for the data model, such as Required, Optional, Conditional, etc. (default is "Required")
    characteristic : CharacteristicOptions, optional
        An enumeration value indicating the characteristic of the variable for the data model, such as Observed, Derived, Calculated, etc. (default is "Observed")
    catalog_bl : bool, optional
        A flag indicating whether the variable has a catalog of possible values or not. (default is False)
    transformations_from_origin : str, optional
        A description of any transformations applied to the original source of the variable's values, if any. (default is "")
    possible_data_source : str, optional
        A reference to a possible data source for the variable's values, if any. (default is "")
    observations_comments : str, optional
        Any additional observations or comments about the variable. (default is "")
    examples : str, optional
        Some examples of the variable's values. (default is "")
    catalog : Catalog, optional
        A Catalog object containing the possible values and descriptions for the variable, if catalog_bl is True. (default is None)

Raises
------
ValueError
    If any of the arguments are invalid or out of range.
Exception
    If catalog_bl is False but catalog is not None.

Examples
--------
>>> import pandas as pd
>>> df = pd.DataFrame({'sex_cd': ['1', '2'], 'sex_st': ['Male', 'Female']})
>>> catalog_gender = Catalog(df, 'sex_cd', 'gender_catalog.csv')
>>> var1 = Variable("name", "The name of a person", format="String", type="Categorical")
>>> var2 = Variable("age", "The age of a person in years", format="Integer", type="Numerical", units="years")
>>> var3 = Variable("gender", "The gender of a person", format="String", type="Categorical", catalog_bl=True,catalog=catalog_gender)

See Also
--------
FormatOptions : An enumeration class for the possible formats of a variable.
TypeOptions : An enumeration class for the possible types of a variable.
RequirementOptions : An enumeration class for the possible requirement levels of a variable.
CharacteristicOptions : An enumeration class for the possible characteristics of a variable.
Catalog : A class to represent a catalog of possible values and descriptions for a variable.

"""

        validate_string_values(characteristic, CharacteristicOptions, "characteristic")
        validate_string_values(requirement_level, RequirementOptions, "requirement_level")
        validate_string_values(format, FormatOptions, "format")
        validate_string_values(type, TypeOptions, "type")

        if catalog is not None and not isinstance(catalog, Catalog):
            raise ValueError('"catalog" argument must must be a Catalog object')

        if ' ' in label:
            raise ValueError('The label must be a string without spaces. Try changing the spaces to \'_\'')

        # check len
        validate_string_length(label, 50, "label", False)
        validate_string_length(description, 100, "description", False)
        validate_string_length(standard_classification, 100, "standard_classification", True)
        validate_string_length(units, 100, "units", True)
        validate_string_length(transformations_from_origin, 250, "transformations_from_origin", True)
        validate_string_length(possible_data_source, 250, "possible_data_source", True)
        validate_string_length(observations_comments, 500, "observations_comments", True)
        validate_string_length(examples, 250, "examples", True)

        if catalog is not None and isinstance(catalog, Catalog):
            catalog_bl = True
        self._label = label
        self._description = description
        self._standard_classification = standard_classification
        self._format: FormatOptions = format
        self._type: TypeOptions = type
        self._units = units
        self._requirement_level: RequirementOptions = requirement_level
        self._characteristic: CharacteristicOptions = characteristic
        self._catalog_bl = catalog_bl
        self._transformations_from_origin = transformations_from_origin
        self._possible_data_source = possible_data_source
        self._observations_comments = observations_comments
        self._examples = examples
        self._catalog: Catalog = catalog

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label: str):
        validate_string_length(label, 50, "label", False)
        self._label = label

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description: str):
        validate_string_length(description, 100, "description", False)
        self._description = description

    @property
    def standard_classification(self):
        return self._standard_classification

    @standard_classification.setter
    def standard_classification(self, standard_classification: str = ""):
        validate_string_length(standard_classification, 100, "standard_classification", True)
        self._standard_classification = standard_classification

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, format_: FormatOptions):
        validate_string_values(format_, FormatOptions, "format")
        self._format = format_

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type_: TypeOptions):
        validate_string_values(type_, TypeOptions, "type")
        self._type = type_

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, units: str):
        validate_string_length(units, 100, "units", True)
        self._units = units

    @property
    def requirement_level(self):
        return self._requirement_level

    @requirement_level.setter
    def requirement_level(self, requirement_level: RequirementOptions):
        validate_string_values(requirement_level, RequirementOptions, "requirement_level")
        self._requirement_level = requirement_level

    @property
    def characteristic(self):
        return self._characteristic

    @characteristic.setter
    def characteristic(self, characteristic: CharacteristicOptions):
        validate_string_values(characteristic, CharacteristicOptions, "characteristic")
        self._characteristic = characteristic

    @property
    def catalog_bl(self):
        return self._catalog_bl

    @catalog_bl.setter
    def catalog_bl(self, catalog_bl: bool):
        if catalog_bl is False and self.catalog is not None:
            raise Exception("Catalog data is available. Set None the catalog before set false catalog_bl.")
        self._catalog_bl = catalog_bl

    @property
    def transformations_from_origin(self):
        return self._transformations_from_origin

    @transformations_from_origin.setter
    def transformations_from_origin(self, transformations_from_origin: str = ""):
        validate_string_length(transformations_from_origin, 250, "transformations_from_origin", True)
        self._transformations_from_origin = transformations_from_origin

    @property
    def possible_data_source(self):
        return self._possible_data_source

    @possible_data_source.setter
    def possible_data_source(self, possible_data_source: str = ""):
        validate_string_length(possible_data_source, 250, "possible_data_source", True)
        self._possible_data_source = possible_data_source

    @property
    def observations_comments(self):
        return self._observations_comments

    @observations_comments.setter
    def observations_comments(self, observations_comments: str = ""):
        validate_string_length(observations_comments, 500, "observations_comments", True)
        self._observations_comments = observations_comments

    @property
    def examples(self):
        return self._examples

    @examples.setter
    def examples(self, examples: str = ""):
        validate_string_length(examples, 250, "examples", True)
        self._examples = examples

    @property
    def catalog(self):
        return self._catalog

    @catalog.setter
    def catalog(self, catalog: Catalog):
        if catalog is None:
            self._catalog_bl = False
        else:
            self._catalog_bl = True
        self._catalog = catalog

    def get_structure(self):
        return {
            "label": self._label,
            "description": self._description,
            "standard_classification": self._standard_classification,
            "format": self._format,
            "type": self._type,
            "units": self._units,
            "requirement_level": self._requirement_level,
            "characteristic": self._characteristic,
            "catalog_bl": self._catalog_bl,
            "transformations_from_origin": self._transformations_from_origin,
            "possible_data_source": self._possible_data_source,
            "observations_comments": self._observations_comments,
            "examples": self._examples,
            "catalog": None if self._catalog is None else self._catalog.get_structure()
        }
