from src.main.common.interpreter import Interpreter, ABS_PATH
import os

class SystemInterpreter(Interpreter):
    def __init__(self):
        super().__init__("System", os.path.join(ABS_PATH, "sys_commands"))
