from src.main.common.interpreter import Interpreter
import sys

class ExitInterpreter(Interpreter):
    def __init__(self):
        super().__init__("exit")

    def default_behavior(self, args):
        sys.exit(0)
