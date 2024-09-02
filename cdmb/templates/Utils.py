import os
import shutil
import datetime
import json
import pandas as pd

from cdmb import Author


def generate_documentation(out_dir, info_citation):
    copyFileDoc(out_dir)
    copyFilesTemplates(out_dir)
    copyFileValidator(out_dir)
    copyFileDqa(out_dir)
    copyFileCheckLoad(out_dir)
    copyFilesEmptyFolders(out_dir)
    createCitationfile(out_dir, info_citation)
    createZenodoJson(out_dir, info_citation)


def createZenodoJson(out_dir: str, info_citation):
    zenodo_info = {"title": info_citation['title'], "description": info_citation['description'], "creators": []}
    authors: list[Author] = info_citation['authors']
    for author in authors:
        zenodo_info["creators"].append({
            "name": f"{author.name}",
            "affiliation": f"{author.affiliation}",
            "orcid": f"{author.id}"
        })
    zenodo_info["keywords"] = info_citation['keywords']
    with open(os.path.join(out_dir, "zenodo_template.json"), 'w', encoding='utf-8') as file:
        json.dump(zenodo_info, file,ensure_ascii=False, indent=4)



def createCitationfile(out_dir: str, info_citation):
    authors: list[Author] = info_citation['authors']

    citation_data = {
        "cff-version": "1.2.0",
        "message": "If you use this software, please cite it as below:",
        "title": info_citation['title'],
        "version": info_citation['version'],
        "date-released": datetime.date.today().isoformat(),
        "url": info_citation['url'],
        "doi": "your_project_doi",
        "repository-code": "https://github.com/user/repository",
        "license": info_citation['license']
    }

    citation_content = f"""cff-version: {citation_data['cff-version']}
message: "{citation_data['message']}"
title: "{citation_data['title']}"
version: "{citation_data['version']}"
date-released: "{citation_data['date-released']}" 
"""

    authors_txt = f""""""
    if len(authors) > 0:
        for author in authors:
            family_names = ""
            given_names = author.name
            orcid = ""
            if ',' in author.name:
                family_names = author.name.split(',')[0].strip()
                given_names = author.name.split(',')[1].strip()
            if author.id is not None and author.id != "":
                orcid = f"https://orcid.org/{author.id}"
            authors_txt += f"""
- family-names: "{family_names}"
  given-names: "{given_names}"
  orcid: "{orcid}" """
        citation_content += f"""authors:"""
        citation_content += authors_txt

    citation_content += f"""
url: "{citation_data['url']}"
repository-code: "{citation_data['repository-code']}"
license: "{citation_data['license']}"
    """

    # Guardar el contenido en un archivo CITATION.cff
    with open(os.path.join(out_dir, "CITATION.cff"), 'w') as file:
        file.write(citation_content)


def copyFileDoc(out_dir: str):
    docs = ["man_container_deployment.md", "README.md", "LICENSE.md"]
    for doc in docs:
        original = os.path.join(os.path.dirname(__file__), 'files', doc)
        target = os.path.join(out_dir, doc)
        shutil.copyfile(original, target)
    original = os.path.join(os.path.dirname(__file__), 'files', ".gitignore")
    shutil.copy(original, os.path.join(out_dir, ".gitignore"))


def copyFileDqa(out_dir: str):
    filename = "dqa.py"
    original = os.path.join(os.path.dirname(__file__), "files", filename)
    target = os.path.join(out_dir, "src", "dqa-scripts", filename)
    shutil.copyfile(original, target)


def copyFileValidator(out_dir: str):
    filenames = ["validator.py", "validator_report.qmd", "_quarto.yml"]
    for filename in filenames:
        original = os.path.join(os.path.dirname(__file__), "files", filename)
        target = os.path.join(out_dir, "src", "validation-scripts", filename)
        shutil.copyfile(original, target)


def copyFileCheckLoad(out_dir: str):
    filename = "check_load.py"
    original = os.path.join(os.path.dirname(__file__), "files", filename)
    target = os.path.join(out_dir, "src", "check_load-scripts", filename)
    shutil.copyfile(original, target)


def copyFilesTemplates(out_dir: str):
    filenames = ["r_report_template.qmd", "_quarto.yml", "testing.py"]
    for filename in filenames:
        original = os.path.join(os.path.dirname(__file__), "files", filename)
        target = os.path.join(out_dir, "src", "analysis-scripts", filename)
        shutil.copyfile(original, target)


def copyFilesEmptyFolders(out_dir: str):
    # inputs
    original = os.path.join(os.path.dirname(__file__), "files", 'readme_input.txt')
    target = os.path.join(out_dir, "inputs", "readme.txt")
    shutil.copyfile(original, target)
    # src/check_load-scripts/inputs
    original = os.path.join(os.path.dirname(__file__), "files", 'readme_input.txt')
    target = os.path.join(out_dir, "src", "check_load-scripts", "inputs", "readme.txt")
    shutil.copyfile(original, target)
    # outputs
    original = os.path.join(os.path.dirname(__file__), "files", 'readme_outputs.txt')
    target = os.path.join(out_dir, "outputs", 'readme.txt')
    shutil.copyfile(original, target)

    # outputs logs
    original = os.path.join(os.path.dirname(__file__), "files", 'readme_logs.txt')
    target = os.path.join(out_dir, "outputs", "logs", "readme.txt")
    shutil.copyfile(original, target)
