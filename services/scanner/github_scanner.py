import os
import shutil
from git import Repo
from scanner import scan_yaml_content

TEMP_DIR = "temp_repo"


def clone_repo(repo_url):
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)

    Repo.clone_from(repo_url, TEMP_DIR)
    return TEMP_DIR


def find_yaml_files(base_path):
    yaml_files = []

    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith((".yaml", ".yml")):
                yaml_files.append(os.path.join(root, file))

    return yaml_files


def scan_repo(repo_url):
    repo_path = clone_repo(repo_url)
    yaml_files = find_yaml_files(repo_path)

    all_results = []

    for file_path in yaml_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            issues = scan_yaml_content(content)

            if issues:
                all_results.append({
                    "file": file_path,
                    "issues": issues
                })

        except Exception as e:
            continue

    return all_results