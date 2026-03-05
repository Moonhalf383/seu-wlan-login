from src.main.common.interpreter import Interpreter
from src.main.client.console import print, printer

class SubInterpreter(Interpreter):
    def __init__(self):
        super().__init__("sub")

    def default_behavior(self, args):
        if args:
            ans = float(args[0])
            for i in range(1, len(args)):
                ans -= float(args[i])
            print(f"[info]{ans}[/info]")
        else:
            print(f"[warning]Unknown show object: {args}[/warning]")
