![Logo of the project](https://cienciadedatosysalud.org/wp-content/uploads/logo-Data-Science-VPM.png)
- [Common Data Model Builder (cdmb)](#common-data-model-builder-cdmb)
- [User Interface](#user-interface)
- [Outputs](#outputs)
- [Classes](#classes)
  - [Metadata](#metadata)
  - [Author](#author)
  - [Cohort](#cohort)
  - [Crosswalks](#crosswalks)
  - [Entities](#entities)
  - [Variables](#variables)
  - [Catalogs](#catalogs)
  - [Rules Set](#rules-set)
  - [Rules](#rules)
  - [Comparison rule](#comparison-rule)
  - [BetweenComparison](#betweencomparison)
  - [NullCheckingRule](#nullcheckingrule)
  - [InValuesRule](#invaluesrule)
  - [ComposedRule](#composedrule)
  - [DummyRule](#dummyrule)
  - [Relationships](#relationships)
  - [Common Data Model](#common-data-model)
- [Data types](#data-types)
- [Outputs](#outputs)
- [Authoring](#authoring)
- [How to contribute](#how-to-contribute)
- [References](#references)


<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

# Common Data Model Builder (cdmb)

The Common Data Model Builder (cdmb) is a Python library that facilitates building data models for projects with a defined structure. The library offers two ways to generate data models: using code or using a graphical interface. The library facilitates  completing the project's metadata, including the cohort's definition, the entities and the validation rules of the data model. The cdmb assists a user in systematically generating a reproducible folder structure of the research project as a Research Object (RO) easily implemented in as part of a deployable workflow.

# User Interface
#### Main functionalities:
One of the functionalities of Common Data Model Builder is to provide the user with a graphical interface to fill in the Common Data Model and export it in a simple way. Follow the following code snippet to access it.
#### Inputs:
- **server_address**: a string representing the server address, default value is "localhost"
- **port**: a string representing the server port, default value is "8501"

#### Example:
```python
from cdmb import launch_ui

server_address = "localhost"
port = 8000

launch_ui(server_address, port)
# Open your web browser at http://<server_address>:<port>.
# http://localhost:8000
```

# Run in Docker
Alternatively you can run the graphical interface provided by the Common Data Model Builder directly in a docker container.

Use the following code snippet to create the container.
```bash
docker pull ghcr.io/cienciadedatosysalud/cdmb:latest

docker run -p 127.0.0.1:8501:8501 --name cdmb_ui ghcr.io/cienciadedatosysalud/cdmb:latest

# Open your web browser at http://localhost:8501.
```


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

# Classes

## Metadata
#### Main functionalities:
The Metadata class is designed to store and manage metadata information for a research project. It allows for the storage of project information such as project name, version, authors, keywords, description, notes, spatial coverage, and license. The class also provides methods for adding and removing authors, setting and getting values for the various fields, and returning the metadata structure as a dictionary.

#### Methods:
- `__init__`: Initializes the Metadata object with the given project, use case, version, funder, url_project, work_package, document, authors, keywords, description, notes, spatial_coverage, and license.
- `add_author`: Adds an Author object to the list of authors.
- `pop_author`: Removes and returns the last Author object from the list of authors.
- `get_structure`: Returns the metadata structure as a dictionary.
- Various `setter` methods: Set the values of the corresponding fields.
- Various `getter` methods: Return the values of the corresponding fields.

#### Fields:
- uuid: A unique identifier for the Metadata object (_automatycally generated_).
- project: The name of the project.
- funder: The name of the funder of the project.
- url_project: The URL of the project.
- work_package: The name of the work package.
- use_case: The name of the use case.
- document: The name of the document.
- version_sem: The semantic version of the project.
- authors: A list of Author objects.
- keywords: A list of keywords associated with the project.
- description: A description of the project.
- notes: Additional notes about the project.
- spatial_coverage: The spatial coverage of the project.
- license: The license of the project.

#### Example:
```python
from cdmb import Metadata

metadata = Metadata(project='Test Project', use_case='Use Case')
```

## Author
#### Main functionalities:
The Author class represents the information associated with the author(s), including their name, affiliation, and ORCID identifier. It provides methods to set and get these attributes, as well as a method to retrieve the author's information as a dictionary.

#### Methods:
- `__init__`: initializes the Author object with the provided name, affiliation, and ORCID identifier
- name, affiliation, id getters and setters: allow getting and setting the name, affiliation, and ORCID identifier attributes of the Author object
- `get_structure`: returns the Author object's attributes as a dictionary

#### Fields:
- **name**: the name of the author
- **affiliation**: the affiliation of the author
- **id**: the ORCID identifier of the author

#### Example:
```python
from cdmb import Author
from cdmb import Metadata

author = Author(
        name='John Doe', 
        affiliation='University of California', 
        id='0000-0000-0000-0001'
      )

metadata = Metadata(project='Test Project', use_case='Use Case')
metadata.add_author(author)
```


## Cohort
#### Main functionalities:
The Cohort class represents a cohort study and its main functionalities are to store information about the cohort, such as its name, description, inclusion and exclusion criteria, study period, and crosswalks for inclusion and exclusion definitions. It also provides methods to get and set these fields and to get the structure of the cohort.

#### Methods:
- `__init__`: initializes the cohort object with its fields and validates their types and lengths.
- `getters` and `setters`: provide access to the fields of the cohort object and validate their types and lengths.
- `get_structure`: returns a dictionary with the structure of the cohort object, including its fields and the structure of its crosswalks.

#### Fields:
- **name**: the name of the cohort.
- **description**: the description of the cohort.
- **inclusion_criteria**: the inclusion criteria of the cohort.
- **exclusion_criteria**: the exclusion criteria of the cohort.
- **beggining_study_period**: the beginning of the study period.
- **end_study_period**: the end of the study period.
- **cohort_definition_inclusion**: the crosswalks for the inclusion definition.
- **cohort_definition_exclusion**: the crosswalks for the exclusion definition.

#### Example:
```python
from cdmb import Cohort
import datetime

cohort = Cohort(
        name='Cohort name',
        description='Cohort description',
        inclusion_criteria='Inclusion criteria text',
        beggining_study_period=datetime.date(2021, 1, 1),
        end_study_period=datetime.date(2021, 12, 31)
    )
```

## Crosswalks
#### Main functionalities:
The Crosswalks class is a data structure that represents crosswalks. It allows the user to specify a pandas DataFrame, a column name, a nature, and a filename. The class provides methods to get and set the filename, nature, column name, and data. It also provides methods to get the header and structure of the crosswalks.

#### Methods:
- `__init__`: initializes the class with optional parameters data, column_name, nature, and filename.
- `get_header`: returns the column labels of data.
- `get_structure`: returns a dictionary with the filename, nature, and column_name.
- `filename.setter`: sets the filename.
- `nature.setter`: sets the nature.
- `column_name.setter`: sets the column name.
- `data.setter`: sets the data.

#### Fields:
- **filename**: the name of the file as the crosswalks will be saved.
- **nature**: the nature of the crosswalks.
- **column_name**: the name of the column used as reference.
- **data**: the crosswalks as a pandas DataFrame.

#### Example:
```python
import pandas
from cdmb import Crosswalks
from cdmb import Cohort
import datetime

crosswalks_df = pandas.DataFrame({
                    'code': ['A1', 'A2', 'A3'], 
                    'name': ['Condition 1', 'Condition 2', 'Condition 3']
                    })
                    
crosswalks = Crosswalks(
                data=crosswalks_df, 
                column_name='code', 
                nature='Condition', 
                filename='crosswalks.csv'
                )
                
cohort = Cohort(
            name='Cohort name',
            description='Cohort description',
            inclusion_criteria='Inclusion criteria text',
            beggining_study_period=datetime.date(2021, 1, 1),
            end_study_period=datetime.date(2021, 12, 31),
            cohort_definition_inclusion=crosswalks
        )
```

## Entities
#### Main functionalities:
The Entity class represents an entity in a data model and contains information about its variables and rules. It allows for the addition and removal of variables, as well as the creation of rules from expressions. It also provides methods for getting the structure of the entity, its variables, and its rules, as well as for getting catalogs associated with its variables.

#### Methods:
- `__init__`: initializes the Entity object with a name, time_varying flag, list of variables, and RuleSet object
- `add_variable`: adds a Variable object to the list of variables
- `pop_variable`: removes and returns the last Variable object in the list of variables
- `get_variable_by_label`: returns the Variable object with the given label
- `get_catalogs`: returns a tuple of dictionaries containing information about catalogs associated with the entity's variables
- `get_rules_synthetic`: returns a list of rules for generating synthetic data
- `dict_to_variables`: converts a list of dictionaries to Variable objects and adds them to the list of variables
- `get_rules_structure`: returns a dictionary containing information about the entity's rules
- `get_structure`: returns a dictionary containing information about the entity's structure
- `get_variables_in_order`: returns a list of variables in the order specified by the input Variable object
- `get_tree_structure_rules`: returns a Tree object representing the dependencies between the entity's variables based on its rules
- `create_rule_from_expression`: creates a Rule object from a string expression

#### Fields:
- **uuid**: a unique identifier for the entity (_automatycally generated_)
- **name**: the name of the entity
- **time_varying**: a boolean flag indicating whether the entity is time-varying
- **variables**: a list of Variable objects associated with the entity
- **rules**: a RuleSet object containing the rules associated with the entity
#### Example:
```python
from cdmb import Entity

entity = Entity('Entity_name', time_varying=True)
```

## Variables
#### Main functionalities:
The Variable class represents a variable in a dataset and contains information about its label, description, format, type, units, requirement level, characteristic, catalog, and other metadata. It allows for setting and getting these attributes and provides methods for getting the structure of the variable.

#### Methods:
- `__init__`: initializes a Variable object with the given attributes
- `get_structure`: returns a dictionary with the structure of the variable
- `getters` and `setters` for each attribute: allows for getting and setting each attribute of the variable

#### Fields:
- **label**: the label of the variable
- **description**: the description of the variable
- **standard_classification**: the standard classification of the variable
- **format**: the format of the variable
- **type**: the type of the variable
- **units**: the units of the variable
- **requirement_level**: the requirement level of the variable
- **characteristic**: the characteristic of the variable
- **catalog_bl**: a boolean indicating whether the variable has a catalog
- **transformations_from_origin**: the transformations applied to the variable from its origin
- **possible_data_source**: the possible data sources for the variable
- **observations_comments**: comments about the observations of the variable
- **examples**: examples of the variable
- **catalog**: the catalog of the variable, if it has one

#### Example:
```python
from cdmb import Entity
from cdmb import Variable

entity = Entity('Entity_name', time_varying=True)

var = Variable(
            label='label',
            description='description',
            standard_classification='standard classification',
            format='String',
            type='Categorical',
            units='units',
            requirement_level='Required',
            characteristic='Observed',
            catalog_bl=False,
            transformations_from_origin='transformations from origin',
            possible_data_source='possible data source',
            observations_comments='observations comments',
            examples='test examples',
            catalog=None
        )

entity.add_variable(var)
```


## Catalogs
#### Main functionalities:
The Catalog class is a data structure that represents a catalog. It takes a pandas DataFrame, a column name, and a filename as input and provides methods to get and set the column name, filename, and data. It also provides methods to get the header, catalog, and structure of the catalog.

#### Methods:
- `__init__`: Initializes the Catalog class with a DataFrame, column name, and filename.
- `get_header`: Returns the header of the catalog.
- `get_catalog`: Returns a dictionary with the filename, column name, and data of the catalog.
- `get_structure`: Returns a dictionary with the column name and filename of the catalog.
- `column_name`: Getter and setter for the column name field.
- `filename`: Getter and setter for the filename field.
- `data`: Getter and setter for the data field.

#### Fields:
- **column_name**: Name of the column used as reference.
- **filename**: Name of the file as the catalog will be saved.
- **data**: DataFrame with the catalog data.

#### Example:
```python
from cdmb import Entity
from cdmb import Variable
from cdmb import Catalog
import pandas as pd 

df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
catalog = Catalog(df, 'A', 'test.csv')

entity = Entity('Entity_name', time_varying=True)
var = Variable(
            label='label',
            description='description',
            standard_classification='standard classification',
            format='String',
            type='Categorical',
            units='units',
            requirement_level='Required',
            characteristic='Observed',
            catalog_bl=False,
            transformations_from_origin='transformations from origin',
            possible_data_source='possible data source',
            observations_comments='observations comments',
            examples='test examples',
            catalog=None
        )

var.catalog = catalog

entity.add_variable(var)
```
---

## Rules Set
#### Main functionalities:
The RuleSet class is responsible for managing a set of rules that can be applied to a dataset. It allows for the creation, modification, and retrieval of rules, as well as the generation of synthetic data based on those rules. The class also provides methods for getting the structure of the rules and for generating example rules based on a list of variables.

#### Methods:
- `__init__`: initializes the RuleSet object with a list of rules (if provided) and a description of the syntax for the rules.
- `append_rule`: adds a new rule to the list of rules.
- `pop_rule`: removes and returns the last rule in the list of rules.
- `rules_for_synthetic_data`: generates a set of rules for generating synthetic data based on the current set of rules and a list of variables.
- `get_rules_comparison_between_variables`: generates a set of rules for comparing variables in the current set of rules.
- `get_rules_dict`: returns a dictionary representation of the current set of rules.
- `get_structure`: returns a list of dictionaries representing the structure of the current set of rules.
- `get_rules_structure_example`: generates example rules based on a list of variables.

#### Example:
```python
from cdmb import ComparisonRule,BetweenComparison,RuleSet,Variable

r1 = ComparisonRule(Variable('age', "patient's age"), '>=', 18)
r2 = BetweenComparison(Variable('height', "patient's height"), 170, 180)
rs = RuleSet([r1, r2])
```

---

## Rules

## Comparison rule
#### Main functionalities:
The ComparisonRule class is a subclass of the abstract class Rule and represents a rule that compares a left statement with a right statement using a comparison operator. The main functionalities of this class are:
- To create a comparison rule with a left statement, a comparison operator, and a right statement.
- To validate the types of the left statement, the comparison operator, and the right statement.
- To treat the right statement according to its type and the comparison operator.
- To generate an expression that represents the comparison rule.
- To provide information about the comparison rule, such as its name, description, subtype comparison, max value, min value, and variable affected.

#### Methods:
- `__init__`: initializes the ComparisonRule object with a left statement, a comparison operator, and a right statement. It validates the types of the left statement, the comparison operator, and the right statement, and treats the right statement according to its type and the comparison operator. It generates an expression that represents the comparison rule, and provides information about the comparison rule, such as its name, description, subtype comparison, max value, min value, and variable affected.
- `get_structure`: returns a dictionary with the expression, name, and description of the comparison rule.

#### Example:
```python
from cdmb import Variable
from cdmb import ComparisonRule
import datetime

# ComparisonOperators ['<', '<=', '>', '>=', '=', '<>', '!=']

left_statement = Variable('age', "patient's age")
comparison_operator = '>='
right_statement = 18
rule = ComparisonRule(left_statement, comparison_operator, right_statement)

# Compare variables
left_statement = Variable('admission_dt', 'hospital admission')
right_statement = Variable('discharge_dt', 'hospital discharge')                       
rule2 = ComparisonRule(left_statement, '<=', right_statement)

# Compare with dates
rule3 = ComparisonRule(left_statement, '>=', datetime.date(2022,1,1))
```
---

## BetweenComparison
#### Main functionalities:
The BetweenComparison class is a subclass of the Rule abstract class and represents a rule that checks if a variable's value is between two given values. It can handle numerical, date, and datetime values. The rule can be negated to check if the variable's value is not between the two given values.

#### Methods:
- `__init__`: Initializes the BetweenComparison object with a variable, two values, and a flag to negate the rule. It checks the types of the inputs and constructs the expression for the rule.
- `get_structure`: Returns a dictionary with the expression, name, and description of the rule.

#### Example:
```python
from cdmb import Variable
from cdmb import BetweenComparison
import datetime

variable = Variable('age', "patient's age")
x_value = 18
y_value = 115
r1 = BetweenComparison(variable, x_value, y_value)
# r1 -> age BETWEEN 18 AND 115

variable2 = Variable('admission_dt', 'hospital admission')
r2 = BetweenComparison(variable2, datetime.date(2020,1,1), datetime.date(2021,1,1),negative=True)
# r2 -> admission_dt NOT BETWEEN '2020-01-01' AND '2021-01-01'
```


---

## NullCheckingRule
#### Main functionalities:
The NullCheckingRule class is a subclass of the abstract Rule class and represents a rule that checks whether a given variable is null or not null. It takes a Variable object and a boolean value as input and generates a SQL expression that checks whether the variable is null or not null based on the boolean value. This class is used to create rules for data validation and filtering.

#### Methods:
- `__init__`: Constructor method that takes a Variable object and a boolean value as input and generates a SQL expression that checks whether the variable is null or not null based on the boolean value.
- `get_structure`: Method that returns a dictionary with the expression, name, and description of the rule.

#### Example:
```python
from cdmb import Variable
from cdmb import NullCheckingRule

variable_1 = Variable('admission_dt', 'hospital admission')
rule = NullCheckingRule(variable_1, negative=True)
# rule -> admission_dt IS NOT NULL

variable_2 = Variable('discharge_dt', 'hospital discharge')
rule2 = NullCheckingRule(variable_2, negative=False)
# rule2 -> discharge_dt IS NULL
```
---

## InValuesRule
#### Main functionalities:
The InValuesRule class is a subclass of the abstract Rule class and represents a rule that checks if a variable's value is in a list of specified values. It can also check if the value is not in the list if the negative parameter is set to True. The class generates an SQL expression based on the input parameters and provides methods to access the expression, name, description, subtype_comparison, list of values, and the affected variable.

#### Methods:
- `__init__`: Initializes the InValuesRule object with a Variable object, a list of values, and a boolean flag to indicate if the rule should check for values not in the list.
- `get_structure`: Returns a dictionary with the expression, name, and description of the rule.

#### Example:
```python
from cdmb import Variable
from cdmb import InValuesRule

variable_1 = Variable('sex_cd', "patient's sex")
rule = InValuesRule(variable_1,['1','2','3','9'])
# rule -> sex_cd IN ('1','2','3','9')

rule2 = InValuesRule(variable_1,['1','2','3','9'], negative=True)
# rule2 ->  sex_cd NOT IN ('1','2','3','9')
```

---

## ComposedRule
#### Main functionalities:
The ComposedRule class is a subclass of the abstract class Rule and represents a complex rule that combines two other rules using a logical operator (and/or). It allows the creation of more complex rules by combining simpler rules.

#### Methods:
- `__init__`: Constructor that initializes the ComposedRule object with two Rule objects and a logical operator to combine them.
- `get_structure`: Returns a dictionary with the expression, name, and description of the composed rule.


#### Example:
```python
from cdmb import Variable
from cdmb import ComposedRule,ComparisonRule

variable_1 = Variable('sex_cd', "patient's sex")
variable_2 = Variable('pregnancy_bl', "pregnancy status")


composed_rule = ComposedRule(
        left_statement=ComparisonRule(variable_1,'=','1'), 
        logical_operator='and',    ## and | or 
        right_statement=ComparisonRule(variable_2, '!=', False))

# composed_rule -> (sex_cd = 1) and (pregnancy_bl != FALSE)
```



## DummyRule
#### Main functionalities:
The DummyRule class is a subclass of the abstract Rule class and is used to create a dummy rule with a custom expression, name, and description. This class can be used to create a rule that does not fit into any of the other rule subclasses.
Exploit the full potential of DuckDB by following its [documentation](https://duckdb.org/docs/sql/introduction).

#### Methods:
- `__init__`: Initializes the DummyRule object with the given expression, name, and description.
- `get_structure`: Returns a dictionary with the expression, name, and description of the rule.

#### Example:
```python
from cdmb import DummyRule

r1 = DummyRule(
    expression="diagnose LIKE 'I20%' and age_cd < 40",
    name='heart attacks rule',
    description=' heart attacks in people under 40 years of age')

# r1 -> diagnose LIKE 'I20%' and age_cd < 40
```

## Relationships
#### Main functionalities:
The Relationship class represents the relationship between two entities (Entity) and provides functionalities to establish and update the relationship. It allows the user to specify the left and right entities, the left and right columns, and the type of join. It also provides methods to get the structure of the relationship and to update the left and right entities, columns, and join type.

#### Methods:
- `__init__`: Initializes the Relationship object with the left and right entities, left and right columns, and join type.
- `get_structure`: Returns a dictionary with the structure of the relationship.

#### Fields:
- **left_entity**: The left entity of the relationship.
- **right_entity**: The right entity of the relationship.
- **join_type**: The type of join between the two entities.
- **left_column**: The left column of the relationship.
- **right_column**: The right column of the relationship.

#### Example:
```python
from cdmb import Entity
from cdmb import Variable
from cdmb import Relationship


main_entity = Entity(
        name='Admission',
        time_varying=False,
        variables=[
            Variable('patient_id', "Patient's pseudonymized id"),
            Variable('service_cd', "Service's code")
        ])
services_entity = Entity(
        name='Service',
        time_varying=False,
        variables=[
            Variable('code', "Service's code"),
            Variable('description', "Service's description")
        ])

relationship = Relationship(
    left_entity = main_entity,
    right_entity = services_entity,
    left_column =  Variable('service_cd', "Service's code"),
    right_column = Variable('code', "Service's code"),
    join_type= "LEFT JOIN" # Join Options -> ["LEFT JOIN", "INNER JOIN", "RIGHT JOIN", "FULL JOIN"]
)
```

## Common Data Model
#### Main functionalities:
- The CommonDataModel class represents a common data model that can be used to define metadata, cohorts, entities, and relationships in a data project.
- It provides methods to add and remove entities, set and get metadata and cohort information, and save the project to a specified directory.
- It also has a method to generate a JSON structure representing the data model and a method to load a previous configuration from a dictionary or from web files.

#### Methods:
- `__init__`: Initializes the CommonDataModel object with metadata, cohort, entities, and relationships.
- `add_entity`: Adds an entity to the list of entities.
- `pop_entity`: Removes and returns the last entity from the list of entities.
- `save_project`: Saves the project to a specified directory by calling various private methods to write metadata, cohort, entities, relationships, and other project files.
- `save_zipped_project`: Saves the project to a temporary directory, creates a zip file of the project, and returns the UUID of the zip file.
- `generate_json_structure`: Generates a JSON structure representing the data model.
- `load_previous_configuration`: Loads a previous configuration from a dictionary and returns the metadata, cohort, entities, and relationships.
- `get_er`: Generates an entity-relationship diagram (ER diagram) for the entities and relationships.


#### Example:
```python
from cdmb import Metadata
from cdmb import Author
from cdmb import Cohort
from cdmb import Entity
from cdmb import Variable
from cdmb import Relationship
import datetime

from cdmb.CommonDataModel import CommonDataModel

metadata = Metadata(project='Test Project', use_case='Use Case')

author = Author(
        name='John Doe', 
        affiliation='University of California', 
        id='0000-0000-0000-0001'
      )

metadata = Metadata(project='Test Project', use_case='Use Case')
metadata.add_author(author)

cohort = Cohort(
        name='Cohort name',
        description='Cohort description',
        inclusion_criteria='Inclusion criteria text',
        beggining_study_period=datetime.date(2021, 1, 1),
        end_study_period=datetime.date(2021, 12, 31)
    )


main_entity = Entity(
        name='Admission',
        time_varying=False,
        variables=[
            Variable('patient_id', "Patient's pseudonymized id"),
            Variable('service_cd', "Service's code")
        ])
services_entity = Entity(
        name='Service',
        time_varying=False,
        variables=[
            Variable('code', "Service's code"),
            Variable('description', "Service's description")
        ])

rel = Relationship(
    left_entity = main_entity,
    right_entity = services_entity,
    left_column =  Variable('service_cd', "Service's code"),
    right_column = Variable('code', "Service's code"),
    join_type= "LEFT JOIN" # Join Options -> ["LEFT JOIN", "INNER JOIN", "RIGHT JOIN", "FULL JOIN"]
)

cdmb_ =  CommonDataModel(
    metadata_definition=metadata,
    cohort_definition=cohort,
    entities=[main_entity,services_entity],
    relationships=[rel]
)

cdmb_.save_project(out_dir='outputs') # save folder structure
cdmb_.save_zipped_project(out_dir='outputs') # save zip
```
# Data types
Several data types are used to restrict the values that can take certain variables or parameters. 
For example:

-  **NatureOptions**: is a data type that can only take the values "**Condition**", "**Intervention**", "**Drugs**" or "**Any**".

-  **FormatOptions**: is a data type that can only take the values "**String**", "**Boolean**", "**Date**", "**Datetime**", "**Integer**" or "**Double**".

-  **TypeOptions**: is a data type that can only take the values "**Categorical**", "**Date**" or "**Numerical**".

-  **RequirementOptions**: is a data type that can only take the values "**Required**", "**Recommended**" or "**Optional**".

-  **JoinOptions**: is a data type that can only take the values "**LEFT JOIN**", "**INNER JOIN**", "**RIGHT JOIN**" or "**FULL JOIN**".

-  **CharacteristicOptions**: is a data type that can only take the values "**Observed**" or "**Calculated**".

-  **ComparisonOperators**: is a data type that can only take the values '**<**', '**<=**', '**>**', '**>=**', '**=**', '**<>**', '!='.

-  **BooleanOperators**: is a data type that can only take the values '**and**' or '**or**'.

# Authoring
Common Data Model Builder (cdmb) has been developed by the [Data Science for Health Services and Policy research group](https://cienciadedatosysalud.org/en/us/research-group/)
in the Institute for Health Sciences in Aragón (IACS).

Lead by ![orcid](https://orcid.org/sites/default/files/images/orcid_16x16.png) [Javier González-Galindo](https://orcid.org/0000-0002-8783-5478)
, with the colaboration of ![orcid](https://orcid.org/sites/default/files/images/orcid_16x16.png) [Francisco Estupiñán-Romero](https://orcid.org/0000-0002-6285-8120), 
and ![orcid](https://orcid.org/sites/default/files/images/orcid_16x16.png) [Santiago Royo-Sierra](https://orcid.org/0000-0002-0048-4370)
, under the supervision and coordination of ![orcid](https://orcid.org/sites/default/files/images/orcid_16x16.png) [Enrique Bernal-Delgado](https://orcid.org/0000-0002-0961-3298) (PI).

# How to contribute
- Repository: https://github.com/cienciadedatosysalud/cdmb/
- Issue tracker: https://github.com/cienciadedatosysalud/cdmb/issues

# References
- Data Science for Health Services and Policy Research group: https://cienciadedatosysalud.org/en/
- Atlas VPM Community: https://zenodo.org/communities/atlasvpm
- ORCID: https://orcid.org/
 
---

<a href="hhttps://creativecommons.org/licenses/by-nc/4.0/" target="_blank" ><img src="https://img.shields.io/badge/license-CC--BY--NC%204.0-lightgrey" alt="License: CC-BY-NC 4.0"></a>

