import json
import logging
import os

import duckdb  # duckdb-0.8.1
import pandas as pd

if __name__ == '__main__':
    # Do not modify if you use the deployment container!
    os.chdir(os.path.dirname(__file__))
    logging.basicConfig(format='%(levelname)s:: %(message)s', level=logging.INFO)
    # Relative paths to the work structure provided from CDMBuilder.
    # Important! The functionality of this script may vary, but the file name,
    # where it reads the data and where the results are saved must be maintained
    # for the correct functioning of the tool.
    database_path = '../../inputs/data.duckdb'
    configuration_file_path = '../../docs/CDM/cdmb_config.json'
    output_path = '../../outputs'

    logging.info("Starting Checking data compliance with validation rules process")
    # Opening JSON file
    try:
        with open(configuration_file_path) as configuration_file:
            configuration_file = json.load(configuration_file)
    except FileNotFoundError as e:
        logging.error("Configuration file "" is missing!")
        exit(1)
    logging.info("Configuration file loaded.")

    if 'metadata' not in configuration_file:
        logging.error(
            "\"metadata\" not found in your configuration file! Check specifications!")
        exit(1)
    if 'use_case' not in configuration_file['metadata']:
        logging.error(
            "\"use_case\" not found in your configuration file ('metadata' -> 'use_case')! Check specifications!")
        exit(1)
    if 'entities' not in configuration_file:
        logging.error("\"entities\" not found in your configuration file! Check specifications!")
        exit(1)

    use_case_name = str(configuration_file['metadata']['use_case']).replace(' ', '_')

    entities = configuration_file['entities']

    logging.info(f"Trying to connect to the database ...")
    con = duckdb.connect(database_path, read_only=False)
    # total_registries
    response = []
    for entity in entities:
        if 'name' not in entity:
            logging.error("properties \"name\" not found in entity! Check specifications!")
            exit(1)
        # Create a list with the line number occupied by each record
        # to inform in which position the errors are found.
        view_name = f"{entity['name']}_view"

        entity_name = entity['name']
        logging.info(
            f"Checking the conformity of the data with the validation rules for the \"{entity_name}\" entity.")
        view_query = f"CREATE OR REPLACE VIEW  {view_name} AS SELECT * FROM (SELECT ROW_NUMBER () OVER () as line_number, * FROM {entity_name})"
        con.execute(view_query)
        result_entity = {}
        result_na = []
        result_rules = []
        result_catalogs = []
        # Count total registries
        logging.info(
            f"Counting total registries for the \"{entity_name}\" entity.")
        count_query = f"Select COUNT(*) as total_registries from {entity_name};"
        result = con.query(count_query).to_df()
        result_entity['entity'] = entity_name
        result_entity['total_registries'] = int(result['total_registries'][0])
        # Count NA values
        if 'variables' not in entity:
            logging.error("properties \"variables\" not found in entity! Check specifications!")
            exit(1)
        logging.info(
            f"Counting NA values for the \"{entity_name}\"'s variables.")
        for variable in entity['variables']:
            if 'label' not in variable:
                logging.error(
                    f"There are variables without the \"label\" property in the \"{entity_name}\" entity.")
                exit(1)
            na_query = f"Select COUNT(*) as na_count from {entity_name} where {variable['label']} is NULL;"
            result = con.query(na_query).to_df()
            result_na.append({
                "label": variable['label'],
                "na_count": int(result['na_count'][0])
            })

            if 'catalog_bl' not in variable:
                logging.warning(
                    f"\"catalog_bl\" property is not defined for variable")

            if 'catalog_bl' in variable and variable['catalog_bl'] is True and str(variable['format']).lower() != "boolean":
                logging.info(
                    f"Checking variables that are defined based on a catalog.")
                if variable['catalog'] is None or 'column_name' not in variable['catalog'] or 'filename' not in variable['catalog']:
                    logging.error(
                        f"\"catalog\" for your variable \"{entity_name}\" is not well defined in your configuration file! Check the specifications!")
                    exit(1)
                column_name = variable['catalog']["column_name"]
                filename = variable['catalog']["filename"]

                catalog_path = os.path.join('../../docs/CDM/entities', entity_name, 'catalogs', filename)
                try:
                    catalog_table = pd.read_csv(catalog_path)
                except Exception as e:
                    logging.error(
                        f"An attempt was made to read catalog \"{filename}\" but it failed. does the file exist in "
                        f"the catalogs folder inside the entity folder structure ?")
                    logging.error(str(e))
                    exit(1)

                catalog_query = f"select CAST(line_number AS VARCHAR) as wrong_lines, CAST({view_name}.{variable['label']} AS VARCHAR) as {variable['label']} from {view_name} " \
                                f"left join catalog_table " \
                                f"on {view_name}.{variable['label']} = catalog_table.{column_name} " \
                                f"where catalog_table.{column_name} is NULL and {view_name}.{variable['label']} is not NULL"
                catalog_result = con.query(catalog_query).to_df()
                logging.warning(
                    f"{len(list(catalog_result[variable['label']].unique()))} different erroneous values were found in the data according to the catalog.")
                wrong_lines = list(catalog_result['wrong_lines'].values[:10]) + list([f"+{len(catalog_result['wrong_lines'].values)-10} lines"])
                wrong_values = list(catalog_result[variable['label']].unique()[:10]) + list([f"+{len(catalog_result[variable['label']].unique())-10} values"])
                if len(catalog_result['wrong_lines'].values) <= 10:
                    wrong_lines = list(catalog_result['wrong_lines'].values[:10])
                if len(catalog_result[variable['label']].unique()) <= 10:
                    wrong_values = list(catalog_result[variable['label']].unique()[:10])
                result_catalogs.append({
                    "variable": variable['label'],
                    "wrong_values": wrong_values,
                    "wrong_lines": wrong_lines,
                    "total_wrong_lines": len(catalog_result['wrong_lines'].values)
                })

        result_entity['na_count_list'] = result_na
        result_entity['catalog_checking'] = result_catalogs

        logging.info(f"Starting validation rules checking")
        if 'rules' in entity:
            # Check rules
            rules = entity['rules']
        else:
            logging.warning(f"\"rules\" for your entity \"{entity_name}\" is not well defined in your configuration file! Check the specifications!")
            rules = []

        for rule in rules:
            logging.info(f"Checking rule - \" {rule['expression']} \"")
            rule_query = f"Select COUNT(*) as passed_rule from {entity_name} where {rule['expression']} ;"
            try:
                result = con.query(rule_query).to_df()
                # Select the lines that do not comply with the rule
                wrong_lines_query = f"select CAST(original_data.line_number as VARCHAR) as wrong_lines " \
                                    f"from (select line_number from {view_name}) original_data " \
                                    f"left join (select line_number from {view_name}  " \
                                    f"where {rule['expression']}) rule_query " \
                                    f"on original_data.line_number == rule_query.line_number " \
                                    f"where rule_query.line_number is NULL "
                wrong_result = con.query(wrong_lines_query).to_df()
                logging.info(f"{int(result['passed_rule'][0])} entries passed the rule.")
                wrong_lines = list(wrong_result['wrong_lines'].values[:10]) + list(
                    [f"+{len(wrong_result['wrong_lines'].values) - 10} lines"])
                if len(wrong_result['wrong_lines'].values) <= 10:
                    wrong_lines = list(wrong_result['wrong_lines'].values[:10])
                result_rules.append({
                    "expression": rule['expression'],
                    "passed_rule": int(result['passed_rule'][0]),
                    "wrong_lines": wrong_lines,
                    "total_wrong_lines": len(wrong_result['wrong_lines'].values)
                })

            except Exception as e:
                logging.warning(f"rule - \" {rule['expression']} \" fails!")
                logging.error(str(e))
                result_rules.append({
                    "expression": rule['expression'],
                    "passed_rule": 0,
                    "wrong_lines": f"{result_entity['total_registries']} lines",
                    "total_wrong_lines": result_entity['total_registries']
                })
                pass

        result_entity['rules'] = result_rules
        response.append(result_entity)
        con.execute(f"DROP VIEW IF EXISTS {view_name};")
    try:
        with open(os.path.join(output_path, 'validator_output.json'), 'w') as f:
            json_object = json.dumps({'info':response}, indent=4)
            f.write(json_object)
            logging.info(f"validator_output.json created.")
    except Exception as e:
        logging.error(f"Something went wrong trying to write \"validator_output\" files")
        logging.error(str(e))
    
    con.close()
