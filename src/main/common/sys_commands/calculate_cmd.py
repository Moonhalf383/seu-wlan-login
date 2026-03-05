from src.main.common.interpreter import Interpreter, ABS_PATH
import os

class CalculateInterpreter(Interpreter):
    def __init__(self):
        super().__init__("calculate",os.path.join(ABS_PATH,"sys_commands","calculate"))
