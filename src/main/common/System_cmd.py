from src.main.common.interpreter import Interpreter, ABS_PATH
import os


class SystemInterpreter(Interpreter):
    def __init__(self):
        super().__init__(
            "System",
            description="系统",
            plugin_dir=os.path.join(ABS_PATH, "sys_commands"),
        )
