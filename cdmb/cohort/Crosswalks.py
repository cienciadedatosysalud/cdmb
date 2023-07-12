import re
from typing import Optional

import pandas
import pandas as pd
from pandas import DataFrame

from cdmb.typing.CommonDataModelTyping import NatureOptions


def _check_type(value, expected_type):
    errmsg = f'"{value}" argument must be {expected_type}'
    if not isinstance(value, expected_type):
        raise TypeError(errmsg)


class Crosswalks:

    def __init__(self,
                 data: Optional[DataFrame] = None,
                 column_name: Optional[str] = None,
                 nature: NatureOptions = "Condition",
                 filename: str = "crosswalks.csv",
                 ):
        """
A class to represent crosswalks of possible values and descriptions.

Parameters
----------
    data : DataFrame, optional
        A DataFrame with the crosswalks data. (default is None)
    column_name : str, optional
        The name of the column used as reference. (default is None)
    nature : NatureOptions, optional
        An enumeration value indicating the nature of the variable, such as Condition, Intervention, etc. (default is "Condition")
    filename : str, optional
        The name of the file as the crosswalks will be saved. Only csv extension allowed. (default is "crosswalks.csv")

Raises
------
    ValueError
        If any of the arguments are invalid or out of range.
    TypeError
        If any of the arguments are not of the expected type.
    Exception
        If the filename is not a valid csv file name or the column_name is not in the data columns.

Examples
--------
>>> #Constructing Crosswalks
>>> crosswalks_df = pd.read_csv('crosswalks_definition.csv')
>>> crosswalks_ = Crosswalks(
>>>             data=crosswalks_df,
>>>             nature="Condition",
>>>             column_name="code")

See Also
--------
    NatureOptions : An enumeration class for the possible natures of a variable.

"""

        if data is not None:
            _check_type(data, pandas.DataFrame)

        if column_name is not None:
            _check_type(column_name,str)
            column_name = column_name.strip('\"')
        if filename is not None:
            _check_type(filename, str)

        errmsg = '"nature" argument must must be in {literal_values}.'.format(literal_values=NatureOptions.__args__)
        if nature not in NatureOptions.__args__:
            raise ValueError(errmsg)

        if data is not None:
            if column_name is None:
                raise ValueError("You need to specify a column of the dataframe.")
            else:
                if column_name not in data.columns:
                    raise ValueError("Please specify a column that is present in the dataframe.")
        exp1 = re.fullmatch(".+\.csv$", filename)
        if exp1 is not None:
            self._filename = filename
        else:
            raise Exception("Invalid name for the csv file.")
        self._nature: NatureOptions = nature
        self._column_name = column_name
        self._data: pandas.Dataframe = data

    @property
    def filename(self) -> str:
        return self._filename

    @filename.setter
    def filename(self, filename: str):
        if filename is not None:
            _check_type(filename, str)
        else:
            raise TypeError(f'The argument filename cannot be null.')
        self._filename = filename

    @property
    def nature(self) -> str:
        return self._nature

    @nature.setter
    def nature(self, nature: NatureOptions):
        errmsg = '"nature" argument must must be in {literal_values}.'.format(literal_values=NatureOptions.__args__)
        if nature not in NatureOptions.__args__:
            raise ValueError(errmsg)
        self._nature = nature

    @property
    def column_name(self) -> str:
        return self._column_name

    @column_name.setter
    def column_name(self, column_name: str):
        if column_name is not None:
            _check_type(column_name, str)
            column_name = column_name.strip('\"')
        self._column_name = column_name

    @property
    def data(self) -> pandas.DataFrame:
        return self._data

    @data.setter
    def data(self, data: pandas.DataFrame):
        if data is not None:
            _check_type(data, pandas.DataFrame)
        self._data = data

    def get_header(self) -> list:
        if self._data is not None:
            return self._data.columns
        else:
            return []

    def get_structure(self) -> dict:
        return {
            "filename": self._filename,
            "nature": self._nature,
            "column_name": self._column_name,
        }
