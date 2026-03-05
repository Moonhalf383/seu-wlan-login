from src.main.common.interpreter import Interpreter
from src.main.client.console import printer

version = "demo"

status = "Running"

class ShowInterpreter(Interpreter):
    def __init__(self):
        super().__init__("show")

    def default_behavior(self, args):
        printer(f"[info]Version: {version}[/info]")
        printer(f"[info]Status: {status}[/info]")
