import importlib
from src.main.common.interpreter import Interpreter
from src.main.client.console import printer, print
from main import ROOT_DIR

import sys
import os
import platform
import subprocess
from importlib.metadata import version, PackageNotFoundError
from packaging.requirements import Requirement

import tomllib

pyproject = os.path.join(ROOT_DIR, "pyproject.toml")

with open(pyproject, "rb") as f:
    config = tomllib.load(f)


def is_module_installed(module_name):
    try:
        version(module_name)
        return True
    except PackageNotFoundError:
        return False


class CheckHealthInterpreter(Interpreter):
    def __init__(self):
        super().__init__("health", description="检查环境依赖")

    def default_behavior(self, args):
        print(config)
        dependencies = config.get("project", {}).get("dependencies", [])
        dependency_names = [Requirement(d).name for d in dependencies]
        for dependency in dependency_names:
            if is_module_installed(dependency):
                printer(f"[info]{dependency} is installed.[/info]")
            else:
                printer(f"[error]{dependency} is not installed.[/error]")
