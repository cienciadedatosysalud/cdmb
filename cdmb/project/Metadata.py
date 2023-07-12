import re
import uuid

from cdmb.project.Author import Author


def validate_string_length(string: str, max_length: int, arg_name: str):
    if string is not None and len(string) > max_length:
        raise ValueError(f'The argument "{arg_name}" must be less than {max_length} characters.')


class Metadata:
    def __init__(
            self,
            project: str,
            use_case: str,
            version_sem: str = "0.0.1",
            funder: str = None,
            url_project: str = None,
            work_package: str = None,
            document: str = None,
            authors: list[Author] = None,
            keywords: list[str] = None,
            description: str = None,
            notes: str = None,
            spatial_coverage: str = None,
            license: str = "CC BY 4.0 https://creativecommons.org/licenses/by/4.0/deed.es"
    ):
        """Data structure representing the project metadata.

        Examples:
            >>> #Constructing Metadata
            >>> metadata_ = Metadata(
            >>>     project="project_name",
            >>>     url_project="https://my-project.com",
            >>>     work_package="Work_package_name",
            >>>     use_case="use_case_name",
            >>>     version_sem="1.0.0",
            >>>     description="",
            >>>     funder="This project has received funding from the ...",
            >>>     notes="Individual level data is required",
            >>>     keywords=["keyword1", "keyword2"]
            >>>     )

        Parameters
        ----------
        project : str
            Name of the project.
        use_case : str
            Name of the use case or project inside the main project.
        version_sem : str
            Actual version of the Common Data Model. Semantic Versioning 2.0.0 format.
        funder : str
            Funder of the project.
        url_project : str
            Webpage URL related to the project.
        work_package : str
            Work package to which the Common Data Model belongs.
        document : str
            Documentation.
        authors : list[Author]
            List of authors.
        keywords : list[str]
            List of keywords.
        description : str
            Project description.
        notes : str
            Notes.
        spatial_coverage : str
            Spatial coverage of the project.
        license : str
            License of the project.

        See Also
        --------
            Author : A class that represents an author of a scientific publication.
            Semantic : Versioning 2.0.0 format: https://semver.org/.
        Raises
        ------
        ValueError
            If any of the arguments are invalid or out of range.
        TypeError
            If any of the arguments are not of the expected type.

        """

        if authors is not None:
            errmsg = '"authors" argument must be a list of Author'
            if not isinstance(authors, list) or not all([type(author) is Author for author in authors]):
                raise TypeError(errmsg)

        if keywords is not None:
            errmsg = '"keywords" argument must be a list of str'
            if not isinstance(keywords, list) or not all([type(keyword) is str for keyword in keywords]):
                raise TypeError(errmsg)

        regexp = re.compile(
            r'^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$')
        if not regexp.search(version_sem):
            raise ValueError('"version_sem" argument must conform to the Semantic Versioning 2.0.0 format')

        # Check field length

        validate_string_length(project, 250, 'project')
        validate_string_length(url_project, 250, 'url_project')
        validate_string_length(work_package, 250, 'work_package')
        validate_string_length(use_case, 250, 'use_case')
        validate_string_length(document, 250, 'document')
        validate_string_length(funder, 500, 'funder')
        validate_string_length(license, 250, 'license')
        validate_string_length(description, 1000, 'description')
        validate_string_length(notes, 1000, 'notes')
        validate_string_length(spatial_coverage, 250, 'spatial_coverage')

        if keywords is not None and len(keywords) > 10:
            raise ValueError('The maximum number of keywords is 10')

        self._uuid = str(uuid.uuid4())
        self._project = project
        self._funder = funder
        self._url_project = url_project
        self._work_package = work_package
        self._use_case = use_case
        self._document = document
        self._version_sem = version_sem
        self._authors: list[Author] = authors if authors is not None else []
        self._keywords: list[str] = keywords if keywords is not None else []
        self._description = description
        self._notes = notes
        self._spatial_coverage = spatial_coverage
        self._license = license

    @property
    def uuid(self) -> str:
        """

        Returns:
            Universally unique identifier related to the metadata.
        """
        return self._uuid

    @property
    def project(self) -> str:
        """

        Returns:
            Name of the project.
        """
        return self._project

    @property
    def funder(self) -> str:
        """

        Returns:
            Funder of the project.
        """
        return self._funder

    @property
    def url_project(self) -> str:
        """

        Returns:
            URL related to the project.
        """
        return self._url_project

    @property
    def work_package(self) -> str:
        """

        Returns:
            Work Package name.
        """
        return self._work_package

    @property
    def use_case(self) -> str:
        """

        Returns:
            Use Case name.
        """
        return self._use_case

    @property
    def document(self) -> str:
        """

        Returns:
            Metadata document.
        """
        return self._document

    @property
    def version_sem(self) -> str:
        """

        Returns:
            Version of the Common Data Model.
        """
        return self._version_sem

    @property
    def authors(self) -> list[Author]:
        """

        Returns:
            List of authors that make up the project.

        """
        return self._authors

    @property
    def keywords(self) -> list[str]:
        """

        Returns:
            List of keywords.
        """
        return self._keywords

    @property
    def description(self) -> str:
        """

        Returns:
            Description of the project.
        """
        return self._description

    @property
    def notes(self) -> str:
        """

        Returns:
            Notes of the project.
        """
        return self._notes

    @property
    def spatial_coverage(self) -> str:
        """

        Returns:
            Spatial coverage of the project.
        """
        return self._spatial_coverage

    @property
    def license(self) -> str:
        """

        Returns:
            License.
        """
        return self._license

    @project.setter
    def project(self, project: str):
        """

        Args:
            project (String): Name of the project.

        """
        validate_string_length(project, 250, 'project')
        self._project = project

    @funder.setter
    def funder(self, funder: str):
        """

        Args:
            funder (String): Funder of the project.
        """
        validate_string_length(funder, 500, 'funder')
        self._funder = funder

    @url_project.setter
    def url_project(self, url_project: str):
        """

        Args:
            url_project (String): Webpage URL related to the project.
        """
        validate_string_length(url_project, 250, 'url_project')
        self._url_project = url_project

    @work_package.setter
    def work_package(self, work_package: str):
        """

        Args:
             work_package (str): Work package to which the Common Data Model belongs.
.
        """
        validate_string_length(work_package, 250, 'work_package')
        self._work_package = work_package

    @use_case.setter
    def use_case(self, use_case: str):
        """

        Args:
         use_case: String. Name of the use case or project inside the main project.
        """
        validate_string_length(use_case, 250, 'use_case')
        self._use_case = use_case

    @document.setter
    def document(self, document: str):
        """
        Args:
            document (String): Documentation.

        """
        validate_string_length(document, 250, 'document')
        self._document = document

    @version_sem.setter
    def version_sem(self, version_sem: str):
        """

        Args:
            version_sem (String): Actual version of the Common Data Model. Semantic Versioning 2.0.0 format.
        """
        # docs https://semver.org/
        regexp = re.compile(
            r'^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$')
        if not regexp.search(version_sem):
            raise ValueError('"version_sem" argument must conform to the Semantic Versioning 2.0.0 format')

        self._version_sem = version_sem

    @authors.setter
    def authors(self, authors: list[Author]):
        """

        Args:
         authors (list[Author]): List of Author.
        """
        errmsg = '"authors" argument must be a list of Author'
        if not isinstance(authors, list) or not all([isinstance(author, Author) for author in authors]):
            raise TypeError(errmsg)
        self._authors = authors

    def add_author(self, author: Author):
        """

        Args:
            author (Author): Append new Author
        """
        errmsg = '"author" argument must be Author'
        if not isinstance(author, Author):
            raise TypeError(errmsg)
        self._authors.append(author)

    def pop_author(self) -> Author:
        """

        Returns:
         Remove the last author in the list and return it.
        """
        return self._authors.pop()

    @keywords.setter
    def keywords(self, keywords: list[str]):
        """

        Args:
         keywords (list[str]): List of str.

        """
        if keywords is not None:
            errmsg = '"keywords" argument must be a list of str'
            if not isinstance(keywords, list) or not all([type(keyword) is str for keyword in keywords]):
                raise TypeError(errmsg)
        if keywords is not None and len(keywords) > 10:
            raise ValueError('The maximum number of keywords is 10')
        self._keywords = keywords

    @description.setter
    def description(self, description: str):
        """

        Args:
            description (String): String.

        """
        validate_string_length(description, 1000, 'description')
        self._description = description

    @notes.setter
    def notes(self, notes: str):
        """

        Args:
            notes (String): String.

        """
        validate_string_length(notes, 1000, 'notes')
        self._notes = notes

    @spatial_coverage.setter
    def spatial_coverage(self, spatial_coverage: str):
        """

        Args:
         spatial_coverage (String): String.

        """
        validate_string_length(spatial_coverage, 250, 'spatial_coverage')
        self._spatial_coverage = spatial_coverage

    @license.setter
    def license(self, license_: str):
        """

        Args:
            license_ (String): String.

        """
        validate_string_length(license_, 250, 'license')
        self._license = license_

    def get_structure(self) -> dict:
        return {
            "uuid": self._uuid,
            "project": self._project,
            "funder": self._funder,
            "url_project": self._url_project,
            "work_package": self._work_package,
            "use_case": self._use_case,
            "document": self._document,
            "version_sem": self._version_sem,
            "authors": [a.get_structure() for a in self._authors],
            "keywords": self._keywords,
            "description": self._description,
            "notes": self._notes,
            "spatial_coverage": self._spatial_coverage,
            "license": self._license
        }
