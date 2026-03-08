from src.main.common.interpreter import Interpreter
from src.main.client.console import printer


class CheckPlatformInterpreter(Interpreter):
    def __init__(self):
        super().__init__("network", description="检查当前网络基本状况")

    def default_behavior(self, args):
        pass
