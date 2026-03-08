from src.main.common.interpreter import Interpreter, ABS_PATH
import os


class ConfigInterpreter(Interpreter):
    def __init__(self):
        super().__init__(
            "config",
            description="配置基本信息",
            plugin_dir=os.path.join(ABS_PATH, "sys_commands", "config"),
        )
