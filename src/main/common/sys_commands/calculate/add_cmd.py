from src.main.common.interpreter import Interpreter
from src.main.client.console import print, printer


class AddInterpreter(Interpreter):
    def __init__(self):
        super().__init__("add", description="若干数字相加")

    def default_behavior(self, args):
        if args:
            ans = 0
            for i in args:
                ans += float(i)
            print(f"[info]{ans}[/info]")
        else:
            print(f"[warning]Unknown show object: {args}[/warning]")
