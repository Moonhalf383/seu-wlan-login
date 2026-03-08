from src.main.common.interpreter import Interpreter, ABS_PATH
import os


class CalculateInterpreter(Interpreter):
    def __init__(self):
        super().__init__(
            "calculate",
            description="测试用插件",
            plugin_dir=os.path.join(ABS_PATH, "sys_commands", "calculate"),
        )
