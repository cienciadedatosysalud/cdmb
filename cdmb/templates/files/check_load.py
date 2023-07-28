import glob
import json
import logging
import os
import re

import duckdb  # duckdb-0.8.1
import pandas as pd


def infer_separator(file_):
    firstline = file_.readline().rstrip()
    separators = re.sub('"*[a-zA-ZÀ-ÿñÑ0-9_-]*"*', '', firstline)
    if len(separators) > 0:
        return separators[0], firstline
    else:
        # Return random separator, exception will be thrown on header reading
        return '|'


def read_file(entity_structure, dtype_, parse_dates):
    logging.info("Trying to read the file with the configuration provided.")
    try:
        df = pd.read_csv(
            entity_structure['uploaded_filename'],
            sep=entity_structure['separator'],
            dtype=dtype_,
            parse_dates=parse_dates
        )
        len_df = len(df)
        logging.info(f"{len_df} records read.")
        return df
    except ValueError as e:
        logging.error(f"Reading the file with the provided configuration failed!")
        logging.error(str(e))
        df = pd.read_csv(
            entity_structure['uploaded_filename'],
            sep=entity_structure['separator']
        )
        variables_name = []
        variables_format = []
        for k, v in dtype_.items():
            if pd.StringDtype != type(v):
                variables_name.append(k)
                variables_format.append(v)
        for v in df.dtypes.items():
            logging.error(f"{v}")
        exit(1)


def load_file(entity_structure, df):
    logging.info(f"Trying to connect to the database ...")
    try:
        con = duckdb.connect(database_path, read_only=False)
        logging.info(f"Connected!")
        entity_name_ = entity_structure['entity_name']
        logging.info(f"Trying to load records in the table \"{entity_name_}\"")
        query = "INSERT INTO {entity} SELECT * FROM df;".format(entity=entity_name_)
        con.execute(query)
        logging.info(f"{entity_structure['uploaded_filename']} -> LOADED!")
    except Exception as e:
        logging.error("Something went wrong trying to insert the data!")
        logging.error(str(e))
    finally:
        con.close()


def check_file(entity_structure):
    dtype_ = {}
    parse_dates = []
    for c, f in zip(entity_structure['entity_variables'], entity_structure['entity_formats']):
        if f == 'string':
            dtype_[c] = pd.StringDtype()
            pass
        elif f == 'boolean':
            dtype_[c] = pd.BooleanDtype()
        elif f == 'date' or f == 'datetime':
            parse_dates.append(c)
        elif f == 'integer':
            dtype_[c] = pd.Int64Dtype()
        elif f == 'double':
            dtype_[c] = pd.Float64Dtype()
            pass
        else:
            logging.warning(f"Format '{f}' not found, will be interpreted as String object.")
            dtype_[c] = pd.StringDtype()
    df = read_file(entity_structure, dtype_, parse_dates)
    load_file(entity_structure, df)


def create_entity_table_if_not_exists(entity_name_, entity_variables_, entity_formats_):
    format_translation = {
        "string": "VARCHAR",
        "boolean": "BOOLEAN",
        "date": "DATE",
        "datetime": "TIMESTAMP",
        "integer": "BIGINT",
        "double": "DOUBLE"
    }
    query = f"""CREATE TABLE IF NOT EXISTS {entity_name_}({entity_variables_[0]} {format_translation.get(entity_formats_[0], "VARCHAR")}"""
    for (variable_, format_) in zip(entity_variables_[1:], entity_formats_[1:]):
        query += f""", {variable_} {format_translation.get(format_)}"""
    query += ");"
    try:
        logging.info(f"Trying to connect to the database ...")
        logging.info(f"Trying to create the table for entity \"{entity_name_}\"")
        logging.info(f"Table structure:\n {query}")
        con = duckdb.connect(database_path, read_only=False)
        con.execute(query)
        logging.info(f"Table successfully created!")
    except Exception as e:
        logging.error("Something went wrong in the creation of the table")
        logging.error(str(e))
    finally:
        con.close()

def create_entity_table(entity_name_, entity_variables_, entity_formats_):
    format_translation = {
        "string": "VARCHAR",
        "boolean": "BOOLEAN",
        "date": "DATE",
        "datetime": "TIMESTAMP",
        "integer": "BIGINT",
        "double": "DOUBLE"
    }
    query = f"""CREATE OR REPLACE TABLE {entity_name_}({entity_variables_[0]} {format_translation.get(entity_formats_[0], "VARCHAR")}"""
    for (variable_, format_) in zip(entity_variables_[1:], entity_formats_[1:]):
        query += f""", {variable_} {format_translation.get(format_)}"""
    query += ");"
    try:
        logging.info(f"Trying to connect to the database ...")
        logging.info(f"Trying to create the table for entity \"{entity_name_}\"")
        logging.info(f"Table structure:\n {query}")
        con = duckdb.connect(database_path, read_only=False)
        con.execute(query)
        logging.info(f"Table successfully created!")
    except Exception as e:
        logging.error("Something went wrong in the creation of the table")
        logging.error(str(e))
    finally:
        con.close()


if __name__ == '__main__':
    # Do not modify if you use the deployment container!
    os.chdir(os.path.dirname(__file__))
    logging.basicConfig(format='%(levelname)s:: %(message)s', level=logging.INFO)
    logging.info("Starting Checking data syntax process")
    # Relative paths to the work structure provided from CDMBuilder.
    # Important! The functionality of this script may vary, but the file name,
    # where it reads the data and where the results are saved must be maintained
    # for the correct functioning of the tool.
    database_path = '../../inputs/data.duckdb'
    configuration_file_path = '../../docs/CDM/cdmb_config.json'
    output_path = '../../outputs'
    upload_files_path = './inputs'

    # Opening JSON file
    try:
        with open(configuration_file_path) as configuration_file:
            configuration_file = json.load(configuration_file)
    except FileNotFoundError as e:
        logging.error("Configuration file "" is missing!")
        exit(1)
    logging.info("Configuration file loaded")
    csv_files = glob.glob(upload_files_path + "/*.csv", recursive=True)
    uploaded_file_structure = []
    logging.info(f"-Found {len(csv_files)} uploaded files to check and map!")
    for uploaded_file in csv_files:
        try:
            with open(uploaded_file, mode='rt', encoding='utf-8') as file:
                separator, header = infer_separator(file)
                logging.info(f"Inferred separator \"{separator}\" for \"{uploaded_file}\" file ")
                header_variable_list = [column.replace("\"", "").strip() for column in str(header).split(separator)]
                uploaded_file_structure.append({
                    'filename': uploaded_file,
                    'header': header_variable_list,
                    'separator': separator
                })
        except Exception as e:
            logging.error(f"Something went wrong trying to read \"{uploaded_file}\" file")
            logging.error(str(e))
            exit(1)
    if 'entities' in configuration_file:
        entities_structure = []
        for entity in configuration_file['entities']:
            if 'name' not in entity or 'variables' not in entity:
                logging.error("properties \"name\" or \"variables\" not found in entity! Check specifications!")
                exit(1)
            entity_name = entity['name']
            logging.info(f"Processing entity \"{entity_name}\"...")
            try:
                entity_variables = [variable['label'] for variable in entity['variables']]
                entity_formats = [str(variable['format']).lower() for variable in entity['variables']]
                create_entity_table_if_not_exists(entity_name,entity_variables,entity_formats)
            except Exception as e:
                logging.error("Variables must have the properties \"label\" and \"format\"")
                logging.error(str(e))
                exit(1)

            uploaded_filename_ = None
            uploaded_filename_list = []
            for file_structure in uploaded_file_structure:
                if set(entity_variables) == set(file_structure['header']):
                    uploaded_filename_ = file_structure
                    logging.info("One of the uploaded files has been found that matches the entity's configuration.")
                    logging.info(f"\"{entity_name}\" with {file_structure['filename']} file")
                    uploaded_filename_list.append(uploaded_filename_)
                else:
                    pass

            if uploaded_filename_ is not None:
                try:
                    logging.info(f"Creating table for entity \"{entity_name}\".")
                    create_entity_table(entity_name, entity_variables, entity_formats)
                except Exception as e:
                    logging.error(f"Something went wrong creating the table for entity \"{entity_name}\"")
                    logging.error(str(e))
                    exit(1)
                uploaded_filename_clean = [str(uploaded_filename_['filename']).rsplit('/', 1)[1] for uploaded_filename_
                                           in uploaded_filename_list]
                uploaded_filename = [uploaded_filename_['filename'] for uploaded_filename_ in uploaded_filename_list]
                separator = [uploaded_filename_['separator'] for uploaded_filename_ in uploaded_filename_list]
            else:
                logging.warning(f"No file of the uploaded files has been found that matches the header with the "
                                f"configuration of the \"{entity_name}\" entity.!")
                uploaded_filename_clean = None
                uploaded_filename = None
                separator = None
            entities_structure.append({
                'entity_name': entity_name,
                'entity_variables': entity_variables,
                'entity_formats': entity_formats,
                'uploaded_filename_clean': uploaded_filename_clean,
                'uploaded_filename': uploaded_filename,
                'separator': separator
            })
        logging.info("Starting the check of the files that do match an entity.")
        logging.info(entities_structure)
        for entity_structure_ in entities_structure:
            if entity_structure_['uploaded_filename'] is not None:
                #
                for uploaded_filename_clean, uploaded_filename, separator in zip(
                        entity_structure_['uploaded_filename_clean'],
                        entity_structure_['uploaded_filename'],
                        entity_structure_['separator']):
                    check_file({
                        'entity_name': entity_structure_['entity_name'],
                        'entity_variables': entity_structure_['entity_variables'],
                        'entity_formats': entity_structure_['entity_formats'],
                        'uploaded_filename_clean': uploaded_filename_clean,
                        'uploaded_filename': uploaded_filename,
                        'separator': separator
                    })
            else:
                pass
    else:
        logging.error("\"entities\" not found in your configuration file! Check specifications!")
        exit(1)
