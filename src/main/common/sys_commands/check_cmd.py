from src.main.common.interpreter import Interpreter, ABS_PATH
import os


class CheckInterpreter(Interpreter):
    def __init__(self):
        super().__init__(
            "check",
            description="检查脚本状况",
            plugin_dir=os.path.join(ABS_PATH, "sys_commands", "check"),
        )
