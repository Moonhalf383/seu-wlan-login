from src.main.common.interpreter import Interpreter
from src.main.client.console import printer
from main import ROOT_DIR

import tomllib
import os

pyproject = os.path.join(ROOT_DIR, "pyproject.toml")


class ShowInterpreter(Interpreter):
    def __init__(self):
        super().__init__("show", description="显示基本信息")

    def default_behavior(self, args):
        with open(pyproject, "rb") as f:
            config = tomllib.load(f)
        version = config["project"]["version"]
        status = config["project"]["description"]
        printer(f"[info]Version: {version}[/info]")
        printer(f"[info]Description: {status}[/info]")
