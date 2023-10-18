import os
import shutil


def generate_documentation(out_dir):
    copyFileDoc(out_dir)
    copyFilesTemplates(out_dir)
    copyFileValidator(out_dir)
    copyFileDqa(out_dir)
    copyFileCheckLoad(out_dir)
    copyFilesEmptyFolders(out_dir)


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
