import os
import shutil


def generate_documentation(out_dir):
    copyFileDoc(out_dir)
    copyFilesTemplates(out_dir)
    copyFileValidator(out_dir)
    copyFileDqa(out_dir)
    copyFileCheckLoad(out_dir)


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
    filenames = ["r_report_template.qmd", "_quarto.yml"]
    for filename in filenames:
        original = os.path.join(os.path.dirname(__file__), "files", filename)
        target = os.path.join(out_dir, "src", "analysis-scripts", filename)
        shutil.copyfile(original, target)
