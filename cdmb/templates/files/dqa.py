import json
import logging
import os

import duckdb  # duckdb-0.8.1
from ydata_profiling import ProfileReport  # ydata-profiling-4.1.1

if __name__ == '__main__':
    # Do not modify if you use the deployment container!
    os.chdir(os.path.dirname(__file__))
    logging.basicConfig(format='%(levelname)s:: %(message)s', level=logging.INFO)
    # Relative paths to the work structure provided from CDMBuilder.
    # Important! The functionality of this script may vary, but the file name,
    # where it reads the data and where the results are saved must be maintained
    # for the correct functioning of the tool.
    logging.info("Starting Data Quality Assesment process")
    database_path = '../../inputs/data.duckdb'
    configuration_file_path = '../../docs/CDM/cdmb_config.json'
    output_path = '../../outputs'

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
    con = duckdb.connect(database_path, read_only=True)
    for entity in entities:
        if 'name' not in entity:
            logging.error("properties \"name\" not found in entity! Check specifications!")
            exit(1)
        entity_name = entity['name']
        title = configuration_file['metadata']['use_case'] + ' - ' + entity_name + ' | Profiling Report'
        query = "Select * from {entity}".format(entity=entity_name)
        df_entity = con.query(query).to_df()
        logging.info(f"\"{entity_name}\" entity contains {len(df_entity)} records")
        if len(df_entity) > 0:
            profile = ProfileReport(df_entity, title=title, minimal=True)
            html_out = os.path.join(output_path, "dqa_{usecase}_{entity_}.html".format(
                usecase=use_case_name,
                entity_=str(entity_name).replace(' ', '_')
            ))
            json_out = os.path.join(output_path, "dqa_{usecase}_{entity_}.json".format(
                usecase=use_case_name,
                entity_=str(entity_name).replace(' ', '_')
            ))
            profile.to_file(html_out)
            profile.to_file(json_out)
    con.close()
