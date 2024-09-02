import json
import logging
import os
import glob
import duckdb
import subprocess
import random
import os
import time

# The functionality of this script is to test the developed scripts in different scenarios.
#
# Scenario 1: Set to null Optional Variable
# Scenario 2: Set to null recommended variables
# Scenario 3: Set 25% null values in required variables
# Scenario 4: Assign constant values to all required variables
#

def get_entities_variables_configuration():
    response = []
    entities = configuration_file['entities']
    for entity in entities:
        partial_res = {"entity_name":entity['name']}
        optional_var = [ v['label'] for v in entity['variables'] if v['requirement_level'] == "Optional"]
        recommended_var = [ v['label'] for v in entity['variables'] if v['requirement_level'] == "Recommended"]
        required_var = [ v['label'] for v in entity['variables'] if v['requirement_level'] == "Required"]
        constant_var_notstr = [ v['label'] for v in entity['variables'] if v['format'] not in ["Date","Datetime","String"]]
        constant_var_str = [ v['label'] for v in entity['variables'] if v['format'] == "String"]
        partial_res['optional'] = optional_var
        partial_res['recommended'] = recommended_var
        partial_res['required'] = required_var
        partial_res['constant_var_notstr'] = constant_var_notstr
        partial_res['constant_var_str'] = constant_var_str   
        response.append(partial_res)
    return response
    

def copy_original_data(entities):
    con = duckdb.connect(database_path, read_only=False)
    for entity in entities:
        con.execute(f"CREATE OR REPLACE TABLE {entity}_copy AS FROM {entity};")
    pass

def reset_original_data(entities):
    con = duckdb.connect(database_path, read_only=False)
    for entity in entities:
        con.execute(f"CREATE OR REPLACE TABLE {entity} AS FROM {entity}_copy;")
    pass

def remove_copy_data(entities):
    reset_original_data(entities)
    con = duckdb.connect(database_path, read_only=False)
    for entity in entities:
        con.execute(f"DROP TABLE {entity}_copy;")

def search_scripts():
    text_files = glob.glob("./**.*", recursive=False)
    text_files = [file.rsplit('/', 1)[1] for file in text_files]
    text_files = [file for file in text_files if str(file.split('.')[1]).lower() in ["py", "r", "qmd"]]
    text_files = [file for file in text_files if file != 'testing.py']
    return text_files


def run_script(script_path):
    file_name, file_extension = os.path.splitext(script_path)
    file_extension = file_extension.upper()
    if file_extension == ".R":
        process = subprocess.Popen(["Rscript", script_path],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        output, error = process.communicate()
        process.wait()
        output = output.replace("\x1b[39m", "")
        output = output.replace("\x1b[31m", "")
        output = output.replace("\x1b[1m", "")
        output = output.replace("\x1b[22m", "")
        if process.returncode != 0:
            logging.info("#########################################")
            logging.info(f"{script_path} script failed\n")
            logging.info(f"Error log:\n")
            logging.info("-----------------------------------------")
            logging.error(f"{output}\n")
            logging.info("#########################################\n")
        else:
            logging.info("#########################################")
            logging.info(f"{script_path} was executed correctly\n")
            logging.info("#########################################\n")
            
    elif file_extension == ".PY":
        process = subprocess.Popen(["python3", script_path],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        output, error = process.communicate()
        process.wait()
        output = output.replace("\x1b[39m", "")
        output = output.replace("\x1b[31m", "")
        output = output.replace("\x1b[1m", "")
        output = output.replace("\x1b[22m", "")
        if process.returncode != 0:
            logging.info("#########################################")
            logging.info(f"{script_path} script failed\n")
            logging.info(f"Error log:\n")
            logging.info("-----------------------------------------")
            logging.error(f"{output}\n")
            logging.info("#########################################\n")
        else:
            logging.info("#########################################")
            logging.info(f"{script_path} was executed correctly\n")
            logging.info("#########################################\n")
       
    elif file_extension == ".QMD":
        process = subprocess.Popen(["quarto", "render", script_path, "--output-dir", "../../outputs"],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        output, error = process.communicate()
        process.wait()
        # remove colors
        output = output.replace("\x1b[39m", "")
        output = output.replace("\x1b[31m", "")
        output = output.replace("\x1b[1m", "")
        output = output.replace("\x1b[22m", "")
        if process.returncode != 0:
            logging.info("#########################################")
            logging.info(f"{script_path} script failed\n")
            logging.info(f"Error log:\n")
            logging.info("-----------------------------------------")
            logging.error(f"{output}\n")
            logging.info("#########################################\n")
        else:
            logging.info("#########################################")
            logging.info(f"{script_path} was executed correctly\n")
            logging.info("#########################################\n")
    else:
        raise Exception(status_code=400, detail="Script with invalid extension. Only .py, .R , .qmd (Python or R) are supported.")
    
    

def execute_scenario1(entities,script_path):
    # Set to null Optional Variable
    logging.info("#########################################")
    logging.info(f"# Scenario 1")
    logging.info(f"# Set to null Optional Variable")
    logging.info("#########################################\n")
    can_run = False
    con = duckdb.connect(database_path, read_only=False)
    for e in entities:
        if len(e['optional']) > 0:
            query = f"UPDATE {e['entity_name']} SET " + " = NULL, ".join(e['optional']) + " = NULL;" 
            con.execute(query)
            can_run = True
    con.close()
    if can_run:
        run_script(script_path)
    else:
        logging.info("#########################################")
        logging.info(f"# The Common Data Model has no optional variables.")
        logging.info("#########################################\n") 
    


def execute_scenario2(entities,script_path):
    # Set to null recommended variables
    logging.info("#########################################")
    logging.info(f"# Scenario 2")
    logging.info(f"# Set to null recommended variables")
    logging.info("#########################################\n")
    can_run = False
    con = duckdb.connect(database_path, read_only=False)
    for e in entities:
        if len(e['recommended']) > 0:
            query = f"UPDATE {e['entity_name']} SET " + " = NULL, ".join(e['recommended']) + " = NULL;" 
            con.execute(query)
            can_run = True
    con.close()
    if can_run:
        run_script(script_path)
    else:
        logging.info("#########################################")
        logging.info(f"# The Common Data Model has no recommended variables.")
        logging.info("#########################################\n") 

def execute_scenario3(entities,script_path):
    # set 25% null values in required variables
    logging.info("#########################################")
    logging.info(f"# Scenario 3")
    logging.info(f"# Set 25% null values in required variables")
    logging.info("#########################################\n")
    can_run = False
    con = duckdb.connect(database_path, read_only=False)
    for e in entities:
        if len(e['required']) > 0:
            # Get count 
            n_registries = con.execute(f"SELECT COUNT(*) FROM {e['entity_name']}").fetchone()[0]
            n_registries_25 = int(n_registries * 0.25)
            if n_registries > 25:
                for c in e['required']:
                    indexes = random.sample(range(0, n_registries), n_registries_25)
                    indexes = [str(i) for i in indexes]
                    query = f"UPDATE {e['entity_name']} SET {c} = NULL where rowid in (" + ",".join(indexes) + ");" 
                    con.execute(query)
                    can_run = True
    con.close()
    if can_run:
        run_script(script_path)
    else:
        logging.info("#########################################")
        logging.info(f"# The Common Data Model has no required variables.")
        logging.info("#########################################\n") 

def execute_scenario4(entities,script_path):
    # Assign constant values to all required variables
    logging.info("#########################################")
    logging.info(f"# Scenario 4")
    logging.info(f"# Assign constant values to all required variables")
    logging.info("#########################################\n")
    can_run = False
    con = duckdb.connect(database_path, read_only=False)
    logging.info(f"{entities}")
    for e in entities:
        n_registries = con.execute(f"SELECT COUNT(*) FROM {e['entity_name']}").fetchone()[0]
        if n_registries > 0:
            if len(e['constant_var_notstr']) > 0:
                for variable in e['constant_var_notstr']:
                    value = con.execute(f"select {variable} from {e['entity_name']} where {variable} is not null using sample 1").fetchone()
                    if value is not None :
                        value = value[0]
                        query = f"UPDATE {e['entity_name']} SET {variable} = {value};" 
                        con.execute(query)
                        can_run = True
            if len(e['constant_var_str']) > 0:
                for variable in e['constant_var_str']:
                    value = con.execute(f"select {variable} from {e['entity_name']} where {variable} is not null using sample 1").fetchone()
                    if value is not None :
                        value = value[0]
                        query = f"UPDATE {e['entity_name']} SET {variable} = '{value}';" 
                        con.execute(query)
                        can_run = True        
    con.close()
    if can_run:
        run_script(script_path)
    else:
        logging.info("#########################################")
        logging.info(f"# Something went wrong trying to run scenario 4.")
        logging.info("#########################################\n") 
def clean_outputs(time_): 
    output_path = '../../outputs'
    for file_ in os.listdir(output_path):
        file_ = os.path.join(output_path, file_)
        if os.path.isfile(file_):
            modificado = os.path.getmtime(file_)
            if modificado > time_:
                os.remove(file_)

if __name__ == '__main__':
    # Do not modify if you use the deployment container!
    os.chdir(os.path.dirname(__file__))
    
    logging.basicConfig(format='%(asctime)s::%(levelname)s:: %(message)s', level=logging.INFO)
    database_path = '../../inputs/data.duckdb'
    configuration_file_path = '../../docs/CDM/cdmb_config.json'
    output_path = '../../outputs'
    
    try:
        with open(configuration_file_path) as configuration_file:
            configuration_file = json.load(configuration_file)
    except FileNotFoundError as e:
        logging.error("Configuration file "" is missing!")
        exit(1)
        
    logging.info("Configuration file loaded\n")
    CDMB_VERSION = configuration_file["cdmb_version"] if "cdmb_version" in configuration_file else "Non-versioned"
    ASPIRE_VERSION = os.environ.get('ASPIRE_VERSION', 'Non-versioned')
    PIPELINE_VERSION = os.environ.get('PIPELINE_VERSION', 'Non-versioned')
    
    logging.info("#########################################")
    logging.info(f"# CDMB version: {CDMB_VERSION}")
    logging.info(f"# ASPIRE version: {ASPIRE_VERSION}")
    logging.info(f"# PIPELINE version: {PIPELINE_VERSION}")
    logging.info("#########################################\n")
    
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

    
    config = get_entities_variables_configuration()
    logging.info("Common Data Model Info") 
    logging.info(json.dumps(config, indent=4, sort_keys=True))
    logging.info("#########################################")
    entities = [e['entity_name'] for e in config]
    scripts = search_scripts()
    time_ = time.time()
    copy_original_data(entities) 
    for script in scripts:
        logging.info("#########################################")
        logging.info(f"# Running script: {script}")
        logging.info("#########################################\n")
        logging.info("#########################################")    
        execute_scenario1(config,script)
        reset_original_data(entities)
        execute_scenario2(config,script)
        reset_original_data(entities)
        execute_scenario3(config,script)
        reset_original_data(entities)
        execute_scenario4(config,script)
        reset_original_data(entities)
        
    logging.info("#########################################")
    logging.info(f"# All test scenarios have been executed.")
    logging.info(f"# Restoring original values")
    remove_copy_data(entities)
    logging.info(f"# Deleting files from the outptus folder ")
    clean_outputs(time_)
    logging.info("#########################################\n")       


