![Logo of the project](https://cienciadedatosysalud.org/wp-content/uploads/logo-Data-Science-VPM.png)

<small><i>This project follows the structure built using the [Common Data Model Builder](https://github.com/cienciadedatosysalud/cdmb), a tool that allows you to create common data models to facilitate interoperability and reproducibility of the analyses.</i></small>


# Your project title

---

# Outputs
Outputs structure and content is described below including the files and folders that are generated when creating a research project with the `cdmb` Python library. There are four main folders corresponding to:

- __docs/CDM/__
  - **cdmb_config.json**: Configuration file.
  - **cohort_definition_inclusion.csv**: csv file that defines the criteria (i.e., codes) for inclusion in a cohort.
  - **cohort_definition_exclusion.csv**: csv file that defines the criteria (i.e., codes) for exclusion in a cohort.
  - **common_datamodel.xlsx**: The definition of the common data model in Excel format.
  - **entities/**: Folder structure where, for each defined entity, the catalogs and the established validation rules are stored.
  - **ER.gv, ER.gv.png**: an Entity-Relationship Diagram of the entities included in the CDM.
  - **synthetic-data/**: Folder structure contaning an automatically generated set of 1000 synthetic records per entity included en the CDM.
  - **hashed_files_list.json**: List of the files generated or used after generating the project with their md5 hash. This file must be kept hidden 
and should be used to cross-check with the results obtained from the analysis from the original input files.
- __inputs/__
  - **data.duckdb**: Database that temporarily contains the data entered by the user (synthetic data by default)
- __outputs/__
  - (Default directory of all the outputs produced in the project execution)
- __src/__
  - __analysis-scripts/__
    - (directory where the analysis scripts developed by the user are stored)
    - **r_report_template.qmd**: Quarto document, with an example analysis, showing the interaction with the folder structure and files generated in the project.
    - **_quarto.yml**: File containing the Metadata to execute Quarto documents.
  - __check_load-scripts/__
    - **check_load.py**: Script in charge of the mapping between the files introduced by the user (./inputs) and map them to the defined entities (inputs/data.duckdb). 
    In the loading process, the following checks are performed: Name of the variables match; the format/type of the variables match those established in the configuration.
    - __inputs/__: Auxiliary folder for the script 'check_load.py'.
  - __dqa-scripts/__
    - **dqa.py**: Data Quality Assesment script by default.
  - **validation-scripts/**
    - **validator.py**: Script in charge of applying the validation rules to the data.
    - **valididator_report.qmd**: Quarto document that generates a report in html from the results obtained from 'validator.py'. 
    - **_quarto.yml**: File containing metadata to execute Quarto documents.
- **ro-crate-metadata.json**: Accessible and practical formal metadata description for use in a wider variety of situations, 
from an individual researcher working with a folder of data, to large data-intensive computational research environments. For more information, visit [RO-Crate](https://www.researchobject.org/ro-crate/).
- **man_container_deployment.md**: From Data Science for Health Services and Policy Research group we provide in the following
  GitHub repository, a solution, for the deployment of the generated project. This step is optional.
- **LICENSE.md**: Project license (CC BY 4.0 by default).


## Requirements/Dependencies 
__*Note that dependencies may vary depending on user modifications!*__

## R dependencies
Version of Rbase used: **4.1**

Version of [Quarto](https://quarto.org/) used: **1.1.149**

| library    | version | link                                                                                    |
|------------|---------|-----------------------------------------------------------------------------------------|
| DuckDB     | 0.8.1   | https://duckdb.org/                                                                     |
| jsonlite   | 1.8.7   | https://cran.r-project.org/web/packages/jsonlite/index.html                             |
| kableExtra | 1.3.4   | https://cran.r-project.org/web/packages/kableExtra/vignettes/awesome_table_in_html.html |
| Hmisc      | 4.7.1   | https://cran.r-project.org/package=Hmisc                                                |

## Python dependencies
Version of Python used: **3.8**

| library         | version | link                                                    |
|-----------------|---------|---------------------------------------------------------|
| pandas          | 1.3.4   | https://pandas.pydata.org/                              |
| DuckDB          | 0.8.1   | https://duckdb.org/                                     |
| ydata_profiling | 4.1.2   | https://ydata-profiling.ydata.ai/docs/master/index.html |


# Authoring

| Surname, name | Affiliation | ![orcid](https://orcid.org/sites/default/files/images/orcid_16x16.png) ORCID |
|---------------|-------------|------------------------------------------------------------------------------|

# Previous version(s):

# How to contribute
- Repository: https://github.com/your_user/your_repository/
- Issue tracker: https://github.com/your_user/your_repository/issues

# References
- Data Science for Health Services and Policy Research group: https://cienciadedatosysalud.org/en/
- Common Data Model Builder library :https://github.com/cienciadedatosysalud/cdmb
- Analytic Software Pipeline Interface for Reproducible Execution (ASPIRE): https://github.com/cienciadedatosysalud/ASPIRE
- Atlas VPM community in Zenodo: https://zenodo.org/communities/atlasvpm
- Research Object Crate (RO-Crate): https://www.researchobject.org/ro-crate/
- ORCID: https://orcid.org/

<a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" ><img src="https://img.shields.io/badge/license-CC--BY%204.0-lightgrey" alt="License: CC-BY 4.0"></a>

