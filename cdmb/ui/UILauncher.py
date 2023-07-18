import glob
import json
import os
import re
import tempfile
import zipfile
from io import StringIO, BytesIO
from typing import Annotated
from typing import Union

import pandas as pd
import uvicorn
from fastapi import FastAPI, UploadFile, HTTPException, Request
# python-multipart
from fastapi import Form  # New way to declare that you want an openapi object in the form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from cdmb.CommonDataModel import CommonDataModel
from cdmb.cohort.Cohort import Cohort
from cdmb.cohort.Crosswalks import Crosswalks
from cdmb.entities.Catalog import Catalog
from cdmb.entities.Entity import Entity
from cdmb.entities.Rule import DummyRule
from cdmb.entities.RuleSet import RuleSet
from cdmb.entities.Variable import Variable
from cdmb.project.Author import Author
from cdmb.project.Metadata import Metadata

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def infer_separator(stringio_):
    firstline = stringio_.readline().rstrip()
    stringio_.seek(0)
    separators = re.sub('"*[a-zA-ZÀ-ÿñÑ0-9_-]*"*', '', firstline)
    if len(separators) > 0:
        return separators[0]
    else:
        # Return random separator, exception will be thrown on header reading
        return '|'


def zipfiles(file_list, output_dir):
    io = BytesIO()
    with zipfile.ZipFile(io, mode='w', compression=zipfile.ZIP_DEFLATED) as zip:
        for fpath in file_list:
            arcname_ = fpath.replace(output_dir + '/', '')
            if arcname_ != '':
                zip.write(fpath, arcname=arcname_)
        # close zip
        zip.close()
    return StreamingResponse(
        iter([io.getvalue()]),
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": f"attachment;"}
    )


@app.post("/api/metadata")
def create_metadata(metadata: Annotated[str, Form(media_type="multipart/form-data")]):
    metadata_ = json.loads(metadata)
    main_keys = {"project", "funder", "url_project", "work_package", "use_case", "document", "version_sem",
                 "keywords", "description", "notes", "spatial_coverage", "license"}
    core_info = {k: v for k, v in metadata_.items() if k in main_keys}
    try:
        author_info = [Author(**v) for v in metadata_['authors']]
        core_info["authors"] = author_info
    except Exception as e:
        output = "Something went wrong creating Authors: "
        output += str(e)
        raise HTTPException(status_code=400, detail=output)
    try:
        metadata = Metadata(**core_info)
    except Exception as e:
        output = "Something went wrong creating Metadata: "
        output += str(e)
        raise HTTPException(status_code=400, detail=output)
    return {"output": "Metadata created without errors"}


@app.post("/api/cohort")
def create_cohort(cohort: Annotated[str, Form(media_type="multipart/form-data")],
                  files: Union[list[UploadFile], None] = None):
    if files is None:
        files = []
    cohort_ = json.loads(cohort)
    main_keys = {"name", "description", "inclusion_criteria", "exclusion_criteria"}
    dates_keys = {"beggining_study_period", "end_study_period"}
    core_info = {k: v for k, v in cohort_.items() if k in main_keys}
    date_ifo = {k: pd.to_datetime(v) for k, v in cohort_.items() if k in dates_keys}
    core_info = core_info | date_ifo
    try:
        cohort = Cohort(**core_info)
    except Exception as e:
        output = "Something went wrong creating Cohort: "
        output += str(e)
        raise HTTPException(status_code=400, detail=output)
    filename_ = cohort_['cohort_definition_inclusion']['filename']
    try:
        if filename_ != '':
            for file in files:
                if filename_ == file.filename:
                    contents = file.file.read()
                    s = str(contents, 'utf-8')
                    data = StringIO(s)
                    separator = infer_separator(data)
                    df_crosswalks = pd.read_csv(data, sep=separator)
                    data.close()
                    file.file.close()
                    cohort.cohort_definition_inclusion = Crosswalks(df_crosswalks,
                                                                    cohort_['cohort_definition_inclusion'][
                                                                        'column_name'],
                                                                    cohort_['cohort_definition_inclusion'][
                                                                        'nature'],
                                                                    filename_)
        filename_ = cohort_['cohort_definition_exclusion']['filename']
        if filename_ != '':
            for file in files:
                if file.file.closed is False and filename_ == file.filename:
                    contents = file.file.read()
                    s = str(contents, 'utf-8')
                    data = StringIO(s)
                    separator = infer_separator(data)
                    df_crosswalks = pd.read_csv(data, sep=separator)
                    data.close()
                    file.file.close()
                    cohort.cohort_definition_exclusion = Crosswalks(df_crosswalks,
                                                                    cohort_[
                                                                        'cohort_definition_exclusion'][
                                                                        'column_name'],
                                                                    cohort_[
                                                                        'cohort_definition_exclusion'][
                                                                        'nature'],
                                                                    filename_)

    except Exception as e:
        output = "Something went wrong creating Crosswalks: "
        output += str(e)
        raise HTTPException(status_code=400, detail=output)
    return {"output": "Cohort created without errors"}


def create_variable(x, files):
    catalog = None
    if 'catalog' in x:
        catalog = x.pop('catalog')
        if catalog is not None and ('filename' not in catalog or 'column_name' not in catalog):
            catalog = None
    variable_clean = {k: v for k, v in x.items() if v is not None}
    variable = Variable(**variable_clean)
    if variable.catalog_bl and catalog is not None:
        filename_ = catalog['filename']
        columnname_ = catalog['column_name']
        if files is not None:
            for file in files:
                if file.file.closed is False and filename_ == file.filename:
                    contents = file.file.read()
                    s = str(contents, 'utf-8')
                    data = StringIO(s)
                    separator = infer_separator(data)
                    df_catalog = pd.read_csv(data, sep=separator)
                    data.close()
                    # file.file.seek(0)
                    file.file.close()
                    variable.catalog = Catalog(df_catalog, columnname_, filename_)
                    break
    return variable


@app.post("/api/entities")
def create_entities(entities: Annotated[str, Form(media_type="multipart/form-data")],
                    files: Union[list[UploadFile], None] = None):
    # Create Entities
    entities = json.loads(entities)
    entities_list = []
    entities_catalog = {}
    rules_output = ""
    for idx, entity in enumerate(entities):
        main_keys = {"name", "time_varying"}
        core_info = {k: v for k, v in entity.items() if k in main_keys}
        if 'variables' not in entity:
            raise ValueError(
                'The "entities["variables"]" field does not exist in the configuration file and is a mandatory field.')
        try:
            variables_info = [create_variable(v, files) for v in entity['variables'] if v]
            core_info["variables"] = variables_info
            entity_ = Entity(**core_info)
        except Exception as e:
            output = f"Something went wrong creating Entity (No. {idx}): "
            output += str(e)
            raise HTTPException(status_code=400, detail=output)

        if entity_.name.strip() == "":
            raise HTTPException(status_code=400, detail="The entity name cannot be an empty string.")

        if len(entity_.variables) == 0:
            raise HTTPException(status_code=400,
                                detail=f"At least one variable must exist for the \"{entity_.name}\" entity.")

        for rule in entity['rules']:
            if 'expression' not in rule:
                raise ValueError("Error in the structure of the rule. The key 'expression' must be present.")
            if 'name' not in rule:
                raise ValueError("Error in the structure of the rule. The key 'name' must be present.")
            if 'description' not in rule:
                raise ValueError("Error in the structure of the rule. The key 'description' must be present.")
            expression_ = rule['expression']
            rule_ = None
            try:
                rule_ = entity_.create_rule_from_expression(expression_, rule['name'], rule['description'])
            except Exception as e:
                if rules_output == "":
                    rules_output = " but there are some rules that could not be validated correctly."
                rule_ = DummyRule(expression_, rule['name'], rule['description'])
                pass
            if rule_ is not None:
                entity_.rules.append_rule(rule_)
        # append
        entities_catalog[entity_.name] = entity_
        entities_list.append(entity_)
    return {"output": "Entities created without errors" + rules_output}


@app.post("/api/project")
def create_project_with_files(configuration: Annotated[str, Form(media_type="multipart/form-data")],
                              files: Union[list[UploadFile], None] = None):
    try:
        if files is None:
            files = []
        configuration_ = json.loads(configuration)
        metadata_, cohort_, entities_, relationships_ = CommonDataModel.load_previous_configuration_from_web(
            configuration_,
            files)
        cdm = CommonDataModel(metadata_, cohort_, entities_, relationships_)
        with tempfile.TemporaryDirectory(dir='.') as output_dir:
            cdm.save_project(output_dir)
            file_list = glob.glob(output_dir + "/**", recursive=True) + glob.glob(output_dir + "/**/.git*", recursive=True)
            return zipfiles(file_list, output_dir)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/rules/template")
def create_rules_template(variables: Annotated[str, Form(media_type="multipart/form-data")]):
    try:
        variable_list = [Variable(**variable) for variable in json.loads(variables)]
        return RuleSet.get_rules_structure_example(variable_list)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


app.mount("/", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static_ui"), html=True), name="static_ui")


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc):
    if request.url.path in ["/", "/about", "/cohort", "/entities", "/project", "/summary", "/validation"]:
        return RedirectResponse("/")
    else:
        return JSONResponse({"detail": str(exc.detail)}, status_code=exc.status_code)


def launch_ui(server_address: str = "localhost", port: int = 8501):
    """Launch the user interface to complete the common data model.

This function uses uvicorn to run a FastAPI app that serves the user interface.

Args:
    server_address (str): The IP address to bind the server to. Defaults to "localhost".
    port (int): The port number to bind the server to. Defaults to 8501.

Raises:
    ValueError: If the port number is not in the range 0-65535.
"""
    if int(port) not in range(0, 65536):
        raise ValueError('Invalid port number')
    uvicorn.run(app, host=server_address, port=port)
