#!/usr/bin/env python
import os

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))

def rename_file(filepath, new_filepath):
    abs_original_filepath = os.path.join(PROJECT_DIRECTORY, filepath)
    abs_new_filepath = os.path.join(PROJECT_DIRECTORY, new_filepath)
    os.rename(abs_original_filepath, abs_new_filepath)


if __name__ == "__main__":

    if "{{ cookiecutter.install_precommit_hooks }}" != "y":
        remove_file(".pre-commit-config.yaml")

    if "Not open source" == "{{ cookiecutter.open_source_license }}":
        remove_file("LICENSE")

    rename_file(".gitignore.tpl", ".gitignore")
