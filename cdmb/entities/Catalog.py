import re
from pandas.core.frame import DataFrame


def _check_type(value, expected_type):
    errmsg = f'"{value}" argument must be {expected_type}'
    if not isinstance(value, expected_type):
        raise TypeError(errmsg)


class Catalog:
    def __init__(self,
                 data: DataFrame,
                 column_name: str,
                 filename: str
                 ):
        """
A class to represent a catalog of possible values and descriptions for a variable.

Parameters
----------
    data : DataFrame
        A DataFrame with the catalog data.
    column_name : str
        The name of the column used as reference.
    filename : str
        The name of the file as the catalog will be saved. Only csv extension allowed.

Raises
------
TypeError
    If any of the arguments are not of the expected type.
Exception
    If the column_name is not in the data columns or the filename is not a valid csv file name.

Examples
--------
>>> # Constructing Catalog
>>> country_catalog_df = pd.read_csv('iso-3166-1_catalog.csv')
>>> catalog_ =  Catalog(country_catalog_df, "Alpha-3_code", "iso-3166-1_catalog.csv")

"""

        _check_type(data, DataFrame)
        _check_type(column_name, str)
        column_name = column_name.strip('\"')
        _check_type(filename, str)
        if column_name not in data.columns:
            raise Exception(
                f'The column "{column_name}" indicated in the catalog ({filename}) provided does not exist.')
        self._column_name = column_name
        pattern = re.compile(".+\.csv$")
        if pattern.match(filename):
            self._filename = filename
        else:
            raise Exception("Invalid name for the csv file.")
        self._data = data

    @property
    def column_name(self) -> str:
        return self._column_name

    @column_name.setter
    def column_name(self, column_name: str):
        _check_type(column_name, str)
        self._column_name = column_name

    @property
    def filename(self) -> str:
        return self._filename

    @filename.setter
    def filename(self, filename: str):
        _check_type(filename, str)
        exp1 = re.search(".+\.csv$", filename)
        if exp1 is not None:
            self._filename = filename
        else:
            raise Exception("Invalid name for the csv file.")

    @property
    def data(self) -> DataFrame:
        return self._data

    @data.setter
    def data(self, data: DataFrame):
        _check_type(data, DataFrame)
        self._data = data

    def get_header(self):
        if self._data is not None:
            return self._data.columns
        else:
            return []

    def get_catalog(self):
        return {'filename': self._filename, 'column_name': self._column_name, 'data': self._data}

    def get_structure(self):
        return {
            "column_name": self._column_name,
            "filename": self._filename
        }
