import re


def validate_name_and_affiliation(name, affiliation):
    if name is not None and len(name) > 250:
        raise ValueError('The argument "name" must be less than 250 characters.')
    if affiliation is not None and len(affiliation) > 250:
        raise ValueError('The argument "affiliation" must be less than 250 characters.')


class Author:
    def __init__(self,
                 name: str,
                 affiliation: str = None,
                 id: str = None):
        """A class that represents an author of a scientific publication.
        Examples:
            >>> # constructing Author
            >>> author1 = Author(name="Surname Name",affiliation="Affiliation name",id="0000-0000-0000-0001")
            >>>
            >>> # add authors to the metadata structure using the add_author function.
            >>> metadata_ = Metadata(...)
            >>> author1 = Author(name="Surname Name",affiliation="Affiliation name",id="0000-0000-0000-0001")
            >>> author2 = Author(name="Surname Name",affiliation="Affiliation name")
            >>> metadata_.add_author(author1)
            >>> metadata_.add_author(author2)
            >>>
            >>> # add authors to the metadata structure by updating the author list.
            >>> metadata_ = Metadata(...)
            >>> author1 = Author(name="Surname Name",affiliation="Affiliation name",id="0000-0000-0000-0001")
            >>> author2 = Author(name="Surname Name",affiliation="Affiliation name")
            >>> metadata_.authors = [author1,author2]


        Parameters
        ----------
        name : str
            Name and surname of the author.
        affiliation : str
            Name of the affiliation to which the author belongs.
        id : str
            ORCID identifier of the author. (e.g., 0000-0000-0000-0000)

        See Also
        --------
        ORCID : https://orcid.org/.

        """
        validate_name_and_affiliation(name, affiliation)
        self._name = name
        self._affiliation = affiliation
        if id is not None and id != "":
            exp1 = re.fullmatch("[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}", id)
            if exp1 is None:
                raise ValueError(
                    'The "id" argument must follow the ORCID identifier format, e.g., 0000-0000-0000-0000.')
        self._id = id

    def __str__(self):
        return f'Name: {self._name}, Affiliation: {self._affiliation}, ID: {self._id}'

    @property
    def name(self) -> str:
        """
        Returns:
             Name and surname of the author
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """
        Args:
         name: Name and surname of the author
        """
        errmsg = '"name" argument must be str'
        if not isinstance(name, str):
            raise TypeError(errmsg)
        if name is not None and len(name) > 250:
            raise ValueError('The argument "name" must be less than 250 characters.')

        self._name = name

    @property
    def affiliation(self):
        """
        Returns: 
            Name of the affiliation to which the author belongs.
        """
        return self._affiliation

    @affiliation.setter
    def affiliation(self, affiliation: str):
        """

        Args:
            affiliation: Name of the affiliation to which the author belongs.
        """
        errmsg = '"affiliation" argument must be str'
        if not isinstance(affiliation, str):
            raise TypeError(errmsg)
        if affiliation is not None and len(affiliation) > 250:
            raise ValueError('The argument "affiliation" must be less than 250 characters.')
        self._affiliation = affiliation

    @property
    def id(self) -> str:
        """
        Returns:
            ORCID identifier of the author or None
        """
        return self._id

    @id.setter
    def id(self, identification: str):
        """

        Args:
            identification: ORCID identifier of the author
        """
        errmsg = '"identification" argument must be str'
        if not isinstance(identification, str):
            raise TypeError(errmsg)

        exp1 = re.fullmatch("[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}", identification)
        if exp1 is None:
            raise ValueError(
                'The "id" argument must follow the ORCID identifier format, e.g., 0000-0000-0000-0000-0000-0000.')

        self._id = identification

    def get_structure(self) -> dict:
        return {
            "name": self._name,
            "affiliation": self._affiliation,
            "id": self._id,
        }
